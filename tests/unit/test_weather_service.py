"""WeatherServiceのユニットテスト"""

import pytest
import responses
from weather_zip_lookup.services import WeatherService
from weather_zip_lookup.exceptions import (
    InvalidPostalCodeError,
    APIError,
    NetworkError,
    MissingAPIKeyError
)
from weather_zip_lookup.models import WeatherData, WeatherAlert


class TestWeatherServiceInit:
    """WeatherServiceの初期化テスト"""
    
    def test_init_with_valid_api_key(self):
        """有効なAPIキーで初期化できる"""
        service = WeatherService("test_api_key")
        assert service.api_key == "test_api_key"
    
    def test_init_with_empty_api_key(self):
        """空のAPIキーで初期化するとエラー"""
        with pytest.raises(MissingAPIKeyError):
            WeatherService("")
    
    def test_init_with_whitespace_api_key(self):
        """空白のみのAPIキーで初期化するとエラー"""
        with pytest.raises(MissingAPIKeyError):
            WeatherService("   ")
    
    def test_init_strips_whitespace(self):
        """APIキーの前後の空白を削除"""
        service = WeatherService("  test_api_key  ")
        assert service.api_key == "test_api_key"


class TestPostalCodeValidation:
    """郵便番号検証のテスト"""
    
    def test_valid_postal_code(self):
        """有効な7桁の郵便番号"""
        service = WeatherService("test_api_key")
        # 例外が発生しないことを確認
        service._validate_postal_code("1000001")
    
    def test_invalid_postal_code_too_short(self):
        """6桁の郵便番号は無効"""
        service = WeatherService("test_api_key")
        with pytest.raises(InvalidPostalCodeError):
            service._validate_postal_code("100000")
    
    def test_invalid_postal_code_too_long(self):
        """8桁の郵便番号は無効"""
        service = WeatherService("test_api_key")
        with pytest.raises(InvalidPostalCodeError):
            service._validate_postal_code("10000001")
    
    def test_invalid_postal_code_with_letters(self):
        """文字を含む郵便番号は無効"""
        service = WeatherService("test_api_key")
        with pytest.raises(InvalidPostalCodeError):
            service._validate_postal_code("100000A")
    
    def test_invalid_postal_code_empty(self):
        """空の郵便番号は無効"""
        service = WeatherService("test_api_key")
        with pytest.raises(InvalidPostalCodeError):
            service._validate_postal_code("")
    
    def test_invalid_postal_code_none(self):
        """Noneの郵便番号は無効"""
        service = WeatherService("test_api_key")
        with pytest.raises(InvalidPostalCodeError):
            service._validate_postal_code(None)



class TestGeocodingAPI:
    """Geocoding APIのテスト"""
    
    @responses.activate
    def test_convert_postal_code_success(self):
        """郵便番号を緯度経度に変換成功"""
        responses.add(
            responses.GET,
            "http://api.openweathermap.org/geo/1.0/zip",
            json={
                'lat': 35.6895,
                'lon': 139.6917,
                'name': '東京'
            },
            status=200
        )
        
        service = WeatherService("test_api_key")
        lat, lon, name = service._convert_postal_code_to_coordinates("1000001")
        
        assert lat == 35.6895
        assert lon == 139.6917
        assert name == '東京'
    
    @responses.activate
    def test_convert_postal_code_not_found(self):
        """郵便番号が見つからない（404エラー）"""
        responses.add(
            responses.GET,
            "http://api.openweathermap.org/geo/1.0/zip",
            json={'message': 'not found'},
            status=404
        )
        
        service = WeatherService("test_api_key")
        with pytest.raises(APIError, match="指定された郵便番号が見つかりませんでした"):
            service._convert_postal_code_to_coordinates("9999999")
    
    @responses.activate
    def test_convert_postal_code_invalid_api_key(self):
        """無効なAPIキー（401エラー）"""
        responses.add(
            responses.GET,
            "http://api.openweathermap.org/geo/1.0/zip",
            json={'message': 'Invalid API key'},
            status=401
        )
        
        service = WeatherService("invalid_key")
        with pytest.raises(APIError, match="無効なAPIキーです"):
            service._convert_postal_code_to_coordinates("1000001")
    
    @responses.activate
    def test_convert_postal_code_rate_limit(self):
        """レート制限超過（429エラー）"""
        responses.add(
            responses.GET,
            "http://api.openweathermap.org/geo/1.0/zip",
            json={'message': 'Rate limit exceeded'},
            status=429
        )
        
        service = WeatherService("test_api_key")
        with pytest.raises(APIError, match="APIレート制限を超えました"):
            service._convert_postal_code_to_coordinates("1000001")
    
    @responses.activate
    def test_convert_postal_code_server_error(self):
        """サーバーエラー（500エラー）"""
        responses.add(
            responses.GET,
            "http://api.openweathermap.org/geo/1.0/zip",
            json={'message': 'Internal server error'},
            status=500
        )
        
        service = WeatherService("test_api_key")
        with pytest.raises(APIError, match="天気サービスが一時的に利用できません"):
            service._convert_postal_code_to_coordinates("1000001")



