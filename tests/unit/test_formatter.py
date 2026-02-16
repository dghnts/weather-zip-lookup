"""OutputFormatterのユニットテスト"""

import pytest
from colorama import Fore, Back, Style
from weather_zip_lookup.formatter import OutputFormatter
from weather_zip_lookup.models import WeatherData, WeatherAlert


class TestOutputFormatter:
    """OutputFormatterクラスのテスト"""
    
    def test_format_weather_output_without_alerts(self):
        """警報がない場合の天気データフォーマットをテスト"""
        formatter = OutputFormatter()
        weather_data = WeatherData(
            postal_code="1000001",
            temperature=20.5,
            precipitation_probability=30.0,
            alerts=[],
            location_name="東京都千代田区"
        )
        
        output = formatter.format_weather_output(weather_data)
        
        # 基本的な要素が含まれているか確認
        assert "東京都千代田区" in output
        assert "1000001" in output
        assert "20.5°C" in output
        assert "30%" in output
        assert "気象警報" not in output
    
    def test_format_weather_output_with_alerts(self):
        """警報がある場合の天気データフォーマットをテスト"""
        formatter = OutputFormatter()
        alerts = [
            WeatherAlert(
                alert_type="大雨",
                description="大雨警報が発令されています",
                severity="高"
            )
        ]
        weather_data = WeatherData(
            postal_code="1000001",
            temperature=25.0,
            precipitation_probability=80.0,
            alerts=alerts,
            location_name="東京都千代田区"
        )
        
        output = formatter.format_weather_output(weather_data)
        
        # 警報情報が含まれているか確認
        assert "気象警報" in output
        assert "大雨" in output
        assert "大雨警報が発令されています" in output
        assert "高" in output
    
    def test_format_temperature_cold(self):
        """寒い気温（青色）のフォーマットをテスト"""
        formatter = OutputFormatter()
        result = formatter._format_temperature(5.0)
        
        assert "5.0°C" in result
        assert Fore.BLUE in result
    
    def test_format_temperature_comfortable(self):
        """快適な気温（緑色）のフォーマットをテスト"""
        formatter = OutputFormatter()
        result = formatter._format_temperature(20.0)
        
        assert "20.0°C" in result
        assert Fore.GREEN in result
    
    def test_format_temperature_hot(self):
        """暑い気温（赤色）のフォーマットをテスト"""
        formatter = OutputFormatter()
        result = formatter._format_temperature(30.0)
        
        assert "30.0°C" in result
        assert Fore.RED in result
    
    def test_format_precipitation_low(self):
        """低い降水確率（灰色）のフォーマットをテスト"""
        formatter = OutputFormatter()
        result = formatter._format_precipitation(20.0)
        
        assert "20%" in result
        assert Fore.LIGHTBLACK_EX in result
    
    def test_format_precipitation_medium(self):
        """中程度の降水確率（黄色）のフォーマットをテスト"""
        formatter = OutputFormatter()
        result = formatter._format_precipitation(50.0)
        
        assert "50%" in result
        assert Fore.YELLOW in result
    
    def test_format_precipitation_high(self):
        """高い降水確率（赤色）のフォーマットをテスト"""
        formatter = OutputFormatter()
        result = formatter._format_precipitation(80.0)
        
        assert "80%" in result
        assert Fore.RED in result
    
    def test_format_alerts_visual_emphasis(self):
        """気象警報の視覚的強調をテスト"""
        formatter = OutputFormatter()
        alerts = [
            WeatherAlert(
                alert_type="雷",
                description="雷注意報が発令されています",
                severity="中"
            )
        ]
        
        result = formatter._format_alerts(alerts)
        
        # 赤背景と警告アイコンが含まれているか確認
        assert Back.RED in result
        assert "⚠" in result
        assert "雷" in result
        assert "雷注意報が発令されています" in result
    
    def test_format_multiple_alerts(self):
        """複数の気象警報のフォーマットをテスト"""
        formatter = OutputFormatter()
        alerts = [
            WeatherAlert(
                alert_type="大雨",
                description="大雨警報",
                severity="高"
            ),
            WeatherAlert(
                alert_type="強風",
                description="強風注意報",
                severity="中"
            )
        ]
        
        result = formatter._format_alerts(alerts)
        
        assert "大雨" in result
        assert "強風" in result
        assert "大雨警報" in result
        assert "強風注意報" in result
    
    def test_extreme_temperature_values(self):
        """極端な気温値のフォーマットをテスト"""
        formatter = OutputFormatter()
        
        # 極寒
        result_cold = formatter._format_temperature(-20.0)
        assert "-20.0°C" in result_cold
        assert Fore.BLUE in result_cold
        
        # 極暑
        result_hot = formatter._format_temperature(40.0)
        assert "40.0°C" in result_hot
        assert Fore.RED in result_hot
    
    def test_boundary_temperature_values(self):
        """境界値の気温のフォーマットをテスト"""
        formatter = OutputFormatter()
        
        # 10度（境界値）
        result_10 = formatter._format_temperature(10.0)
        assert "10.0°C" in result_10
        assert Fore.GREEN in result_10
        
        # 25度（境界値）
        result_25 = formatter._format_temperature(25.0)
        assert "25.0°C" in result_25
        assert Fore.RED in result_25
    
    def test_boundary_precipitation_values(self):
        """境界値の降水確率のフォーマットをテスト"""
        formatter = OutputFormatter()
        
        # 30%（境界値）
        result_30 = formatter._format_precipitation(30.0)
        assert "30%" in result_30
        assert Fore.YELLOW in result_30
        
        # 70%（境界値）
        result_70 = formatter._format_precipitation(70.0)
        assert "70%" in result_70
        assert Fore.RED in result_70
