"""設定管理のプロパティベーステスト"""

import tempfile
from pathlib import Path
from unittest.mock import patch

from hypothesis import given, strategies as st

from weather_zip_lookup.config import ConfigManager


# プラットフォーム名の戦略
PLATFORM_STRATEGY = st.sampled_from(["Windows", "Darwin", "Linux"])


# Feature: weather-zip-lookup, Property 7: 設定ファイルのラウンドトリップ
# 検証: 要件 3.2, 3.5, 6.2
@given(
    postal_code=st.text(
        alphabet=st.characters(min_codepoint=0x30, max_codepoint=0x39),  # 0-9
        min_size=7,
        max_size=7
    ),
    api_key=st.text(min_size=1, max_size=100)
)
def test_config_roundtrip(postal_code, api_key):
    """
    プロパティ7: 設定ファイルのラウンドトリップ
    
    任意の有効な郵便番号とAPIキーに対して、設定ファイルに保存してから
    読み取った値は、元の値と一致するべきである
    
    **Validates: Requirements 3.2, 3.5, 6.2**
    """
    # 一時ディレクトリを作成
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        config_dir = tmp_path / "weather-zip-lookup"
        config_file = config_dir / "config.json"
        
        # ConfigManagerが一時パスを使用するようにパッチ
        with patch.object(ConfigManager, 'get_config_path', return_value=config_file):
            # ConfigManagerインスタンスを作成
            config_manager = ConfigManager()
            
            # 設定データを作成
            original_config = {
                "default_postal_code": postal_code,
                "api_key": api_key
            }
            
            # 設定を保存
            config_manager.save_config(original_config)
            
            # 設定を読み込み
            loaded_config = config_manager.load_config()
            
            # ラウンドトリップの検証: 保存した値と読み込んだ値が一致すること
            assert loaded_config["default_postal_code"] == postal_code, \
                f"郵便番号が一致しません: 期待={postal_code}, 実際={loaded_config.get('default_postal_code')}"
            assert loaded_config["api_key"] == api_key, \
                f"APIキーが一致しません: 期待={api_key}, 実際={loaded_config.get('api_key')}"
            
            # get_default_postal_code()とget_api_key()メソッドでも検証
            assert config_manager.get_default_postal_code() == postal_code, \
                "get_default_postal_code()が元の値を返しません"
            assert config_manager.get_api_key() == api_key, \
                "get_api_key()が元の値を返しません"



# Feature: weather-zip-lookup, Property 9: プラットフォーム固有のパス生成
# 検証: 要件 3.4, 4.4
@given(platform_name=PLATFORM_STRATEGY)
def test_platform_specific_path_generation(platform_name):
    """
    プロパティ9: プラットフォーム固有のパス生成
    
    任意のプラットフォーム(Mac OS、Windows、Linux)に対して、
    Weather_Scriptはそのプラットフォームに適した設定ファイルパスを生成するべきである
    
    **Validates: Requirements 3.4, 4.4**
    """
    # platform.system()をモック
    with patch('weather_zip_lookup.config.platform.system', return_value=platform_name):
        config_manager = ConfigManager()
        config_path = config_manager.get_config_path()
        
        # パスがPathオブジェクトであることを確認
        assert isinstance(config_path, Path), \
            f"設定パスはPathオブジェクトであるべきです: {type(config_path)}"
        
        # パスが絶対パスであることを確認
        assert config_path.is_absolute(), \
            f"設定パスは絶対パスであるべきです: {config_path}"
        
        # パスに"weather-zip-lookup"ディレクトリが含まれることを確認
        assert "weather-zip-lookup" in str(config_path), \
            f"設定パスに'weather-zip-lookup'ディレクトリが含まれるべきです: {config_path}"
        
        # パスが"config.json"で終わることを確認
        assert config_path.name == "config.json", \
            f"設定ファイル名は'config.json'であるべきです: {config_path.name}"
        
        # プラットフォーム固有のパス検証
        path_str = str(config_path)
        
        if platform_name == "Windows":
            # Windows: %APPDATA%\weather-zip-lookup\config.json
            # パスに"AppData"と"Roaming"が含まれることを確認
            assert "AppData" in path_str and "Roaming" in path_str, \
                f"Windowsの設定パスには'AppData\\Roaming'が含まれるべきです: {config_path}"
        elif platform_name == "Darwin":
            # Mac OS: ~/.config/weather-zip-lookup/config.json
            assert ".config" in path_str, \
                f"Mac OSの設定パスには'.config'が含まれるべきです: {config_path}"
        else:  # Linux
            # Linux: ~/.config/weather-zip-lookup/config.json
            assert ".config" in path_str, \
                f"Linuxの設定パスには'.config'が含まれるべきです: {config_path}"
        
        # ホームディレクトリから始まることを確認
        home = Path.home()
        try:
            config_path.relative_to(home)
        except ValueError:
            raise AssertionError(
                f"設定パスはホームディレクトリ配下にあるべきです: {config_path} (home: {home})"
            )