class TestCurrentWeatherAPI:
    """Current Weather APIのテスト"""
    
    @responses.activate
    def test_fetch_current_weather_success(self):
        """現在の天気データ取得成功"""
        # Current Weather APIのモック
        responses.add(
            responses.GET,
            "https://api.openweathermap.org/data/2.5/weather",
            json={
                'main': {
                    'temp': 25.5
                }
            },
            status=200
        )
        
        # One Call APIのモック（降水確率用）
        responses.add(
            responses.GET,
            "https://api.openweathermap.org/data/3.0/onecall",
            json={
                'hourly': [
                    {'pop': 0.3}  # 30%
                ]
            },
            status=200
        )
        
        service = WeatherService("test_api_key")
        weather_data = service._fetch_current_weather(35.6895, 139.6917)
        
        assert weather_data['temperature'] == 25.5
        assert weather_data['precipitation_probability'] == 30.0
    
    @responses.activate
    def test_fetch_current_weather_without_precipitation(self):
        """降水確率なしの天気データ取得"""
        # Current Weather APIのモック
        responses.add(
            responses.GET,
            "https://api.openweathermap.org/data/2.5/weather",
            json={
                'main': {
                    'temp': 20.0
                }
            },
            status=200
        )
        
        # One Call APIが失敗する場合
        responses.add(
            responses.GET,
            "https://api.openweathermap.org/data/3.0/onecall",
            json={'message': 'error'},
            status=500
        )
        
        service = WeatherService("test_api_key")
        weather_data = service._fetch_current_weather(35.6895, 139.6917)
        
        assert weather_data['temperature'] == 20.0
        assert weather_data['precipitation_probability'] == 0.0


class TestWeatherAlerts:
    """気象警報のテスト"""
    
    @responses.activate
    def test_fetch_weather_alerts_with_alerts(self):
        """警報ありの場合"""
        responses.add(
            responses.GET,
            "https://api.openweathermap.org/data/3.0/onecall",
            json={
                'alerts': [
                    {
                        'event': 'Thunderstorm warning',
                        'description': '雷雨の警報が発令されています',
                        'tags': ['Severe']
                    },
                    {
                        'event': 'Heavy rain',
                        'description': '大雨の注意報が発令されています',
                        'tags': ['Moderate']
                    }
                ]
            },
            status=200
        )
        
        service = WeatherService("test_api_key")
        alerts = service._fetch_weather_alerts(35.6895, 139.6917)
        
        assert len(alerts) == 2
        assert alerts[0].alert_type == '雷'
        assert alerts[0].description == '雷雨の警報が発令されています'
        assert alerts[0].severity == 'Severe'
        assert alerts[1].alert_type == '大雨'
    
    @responses.activate
    def test_fetch_weather_alerts_no_alerts(self):
        """警報なしの場合"""
        responses.add(
            responses.GET,
            "https://api.openweathermap.org/data/3.0/onecall",
            json={},
            status=200
        )
        
        service = WeatherService("test_api_key")
        alerts = service._fetch_weather_alerts(35.6895, 139.6917)
        
        assert len(alerts) == 0
    
    @responses.activate
    def test_fetch_weather_alerts_api_error(self):
        """API呼び出しが失敗した場合は空のリストを返す"""
        responses.add(
            responses.GET,
            "https://api.openweathermap.org/data/3.0/onecall",
            json={'message': 'error'},
            status=500
        )
        
        service = WeatherService("test_api_key")
        alerts = service._fetch_weather_alerts(35.6895, 139.6917)
        
        assert len(alerts) == 0


