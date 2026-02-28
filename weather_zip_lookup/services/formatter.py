"""出力フォーマッターの実装"""

from colorama import Fore, Back, Style, init
from ..models import WeatherData, WeatherAlert

# coloramaの初期化（クロスプラットフォーム対応）
init(autoreset=True)


class OutputFormatter:
    """出力をフォーマットするクラス"""
    
    def format_weather_output(self, weather_data: WeatherData) -> str:
        """
        天気データをフォーマット
        
        Args:
            weather_data: 表示する天気データ
            
        Returns:
            フォーマットされた文字列
        """
        lines = []
        
        # ヘッダー
        lines.append("=" * 50)
        lines.append(f"天気情報 - {weather_data.location_name} (郵便番号: {weather_data.postal_code})")
        lines.append("=" * 50)
        lines.append("")
        
        # 気温
        temp_formatted = self._format_temperature(weather_data.temperature)
        lines.append(f"気温: {temp_formatted}")
        
        # 降水確率
        precip_formatted = self._format_precipitation(weather_data.precipitation_probability)
        lines.append(f"降水確率: {precip_formatted}")
        
        # 気象警報
        if weather_data.alerts:
            lines.append("")
            alerts_formatted = self._format_alerts(weather_data.alerts)
            lines.append(alerts_formatted)
        
        lines.append("")
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def _format_temperature(self, temp: float) -> str:
        """
        気温をフォーマット
        
        Args:
            temp: 気温（摂氏）
            
        Returns:
            色付きでフォーマットされた気温文字列
        """
        # 色分け: 青（寒い）、緑（快適）、赤（暑い）
        if temp < 10:
            color = Fore.BLUE
        elif temp < 25:
            color = Fore.GREEN
        else:
            color = Fore.RED
        
        return f"{color}{temp:.1f}°C{Style.RESET_ALL}"
    
    def _format_precipitation(self, probability: float) -> str:
        """
        降水確率をフォーマット
        
        Args:
            probability: 降水確率（パーセンテージ 0-100）
            
        Returns:
            色付きでフォーマットされた降水確率文字列
        """
        # 色分け: 灰色（低）、黄色（中）、赤（高）
        if probability < 30:
            color = Fore.LIGHTBLACK_EX
        elif probability < 70:
            color = Fore.YELLOW
        else:
            color = Fore.RED
        
        return f"{color}{probability:.0f}%{Style.RESET_ALL}"
    
    def _format_alerts(self, alerts: list[WeatherAlert]) -> str:
        """
        気象警報をフォーマット
        
        Args:
            alerts: 気象警報のリスト
            
        Returns:
            色付きでフォーマットされた警報文字列
        """
        lines = []
        lines.append(f"{Back.RED}{Fore.WHITE}⚠ 気象警報 ⚠{Style.RESET_ALL}")
        lines.append("")
        
        for alert in alerts:
            # 警報の種類と説明を赤背景で強調
            lines.append(f"{Fore.RED}【{alert.alert_type}】{Style.RESET_ALL}")
            lines.append(f"  {alert.description}")
            lines.append(f"  重要度: {alert.severity}")
            lines.append("")
        
        return "\n".join(lines)
