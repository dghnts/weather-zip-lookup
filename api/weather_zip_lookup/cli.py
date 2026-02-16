"""
CLIインターフェースモジュール

コマンドライン引数の解析とメインフロー制御を提供します。
"""

import argparse
import sys
from typing import Optional

from .config import ConfigManager
from .exceptions import (
    InvalidPostalCodeError,
    APIError,
    NetworkError,
    ConfigError,
    MissingAPIKeyError
)
from .weather_service import WeatherService
from .formatter import OutputFormatter


def parse_arguments() -> argparse.Namespace:
    """
    コマンドライン引数を解析
    
    Returns:
        解析された引数を含むNamespaceオブジェクト
    """
    parser = argparse.ArgumentParser(
        prog='weather-zip-lookup',
        description='郵便番号から天気情報を取得するターミナルスクリプト',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用例:
  %(prog)s 1000001          # 指定した郵便番号の天気を取得
  %(prog)s                  # デフォルトの郵便番号の天気を取得
  %(prog)s -h               # ヘルプを表示
        '''
    )
    
    parser.add_argument(
        'postal_code',
        nargs='?',
        help='7桁の日本の郵便番号（例: 1000001）。省略した場合は設定ファイルのデフォルト値を使用します。'
    )
    
    return parser.parse_args()


def main() -> int:
    """
    メインエントリーポイント
    
    Returns:
        終了コード（0: 成功、1以上: エラー）
    """
    try:
        # コマンドライン引数を解析
        args = parse_arguments()
        
        # 設定マネージャーを初期化
        config_manager = ConfigManager()
        
        # 郵便番号を取得（引数 > 設定ファイル）
        postal_code = args.postal_code
        if not postal_code:
            # コマンドライン引数がない場合は設定ファイルから取得
            postal_code = config_manager.get_default_postal_code()
            if not postal_code:
                print("エラー: 郵便番号が指定されていません。")
                print("コマンドライン引数で郵便番号を指定するか、設定ファイルにデフォルトの郵便番号を設定してください。")
                print(f"設定ファイルの場所: {config_manager.get_config_path()}")
                return 3
        
        # APIキーを取得
        api_key = config_manager.get_api_key()
        if not api_key:
            print("エラー: APIキーが設定されていません。")
            print("OpenWeatherMapからAPIキーを取得し、設定ファイルに保存してください。")
            print(f"設定ファイルの場所: {config_manager.get_config_path()}")
            print("\n設定ファイルの例:")
            print('{')
            print('  "default_postal_code": "1000001",')
            print('  "api_key": "your_api_key_here"')
            print('}')
            return 5
        
        # 天気サービスを初期化
        weather_service = WeatherService(api_key)
        
        # 天気データを取得
        weather_data = weather_service.get_weather_by_postal_code(postal_code)
        
        # 出力フォーマッターを初期化
        formatter = OutputFormatter()
        
        # フォーマットされた出力を表示
        output = formatter.format_weather_output(weather_data)
        print(output)
        
        return 0
        
    except InvalidPostalCodeError as e:
        print(f"エラー: {e}")
        return 3
    except MissingAPIKeyError as e:
        print(f"エラー: {e}")
        return 5
    except NetworkError as e:
        print(f"エラー: {e}")
        return 1
    except APIError as e:
        print(f"エラー: {e}")
        return 2
    except ConfigError as e:
        print(f"エラー: {e}")
        return 4
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
