"""モックデータを使用したアプリケーションのテスト"""

from unittest.mock import patch, MagicMock
from weather_zip_lookup.cli import main
from weather_zip_lookup.models import WeatherData, WeatherAlert
import sys


def test_with_mock_data():
    """モックデータを使用して完全なフローをテスト"""
    
    # モックの天気データを作成
    mock_weather_data = WeatherData(
        postal_code="1000001",
        temperature=22.5,
        precipitation_probability=35.0,
        alerts=[
            WeatherAlert(
                alert_type="大雨",
                description="大雨警報が発令されています",
                severity="高"
            )
        ],
        location_name="東京都千代田区"
    )
    
    # コマンドライン引数をモック
    with patch.object(sys, 'argv', ['weather.py', '1000001']), \
         patch('weather_zip_lookup.cli.WeatherService') as mock_service:
        
        # WeatherServiceのモック
        mock_service_instance = mock_service.return_value
        mock_service_instance.get_weather_by_postal_code.return_value = mock_weather_data
        
        # main関数を実行
        print("=" * 60)
        print("モックデータを使用したアプリケーションテスト")
        print("=" * 60)
        print()
        
        exit_code = main()
        
        print()
        print("=" * 60)
        print(f"終了コード: {exit_code}")
        print("=" * 60)
        
        if exit_code == 0:
            print("\n✅ アプリケーションは正常に動作しています！")
            print("APIキーが有効になれば、実際の天気データを取得できます。")
        else:
            print(f"\n❌ エラーが発生しました（終了コード: {exit_code}）")


if __name__ == "__main__":
    test_with_mock_data()
