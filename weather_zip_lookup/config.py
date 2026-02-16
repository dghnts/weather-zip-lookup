"""設定ファイル管理モジュール"""

import json
import platform
from pathlib import Path
from typing import Optional

from .exceptions import ConfigError


class ConfigManager:
    """設定ファイルを管理するクラス"""
    
    def __init__(self):
        """設定ファイルのパスを初期化"""
        self._config_path = self.get_config_path()
    
    def get_config_path(self) -> Path:
        """
        プラットフォーム固有の設定ファイルパスを取得
        
        Returns:
            設定ファイルのPathオブジェクト
        """
        system = platform.system()
        
        if system == "Windows":
            # Windows: %APPDATA%\weather-zip-lookup\config.json
            base_path = Path.home() / "AppData" / "Roaming"
        elif system == "Darwin":
            # Mac OS: ~/.config/weather-zip-lookup/config.json
            base_path = Path.home() / ".config"
        else:
            # Linux: ~/.config/weather-zip-lookup/config.json
            base_path = Path.home() / ".config"
        
        config_dir = base_path / "weather-zip-lookup"
        return config_dir / "config.json"
    
    def load_config(self) -> dict:
        """
        設定ファイルを読み込む
        
        Returns:
            設定データを含む辞書
            
        Raises:
            ConfigError: 設定ファイルの読み取りに失敗した場合
        """
        if not self._config_path.exists():
            return {}
        
        try:
            with open(self._config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # JSONが辞書であることを検証
                if not isinstance(data, dict):
                    raise ConfigError(
                        f"設定ファイルの形式が無効です: 辞書である必要がありますが、{type(data).__name__}が見つかりました"
                    )
                
                return data
        except (json.JSONDecodeError, IOError) as e:
            raise ConfigError(f"設定ファイルの読み取りに失敗しました: {e}")
    
    def save_config(self, config: dict) -> None:
        """
        設定ファイルに保存
        
        Args:
            config: 保存する設定データ
            
        Raises:
            ConfigError: 設定ファイルの書き込みに失敗した場合
        """
        try:
            # ディレクトリが存在しない場合は作成
            self._config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise ConfigError(f"設定ファイルの書き込みに失敗しました: {e}")
    
    def get_default_postal_code(self) -> Optional[str]:
        """
        デフォルトの郵便番号を取得
        
        Returns:
            郵便番号文字列、設定されていない場合はNone
        """
        config = self.load_config()
        return config.get("default_postal_code")
    
    def get_api_key(self) -> Optional[str]:
        """
        APIキーを取得
        
        Returns:
            APIキー文字列、設定されていない場合はNone
        """
        config = self.load_config()
        return config.get("api_key")
