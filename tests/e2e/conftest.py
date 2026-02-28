"""Playwright E2Eテスト用のフィクスチャ"""

import pytest
from unittest.mock import patch
from weather_zip_lookup.models import WeatherData, WeatherAlert
import sys
import os
from pathlib import Path

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


@pytest.fixture
def mock_weather_service():
    """WeatherServiceをモック化"""
    mock_weather_data = WeatherData(
        postal_code="1000001",
        temperature=22.5,
        precipitation_probability=35.0,
        alerts=[
            WeatherAlert(
                alert_type="大雨警報",
                description="大雨警報が発令されています",
                severity="高"
            )
        ],
        location_name="東京都千代田区"
    )
    
    with patch('weather_zip_lookup.services.weather_service.WeatherService') as mock_service:
        mock_service_instance = mock_service.return_value
        mock_service_instance.get_weather_by_postal_code.return_value = mock_weather_data
        yield mock_service


@pytest.fixture
def flask_app(mock_weather_service):
    """テスト用のFlaskアプリ"""
    from weather_zip_lookup import create_app
    
    app = create_app({
        'TESTING': True,
        'OPENWEATHER_API_KEY': 'test_api_key',
        'DEFAULT_POSTAL_CODE': '1000001'
    })
    
    return app


@pytest.fixture
def flask_server(flask_app):
    """Flaskサーバーを起動"""
    import threading
    import time
    
    def run_server():
        flask_app.run(host='127.0.0.1', port=5555, debug=False, use_reloader=False)
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    time.sleep(2)  # サーバー起動を待つ
    
    yield "http://127.0.0.1:5555"


# スクリーンショットと動画の保存ディレクトリを設定
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """ブラウザコンテキストの設定"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "record_video_dir": "test-results/videos/",
        "record_video_size": {"width": 1280, "height": 720}
    }


@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(request, page):
    """テスト失敗時に自動的にスクリーンショットを保存"""
    yield
    if request.node.rep_call.failed:
        screenshot_dir = Path("test-results/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path))
        print(f"\nスクリーンショット保存: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """テスト結果を取得するためのフック"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
