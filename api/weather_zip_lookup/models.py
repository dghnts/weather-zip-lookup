"""データモデルの定義"""

from dataclasses import dataclass


@dataclass
class WeatherAlert:
    """気象警報を表すデータクラス"""
    alert_type: str  # 熱波、寒波、強風、雪、濃霧、大雨、雷
    description: str
    severity: str  # 重要度レベル


@dataclass
class WeatherData:
    """天気データを表すデータクラス"""
    postal_code: str
    temperature: float  # 摂氏
    precipitation_probability: float  # パーセンテージ (0-100)
    alerts: list[WeatherAlert]
    location_name: str
