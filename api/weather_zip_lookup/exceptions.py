"""カスタム例外クラスの定義"""


class WeatherScriptError(Exception):
    """Weather Scriptの基底例外クラス"""
    pass


class NetworkError(WeatherScriptError):
    """ネットワーク接続エラー"""
    pass


class APIError(WeatherScriptError):
    """API呼び出しエラー"""
    pass


class InvalidPostalCodeError(WeatherScriptError):
    """無効な郵便番号形式エラー"""
    pass


class ConfigError(WeatherScriptError):
    """設定ファイルエラー"""
    pass


class MissingAPIKeyError(WeatherScriptError):
    """APIキー欠落エラー"""
    pass
