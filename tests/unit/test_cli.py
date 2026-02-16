"""
CLIモジュールのユニットテスト
"""

import pytest
import sys
from unittest.mock import patch

from weather_zip_lookup.cli import parse_arguments


class TestParseArguments:
    """parse_arguments関数のテスト"""
    
    def test_parse_postal_code_argument(self):
        """郵便番号引数が正しく解析されることを確認"""
        with patch.object(sys, 'argv', ['weather-zip-lookup', '1000001']):
            args = parse_arguments()
            assert args.postal_code == '1000001'
    
    def test_parse_no_arguments(self):
        """引数なしで実行した場合、postal_codeがNoneになることを確認"""
        with patch.object(sys, 'argv', ['weather-zip-lookup']):
            args = parse_arguments()
            assert args.postal_code is None
    
    def test_help_flag_short(self):
        """短いヘルプフラグ(-h)が機能することを確認"""
        with patch.object(sys, 'argv', ['weather-zip-lookup', '-h']):
            with pytest.raises(SystemExit) as exc_info:
                parse_arguments()
            # argparseはヘルプ表示時に0で終了する
            assert exc_info.value.code == 0
    
    def test_help_flag_long(self):
        """長いヘルプフラグ(--help)が機能することを確認"""
        with patch.object(sys, 'argv', ['weather-zip-lookup', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                parse_arguments()
            # argparseはヘルプ表示時に0で終了する
            assert exc_info.value.code == 0
    
    def test_parse_multiple_digit_postal_code(self):
        """7桁の郵便番号が正しく解析されることを確認"""
        with patch.object(sys, 'argv', ['weather-zip-lookup', '5430001']):
            args = parse_arguments()
            assert args.postal_code == '5430001'


class TestMain:
    """main関数のテスト"""
    
    def test_main_with_valid_postal_code_argument(self, tmp_path, monkeypatch):
        """有効な郵便番号引数で実行した場合、成功することを確認"""
        from weather_zip_lookup.cli import main
        from weather_zip_lookup.models import WeatherData
        
        # 設定ファイルのパスをモック
        config_path = tmp_path / "config.json"
        config_path.write_text('{"api_key": "test_api_key"}')
        
        # モックの設定
        with patch.object(sys, 'argv', ['weather-zip-lookup', '1000001']), \
             patch('weather_zip_lookup.cli.ConfigManager') as mock_config_manager, \
             patch('weather_zip_lookup.cli.WeatherService') as mock_weather_service, \
             patch('weather_zip_lookup.cli.OutputFormatter') as mock_formatter:
            
            # ConfigManagerのモック
            mock_config_instance = mock_config_manager.return_value
            mock_config_instance.get_api_key.return_value = 'test_api_key'
            mock_config_instance.get_default_postal_code.return_value = None
            
            # WeatherServiceのモック
            mock_weather_instance = mock_weather_service.return_value
            mock_weather_data = WeatherData(
                postal_code='1000001',
                temperature=20.0,
                precipitation_probability=30.0,
                alerts=[],
                location_name='東京'
            )
            mock_weather_instance.get_weather_by_postal_code.return_value = mock_weather_data
            
            # OutputFormatterのモック
            mock_formatter_instance = mock_formatter.return_value
            mock_formatter_instance.format_weather_output.return_value = 'Formatted output'
            
            # main関数を実行
            exit_code = main()
            
            # 検証
            assert exit_code == 0
            mock_weather_instance.get_weather_by_postal_code.assert_called_once_with('1000001')
            mock_formatter_instance.format_weather_output.assert_called_once_with(mock_weather_data)
    
    def test_main_with_default_postal_code(self, tmp_path):
        """引数なしで設定ファイルのデフォルト郵便番号を使用する場合"""
        from weather_zip_lookup.cli import main
        from weather_zip_lookup.models import WeatherData
        
        with patch.object(sys, 'argv', ['weather-zip-lookup']), \
             patch('weather_zip_lookup.cli.ConfigManager') as mock_config_manager, \
             patch('weather_zip_lookup.cli.WeatherService') as mock_weather_service, \
             patch('weather_zip_lookup.cli.OutputFormatter') as mock_formatter:
            
            # ConfigManagerのモック
            mock_config_instance = mock_config_manager.return_value
            mock_config_instance.get_api_key.return_value = 'test_api_key'
            mock_config_instance.get_default_postal_code.return_value = '5430001'
            
            # WeatherServiceのモック
            mock_weather_instance = mock_weather_service.return_value
            mock_weather_data = WeatherData(
                postal_code='5430001',
                temperature=15.0,
                precipitation_probability=50.0,
                alerts=[],
                location_name='大阪'
            )
            mock_weather_instance.get_weather_by_postal_code.return_value = mock_weather_data
            
            # OutputFormatterのモック
            mock_formatter_instance = mock_formatter.return_value
            mock_formatter_instance.format_weather_output.return_value = 'Formatted output'
            
            # main関数を実行
            exit_code = main()
            
            # 検証
            assert exit_code == 0
            mock_weather_instance.get_weather_by_postal_code.assert_called_once_with('5430001')
    
    def test_main_without_postal_code_and_config(self, capsys):
        """郵便番号が引数にも設定ファイルにもない場合、エラーを返す"""
        from weather_zip_lookup.cli import main
        
        with patch.object(sys, 'argv', ['weather-zip-lookup']), \
             patch('weather_zip_lookup.cli.ConfigManager') as mock_config_manager:
            
            # ConfigManagerのモック
            mock_config_instance = mock_config_manager.return_value
            mock_config_instance.get_api_key.return_value = 'test_api_key'
            mock_config_instance.get_default_postal_code.return_value = None
            
            # main関数を実行
            exit_code = main()
            
            # 検証
            assert exit_code == 3
            captured = capsys.readouterr()
            assert '郵便番号が指定されていません' in captured.out
    
    def test_main_without_api_key(self, capsys):
        """APIキーが設定されていない場合、エラーを返す"""
        from weather_zip_lookup.cli import main
        
        with patch.object(sys, 'argv', ['weather-zip-lookup', '1000001']), \
             patch('weather_zip_lookup.cli.ConfigManager') as mock_config_manager:
            
            # ConfigManagerのモック
            mock_config_instance = mock_config_manager.return_value
            mock_config_instance.get_api_key.return_value = None
            
            # main関数を実行
            exit_code = main()
            
            # 検証
            assert exit_code == 5
            captured = capsys.readouterr()
            assert 'APIキーが設定されていません' in captured.out
    
    def test_main_with_invalid_postal_code(self, capsys):
        """無効な郵便番号の場合、エラーを返す"""
        from weather_zip_lookup.cli import main
        from weather_zip_lookup.exceptions import InvalidPostalCodeError
        
        with patch.object(sys, 'argv', ['weather-zip-lookup', '123']), \
             patch('weather_zip_lookup.cli.ConfigManager') as mock_config_manager, \
             patch('weather_zip_lookup.cli.WeatherService') as mock_weather_service:
            
            # ConfigManagerのモック
            mock_config_instance = mock_config_manager.return_value
            mock_config_instance.get_api_key.return_value = 'test_api_key'
            
            # WeatherServiceのモック
            mock_weather_instance = mock_weather_service.return_value
            mock_weather_instance.get_weather_by_postal_code.side_effect = InvalidPostalCodeError(
                "無効な郵便番号形式です。7桁の数字を入力してください。"
            )
            
            # main関数を実行
            exit_code = main()
            
            # 検証
            assert exit_code == 3
            captured = capsys.readouterr()
            assert '無効な郵便番号形式' in captured.out
    
    def test_main_with_network_error(self, capsys):
        """ネットワークエラーの場合、エラーを返す"""
        from weather_zip_lookup.cli import main
        from weather_zip_lookup.exceptions import NetworkError
        
        with patch.object(sys, 'argv', ['weather-zip-lookup', '1000001']), \
             patch('weather_zip_lookup.cli.ConfigManager') as mock_config_manager, \
             patch('weather_zip_lookup.cli.WeatherService') as mock_weather_service:
            
            # ConfigManagerのモック
            mock_config_instance = mock_config_manager.return_value
            mock_config_instance.get_api_key.return_value = 'test_api_key'
            
            # WeatherServiceのモック
            mock_weather_instance = mock_weather_service.return_value
            mock_weather_instance.get_weather_by_postal_code.side_effect = NetworkError(
                "ネットワーク接続に失敗しました。"
            )
            
            # main関数を実行
            exit_code = main()
            
            # 検証
            assert exit_code == 1
            captured = capsys.readouterr()
            assert 'ネットワーク接続に失敗しました' in captured.out
    
    def test_main_with_api_error(self, capsys):
        """APIエラーの場合、エラーを返す"""
        from weather_zip_lookup.cli import main
        from weather_zip_lookup.exceptions import APIError
        
        with patch.object(sys, 'argv', ['weather-zip-lookup', '1000001']), \
             patch('weather_zip_lookup.cli.ConfigManager') as mock_config_manager, \
             patch('weather_zip_lookup.cli.WeatherService') as mock_weather_service:
            
            # ConfigManagerのモック
            mock_config_instance = mock_config_manager.return_value
            mock_config_instance.get_api_key.return_value = 'test_api_key'
            
            # WeatherServiceのモック
            mock_weather_instance = mock_weather_service.return_value
            mock_weather_instance.get_weather_by_postal_code.side_effect = APIError(
                "無効なAPIキーです。"
            )
            
            # main関数を実行
            exit_code = main()
            
            # 検証
            assert exit_code == 2
            captured = capsys.readouterr()
            assert '無効なAPIキーです' in captured.out
