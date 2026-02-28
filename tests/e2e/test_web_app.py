"""Playwright E2Eテスト"""

import pytest
from playwright.sync_api import Page, expect
from pathlib import Path


# スクリーンショット保存用のヘルパー関数
def save_screenshot(page: Page, test_name: str, step: str):
    """スクリーンショットを保存"""
    screenshot_dir = Path("test-results/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshot_dir / f"{test_name}_{step}.png"
    page.screenshot(path=str(screenshot_path))
    print(f"\nスクリーンショット保存: {screenshot_path}")


def test_page_loads(page: Page, flask_server):
    """ページが正常に読み込まれることを確認"""
    page.goto(flask_server)
    save_screenshot(page, "test_page_loads", "01_initial_load")
    
    # タイトルを確認
    expect(page).to_have_title("天気情報 - Weather Zip Lookup")
    
    # ヘッダーを確認
    header = page.locator("h1")
    expect(header).to_contain_text("天気情報")
    save_screenshot(page, "test_page_loads", "02_header_verified")


def test_postal_code_input_exists(page: Page, flask_server):
    """郵便番号入力フィールドが存在することを確認"""
    page.goto(flask_server)
    
    # 入力フィールドを確認
    postal_input = page.locator("#postal_code")
    expect(postal_input).to_be_visible()
    expect(postal_input).to_have_attribute("placeholder", "例: 1000001")


def test_submit_button_exists(page: Page, flask_server):
    """天気取得ボタンが存在することを確認"""
    page.goto(flask_server)
    
    # ボタンを確認
    button = page.locator("button.btn")
    expect(button).to_be_visible()
    expect(button).to_contain_text("天気を取得")


def test_invalid_postal_code_validation(page: Page, flask_server):
    """無効な郵便番号のバリデーション"""
    page.goto(flask_server)
    save_screenshot(page, "test_invalid_postal_code", "01_initial_page")
    
    # 無効な郵便番号を入力
    page.fill("#postal_code", "123")
    save_screenshot(page, "test_invalid_postal_code", "02_invalid_input")
    page.click("button.btn")
    
    # エラーメッセージを確認
    error = page.locator("#error")
    expect(error).to_be_visible()
    expect(error).to_contain_text("郵便番号は7桁の数字で入力してください")
    save_screenshot(page, "test_invalid_postal_code", "03_error_displayed")


def test_get_weather_flow(page: Page, flask_server):
    """天気情報取得の完全なフロー"""
    page.goto(flask_server)
    save_screenshot(page, "test_get_weather_flow", "01_initial_page")
    
    # 郵便番号を入力
    page.fill("#postal_code", "1000001")
    save_screenshot(page, "test_get_weather_flow", "02_postal_code_entered")
    
    # ボタンをクリック
    page.click("button.btn")
    save_screenshot(page, "test_get_weather_flow", "03_button_clicked")
    
    # 結果が表示されるまで待つ
    result = page.locator("#result")
    expect(result).to_be_visible(timeout=10000)
    save_screenshot(page, "test_get_weather_flow", "04_result_displayed")
    
    # 地名を確認
    location = page.locator("#location")
    expect(location).to_contain_text("東京都千代田区")
    
    # 郵便番号を確認
    postal_display = page.locator("#postal-code-display")
    expect(postal_display).to_contain_text("1000001")
    
    # 気温を確認
    temperature = page.locator("#temperature")
    expect(temperature).to_be_visible()
    
    # 降水確率を確認
    precipitation = page.locator("#precipitation")
    expect(precipitation).to_contain_text("降水確率")
    save_screenshot(page, "test_get_weather_flow", "05_all_data_verified")


def test_weather_alerts_display(page: Page, flask_server):
    """気象警報が表示されることを確認"""
    page.goto(flask_server)
    
    # 郵便番号を入力して天気を取得
    page.fill("#postal_code", "1000001")
    page.click("button.btn")
    
    # 結果が表示されるまで待つ
    result = page.locator("#result")
    expect(result).to_be_visible(timeout=10000)
    save_screenshot(page, "test_weather_alerts", "01_result_with_alerts")
    
    # 警報を確認
    alerts = page.locator("#alerts .alert-item")
    expect(alerts.first).to_be_visible()
    
    # 警報タイプを確認
    alert_type = page.locator(".alert-type")
    expect(alert_type.first).to_contain_text("大雨警報")
    save_screenshot(page, "test_weather_alerts", "02_alert_verified")


def test_enter_key_submission(page: Page, flask_server):
    """Enterキーで送信できることを確認"""
    page.goto(flask_server)
    
    # 郵便番号を入力してEnterキーを押す
    postal_input = page.locator("#postal_code")
    postal_input.fill("1000001")
    postal_input.press("Enter")
    
    # 結果が表示されることを確認
    result = page.locator("#result")
    expect(result).to_be_visible(timeout=10000)


def test_responsive_design(page: Page, flask_server):
    """レスポンシブデザインの確認（モバイルビュー）"""
    # モバイルサイズに設定
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(flask_server)
    save_screenshot(page, "test_responsive_design", "01_mobile_view")
    
    # 要素が表示されることを確認
    header = page.locator("h1")
    expect(header).to_be_visible()
    
    postal_input = page.locator("#postal_code")
    expect(postal_input).to_be_visible()
    
    button = page.locator("button.btn")
    expect(button).to_be_visible()
    
    # 天気情報を取得してモバイルでの表示を確認
    page.fill("#postal_code", "1000001")
    page.click("button.btn")
    result = page.locator("#result")
    expect(result).to_be_visible(timeout=10000)
    save_screenshot(page, "test_responsive_design", "02_mobile_with_results")
