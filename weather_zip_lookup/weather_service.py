"""天気データを取得するサービスクラス"""

import re
import requests
from typing import Optional

from .models import WeatherData, WeatherAlert
from .exceptions import (
    InvalidPostalCodeError,
    APIError,
    NetworkError,
    MissingAPIKeyError
)


class WeatherService:
    """天気データを取得するサービスクラス"""
    
    # API エンドポイント
    GEOCODING_API_URL = "http://api.openweathermap.org/geo/1.0/zip"
    CURRENT_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
    ONE_CALL_API_URL = "https://api.openweathermap.org/data/3.0/onecall"
    
    # 郵便番号の正規表現パターン（7桁の数字）
    POSTAL_CODE_PATTERN = re.compile(r'^\d{7}$')
    
    # 警報イベントのマッピング
    ALERT_TYPE_MAPPING = {
        'extreme temperature': '熱波/寒波',
        'heat': '熱波',
        'cold': '寒波',
        'wind': '強風',
        'snow': '雪',
        'fog': '濃霧',
        'rain': '大雨',
        'thunderstorm': '雷',
    }
    
    def __init__(self, api_key: str):
        """
        Args:
            api_key: OpenWeatherMap APIキー
        
        Raises:
            MissingAPIKeyError: APIキーが空または無効な場合
        """
        if not api_key or not api_key.strip():
            raise MissingAPIKeyError("APIキーが設定されていません。OpenWeatherMapからAPIキーを取得してください。")
        self.api_key = api_key.strip()
    
    def get_weather_by_postal_code(self, postal_code: str) -> WeatherData:
        """
        郵便番号から天気データを取得
        
        Args:
            postal_code: 7桁の日本の郵便番号
            
        Returns:
            天気データを含むWeatherDataオブジェクト
            
        Raises:
            InvalidPostalCodeError: 郵便番号が無効な場合
            APIError: API呼び出しが失敗した場合
            NetworkError: ネットワーク接続が失敗した場合
        """
        # 郵便番号の検証
        self._validate_postal_code(postal_code)
        
        # 郵便番号を緯度経度に変換
        lat, lon, location_name = self._convert_postal_code_to_coordinates(postal_code)
        
        # 現在の天気データを取得
        weather_data = self._fetch_current_weather(lat, lon)
        
        # 気象警報を取得
        alerts = self._fetch_weather_alerts(lat, lon)
        
        # WeatherDataオブジェクトを構築
        return WeatherData(
            postal_code=postal_code,
            temperature=weather_data['temperature'],
            precipitation_probability=weather_data['precipitation_probability'],
            alerts=alerts,
            location_name=location_name
        )

    def _validate_postal_code(self, postal_code: str) -> None:
        """
        郵便番号の形式を検証
        
        Args:
            postal_code: 検証する郵便番号
            
        Raises:
            InvalidPostalCodeError: 郵便番号が無効な場合
        """
        if not postal_code or not isinstance(postal_code, str):
            raise InvalidPostalCodeError("無効な郵便番号形式です。7桁の数字を入力してください。")
        
        if not self.POSTAL_CODE_PATTERN.match(postal_code):
            raise InvalidPostalCodeError("無効な郵便番号形式です。7桁の数字を入力してください。")
    
    def _convert_postal_code_to_coordinates(self, postal_code: str) -> tuple[float, float, str]:
        """
        郵便番号を緯度経度に変換
        
        Args:
            postal_code: 7桁の日本の郵便番号
            
        Returns:
            (緯度, 経度, 地名)のタプル
            
        Raises:
            APIError: API呼び出しが失敗した場合
            NetworkError: ネットワーク接続が失敗した場合
        """
        params = {
            'zip': f'{postal_code},JP',
            'appid': self.api_key
        }
        
        try:
            response = requests.get(
                self.GEOCODING_API_URL,
                params=params,
                timeout=10
            )
            
            # HTTPステータスコードのチェック
            if response.status_code == 401:
                raise APIError("無効なAPIキーです。設定を確認してください。")
            elif response.status_code == 404:
                raise APIError("指定された郵便番号が見つかりませんでした。")
            elif response.status_code == 429:
                raise APIError("APIレート制限を超えました。しばらく待ってから再試行してください。")
            elif 500 <= response.status_code < 600:
                raise APIError("天気サービスが一時的に利用できません。後でもう一度お試しください。")
            
            response.raise_for_status()
            
            data = response.json()
            return data['lat'], data['lon'], data.get('name', '不明')
            
        except requests.exceptions.Timeout:
            raise NetworkError("ネットワーク接続に失敗しました。インターネット接続を確認してください。")
        except requests.exceptions.ConnectionError:
            raise NetworkError("ネットワーク接続に失敗しました。インターネット接続を確認してください。")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"ネットワーク接続に失敗しました: {str(e)}")
        except (KeyError, ValueError) as e:
            raise APIError(f"APIレスポンスの解析に失敗しました: {str(e)}")

    def _fetch_current_weather(self, lat: float, lon: float) -> dict:
        """
        現在の天気データを取得
        
        Args:
            lat: 緯度
            lon: 経度
            
        Returns:
            temperature と precipitation_probability を含む辞書
            
        Raises:
            APIError: API呼び出しが失敗した場合
            NetworkError: ネットワーク接続が失敗した場合
        """
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',  # 摂氏
            'lang': 'ja'
        }
        
        try:
            response = requests.get(
                self.CURRENT_WEATHER_API_URL,
                params=params,
                timeout=10
            )
            
            # HTTPステータスコードのチェック
            if response.status_code == 401:
                raise APIError("無効なAPIキーです。設定を確認してください。")
            elif response.status_code == 404:
                raise APIError("指定された場所の天気データが見つかりませんでした。")
            elif response.status_code == 429:
                raise APIError("APIレート制限を超えました。しばらく待ってから再試行してください。")
            elif 500 <= response.status_code < 600:
                raise APIError("天気サービスが一時的に利用できません。後でもう一度お試しください。")
            
            response.raise_for_status()
            
            data = response.json()
            
            # 気温を取得
            temperature = data['main']['temp']
            
            # 降水確率を取得（Current Weather APIには含まれていないため、0をデフォルトとする）
            # 実際の降水確率はOne Call APIから取得する必要がある
            precipitation_probability = 0.0
            
            # One Call APIから降水確率を取得
            try:
                onecall_data = self._fetch_onecall_data(lat, lon)
                if 'hourly' in onecall_data and len(onecall_data['hourly']) > 0:
                    # 次の1時間の降水確率を取得
                    precipitation_probability = onecall_data['hourly'][0].get('pop', 0.0) * 100
            except Exception:
                # One Call APIが失敗しても、現在の天気データは返す
                pass
            
            return {
                'temperature': temperature,
                'precipitation_probability': precipitation_probability
            }
            
        except requests.exceptions.Timeout:
            raise NetworkError("ネットワーク接続に失敗しました。インターネット接続を確認してください。")
        except requests.exceptions.ConnectionError:
            raise NetworkError("ネットワーク接続に失敗しました。インターネット接続を確認してください。")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"ネットワーク接続に失敗しました: {str(e)}")
        except (KeyError, ValueError) as e:
            raise APIError(f"APIレスポンスの解析に失敗しました: {str(e)}")

    def _fetch_onecall_data(self, lat: float, lon: float) -> dict:
        """
        One Call APIからデータを取得（降水確率用）
        
        Args:
            lat: 緯度
            lon: 経度
            
        Returns:
            One Call APIのレスポンス辞書
            
        Raises:
            APIError: API呼び出しが失敗した場合
            NetworkError: ネットワーク接続が失敗した場合
        """
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'exclude': 'minutely,daily',
            'units': 'metric',
            'lang': 'ja'
        }
        
        try:
            response = requests.get(
                self.ONE_CALL_API_URL,
                params=params,
                timeout=10
            )
            
            # HTTPステータスコードのチェック
            if response.status_code == 401:
                raise APIError("無効なAPIキーです。設定を確認してください。")
            elif response.status_code == 404:
                raise APIError("指定された場所のデータが見つかりませんでした。")
            elif response.status_code == 429:
                raise APIError("APIレート制限を超えました。しばらく待ってから再試行してください。")
            elif 500 <= response.status_code < 600:
                raise APIError("天気サービスが一時的に利用できません。後でもう一度お試しください。")
            
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise NetworkError("ネットワーク接続に失敗しました。インターネット接続を確認してください。")
        except requests.exceptions.ConnectionError:
            raise NetworkError("ネットワーク接続に失敗しました。インターネット接続を確認してください。")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"ネットワーク接続に失敗しました: {str(e)}")

    def _fetch_weather_alerts(self, lat: float, lon: float) -> list[WeatherAlert]:
        """
        気象警報データを取得
        
        Args:
            lat: 緯度
            lon: 経度
            
        Returns:
            警報データのリスト
            
        Raises:
            APIError: API呼び出しが失敗した場合
            NetworkError: ネットワーク接続が失敗した場合
        """
        try:
            # One Call APIから警報データを取得
            onecall_data = self._fetch_onecall_data(lat, lon)
            
            alerts = []
            if 'alerts' in onecall_data:
                for alert_data in onecall_data['alerts']:
                    # 警報イベントを日本語にマッピング
                    event = alert_data.get('event', '').lower()
                    alert_type = self._map_alert_type(event)
                    
                    alert = WeatherAlert(
                        alert_type=alert_type,
                        description=alert_data.get('description', ''),
                        severity=alert_data.get('tags', ['不明'])[0] if alert_data.get('tags') else '不明'
                    )
                    alerts.append(alert)
            
            return alerts
            
        except (APIError, NetworkError):
            # API呼び出しが失敗した場合は空のリストを返す
            # 警報データは必須ではないため
            return []
        except Exception:
            # その他のエラーも空のリストを返す
            return []
    
    def _map_alert_type(self, event: str) -> str:
        """
        警報イベントを日本語の警報タイプにマッピング
        
        Args:
            event: 警報イベント名（英語、小文字）
            
        Returns:
            日本語の警報タイプ
        """
        # 部分一致で検索
        for key, value in self.ALERT_TYPE_MAPPING.items():
            if key in event:
                return value
        
        # マッピングが見つからない場合は元のイベント名を返す
        return event.title()
