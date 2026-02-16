"""OutputFormatterのデモンストレーション"""

from weather_zip_lookup.formatter import OutputFormatter
from weather_zip_lookup.models import WeatherData, WeatherAlert


def demo_without_alerts():
    """警報なしの天気データをデモ"""
    print("\n=== デモ1: 警報なしの天気データ ===\n")
    
    formatter = OutputFormatter()
    weather_data = WeatherData(
        postal_code="1000001",
        temperature=22.5,
        precipitation_probability=35.0,
        alerts=[],
        location_name="東京都千代田区"
    )
    
    output = formatter.format_weather_output(weather_data)
    print(output)


def demo_with_alerts():
    """警報ありの天気データをデモ"""
    print("\n=== デモ2: 警報ありの天気データ ===\n")
    
    formatter = OutputFormatter()
    alerts = [
        WeatherAlert(
            alert_type="大雨",
            description="大雨警報が発令されています。低地の浸水、河川の増水に注意してください。",
            severity="高"
        ),
        WeatherAlert(
            alert_type="雷",
            description="雷注意報が発令されています。落雷に注意してください。",
            severity="中"
        )
    ]
    weather_data = WeatherData(
        postal_code="5400001",
        temperature=28.0,
        precipitation_probability=85.0,
        alerts=alerts,
        location_name="大阪府大阪市"
    )
    
    output = formatter.format_weather_output(weather_data)
    print(output)


def demo_temperature_colors():
    """気温の色分けをデモ"""
    print("\n=== デモ3: 気温の色分け ===\n")
    
    formatter = OutputFormatter()
    
    # 寒い（青）
    weather_cold = WeatherData(
        postal_code="0600001",
        temperature=5.0,
        precipitation_probability=20.0,
        alerts=[],
        location_name="北海道札幌市"
    )
    print(formatter.format_weather_output(weather_cold))
    
    print("\n")
    
    # 快適（緑）
    weather_comfortable = WeatherData(
        postal_code="1000001",
        temperature=18.0,
        precipitation_probability=10.0,
        alerts=[],
        location_name="東京都千代田区"
    )
    print(formatter.format_weather_output(weather_comfortable))
    
    print("\n")
    
    # 暑い（赤）
    weather_hot = WeatherData(
        postal_code="9000001",
        temperature=35.0,
        precipitation_probability=5.0,
        alerts=[],
        location_name="沖縄県那覇市"
    )
    print(formatter.format_weather_output(weather_hot))


if __name__ == "__main__":
    demo_without_alerts()
    demo_with_alerts()
    demo_temperature_colors()
