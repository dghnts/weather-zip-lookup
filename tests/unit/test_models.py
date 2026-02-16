"""データモデルのユニットテスト"""

from weather_zip_lookup.models import WeatherData, WeatherAlert


def test_weather_alert_creation():
    """WeatherAlertが正しく作成されることを確認"""
    alert = WeatherAlert(
        alert_type="大雨",
        description="大雨警報が発令されています",
        severity="high"
    )
    assert alert.alert_type == "大雨"
    assert alert.description == "大雨警報が発令されています"
    assert alert.severity == "high"


def test_weather_data_creation():
    """WeatherDataが正しく作成されることを確認"""
    alert = WeatherAlert(
        alert_type="強風",
        description="強風注意報",
        severity="medium"
    )
    weather = WeatherData(
        postal_code="1000001",
        temperature=25.5,
        precipitation_probability=30.0,
        alerts=[alert],
        location_name="東京都千代田区"
    )
    assert weather.postal_code == "1000001"
    assert weather.temperature == 25.5
    assert weather.precipitation_probability == 30.0
    assert len(weather.alerts) == 1
    assert weather.location_name == "東京都千代田区"


def test_weather_data_no_alerts():
    """警報がない場合のWeatherDataを確認"""
    weather = WeatherData(
        postal_code="1000001",
        temperature=20.0,
        precipitation_probability=10.0,
        alerts=[],
        location_name="東京都千代田区"
    )
    assert len(weather.alerts) == 0