class TestAlertTypeMapping:
    """警報タイプマッピングのテスト"""
    
    def test_map_thunderstorm(self):
        """雷雨のマッピング"""
        service = WeatherService("test_api_key")
        assert service._map_alert_type("thunderstorm warning") == "雷"
    
    def test_map_rain(self):
        """大雨のマッピング"""
        service = WeatherService("test_api_key")
        assert service._map_alert_type("heavy rain") == "大雨"
    
    def test_map_wind(self):
        """強風のマッピング"""
        service = WeatherService("test_api_key")
        assert service._map_alert_type("strong wind") == "強風"
    
    def test_map_snow(self):
        """雪のマッピング"""
        service = WeatherService("test_api_key")
        assert service._map_alert_type("heavy snow") == "雪"
    
    def test_map_fog(self):
        """濃霧のマッピング"""
        service = WeatherService("test_api_key")
        assert service._map_alert_type("dense fog") == "濃霧"
    
    def test_map_unknown_event(self):
        """未知のイベントはタイトルケースで返す"""
        service = WeatherService("test_api_key")
        assert service._map_alert_type("unknown event") == "Unknown Event"



class TestGetWeatherByPostalCode:
    """get_weather_by_postal_code統合テスト"""
    
    @responses.activate
    def test_get_weather_complete_flow(self):
        """完全なフローのテスト"""
        # Geocoding APIのモック
        responses.add(
            responses.GET,
            "http://api.openweathermap.org/geo/1.0/zip",
            json={
                'lat': 35.6895,
                'lon': 139.6917,
                'name': '東京'
            },
            status=200
        )
        
        # Current Weather APIのモック
        responses.add(
            responses.GET,
            "https://api.openweathermap.org/data/2.5/weather",
            json={
                'main': {
                    'temp': 22.5
                }
            },
            status=200
        )
        
        # One Call APIのモック（降水確率と警報用）
        responses.add(
            responses.GET,
            "https://api.openweathermap.org/data/3.0/onecall",
            json={
                'hourly': [
                    {'pop': 0.45}
                ]
            },
            status=200
        )
        
        # One Call APIのモック（警報用、2回目の呼び出し）
        responses.add(
            responses.GET,
            "https://api.openweathermap.org/data/3.0/onecall",
            json={
                'alerts': [
                    {
                        'event': 'Rain warning',
                        'description': '大雨警報',
                        'tags': ['Severe']
                    }
                ]
            },
            status=200
        )
        
        service = WeatherService("test_api_key")
        weather_data = service.get_weather_by_postal_code("1000001")
        
        assert weather_data.postal_code == "1000001"
        assert weather_data.temperature == 22.5
        assert weather_data.precipitation_probability == 45.0
        assert weather_data.location_name == '東京'
        assert len(weather_data.alerts) == 1
        assert weather_data.alerts[0].alert_type == '大雨'
    
    def test_get_weather_invalid_postal_code(self):
        """無効な郵便番号でエラー"""
        service = WeatherService("test_api_key")
        with pytest.raises(InvalidPostalCodeError):
            service.get_weather_by_postal_code("invalid")
