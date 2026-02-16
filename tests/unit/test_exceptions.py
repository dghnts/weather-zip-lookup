"""例外クラスのユニットテスト"""

import pytest
from weather_zip_lookup.exceptions import (
    WeatherScriptError,
    NetworkError,
    APIError,
    InvalidPostalCodeError,
    ConfigError,
    MissingAPIKeyError
)


def test_network_error_inheritance():
    """NetworkErrorがWeatherScriptErrorを継承していることを確認"""
    error = NetworkError("ネットワークエラー")
    assert isinstance(error, WeatherScriptError)
    assert isinstance(error, Exception)


def test_api_error_inheritance():
    """APIErrorがWeatherScriptErrorを継承していることを確認"""
    error = APIError("APIエラー")
    assert isinstance(error, WeatherScriptError)


def test_invalid_postal_code_error_inheritance():
    """InvalidPostalCodeErrorがWeatherScriptErrorを継承していることを確認"""
    error = InvalidPostalCodeError("無効な郵便番号")
    assert isinstance(error, WeatherScriptError)


def test_config_error_inheritance():
    """ConfigErrorがWeatherScriptErrorを継承していることを確認"""
    error = ConfigError("設定エラー")
    assert isinstance(error, WeatherScriptError)


def test_missing_api_key_error_inheritance():
    """MissingAPIKeyErrorがWeatherScriptErrorを継承していることを確認"""
    error = MissingAPIKeyError("APIキーが見つかりません")
    assert isinstance(error, WeatherScriptError)


def test_exception_messages():
    """例外メッセージが正しく設定されることを確認"""
    message = "テストメッセージ"
    error = NetworkError(message)
    assert str(error) == message