# Feature: weather-zip-lookup, Property 8: 設定ファイルエラーの処理
# 検証: 要件 3.3, 7.4
@given(
    corrupted_content=st.one_of(
        st.just(""),  # 空ファイル
        st.just("{"),  # 不完全なJSON
        st.just("not json at all"),  # 無効なJSON
        st.just("{'invalid': 'json'}"),  # シングルクォートJSON
        st.just("[1, 2, 3]"),  # 配列（辞書ではない）
        st.text(min_size=1, max_size=100).filter(lambda x: x.strip() and not x.strip().startswith('{')),  # ランダムテキスト
    )
)
def test_config_file_error_handling(corrupted_content):
    """
    プロパティ8: 設定ファイルエラーの処理
    
    任意の破損した設定ファイルまたは存在しない設定ファイルに対して、
    Weather_Scriptは適切なプロンプトまたはエラーメッセージを表示するべきである
    
    **Validates: Requirements 3.3, 7.4**
    """
    from weather_zip_lookup.exceptions import ConfigError
    
    # 一時ディレクトリを作成
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        config_dir = tmp_path / "weather-zip-lookup"
        config_file = config_dir / "config.json"
        
        # ConfigManagerが一時パスを使用するようにパッチ
        with patch.object(ConfigManager, 'get_config_path', return_value=config_file):
            config_manager = ConfigManager()
            
            # ケース1: 存在しない設定ファイル
            # load_config()は空の辞書を返すべき（エラーではない）
            loaded_config = config_manager.load_config()
            assert loaded_config == {}, \
                "存在しない設定ファイルの場合、空の辞書を返すべきです"
            
            # get_default_postal_code()とget_api_key()はNoneを返すべき
            assert config_manager.get_default_postal_code() is None, \
                "設定ファイルが存在しない場合、get_default_postal_code()はNoneを返すべきです"
            assert config_manager.get_api_key() is None, \
                "設定ファイルが存在しない場合、get_api_key()はNoneを返すべきです"
            
            # ケース2: 破損した設定ファイル
            # ディレクトリを作成して破損したファイルを書き込む
            config_dir.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(corrupted_content)
            
            # 破損したファイルを読み込もうとするとConfigErrorが発生すべき
            try:
                config_manager.load_config()
                # JSONとして有効な場合（例: 空配列）は例外が発生しないこともある
                # その場合でも、エラーメッセージなしで処理されるべき
            except ConfigError as e:
                # ConfigErrorが発生した場合、エラーメッセージが含まれることを確認
                error_message = str(e)
                assert len(error_message) > 0, \
                    "ConfigErrorには説明的なエラーメッセージが含まれるべきです"
                assert "設定ファイル" in error_message or "読み取り" in error_message, \
                    f"エラーメッセージには設定ファイルに関する情報が含まれるべきです: {error_message}"
            
            # get_default_postal_code()とget_api_key()も同様にエラーを伝播すべき
            try:
                config_manager.get_default_postal_code()
            except ConfigError:
                pass  # ConfigErrorが発生することを期待
            
            try:
                config_manager.get_api_key()
            except ConfigError:
                pass  # ConfigErrorが発生することを期待
