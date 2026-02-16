"""
Vercel用のエントリーポイント

環境変数からAPIキーを読み取り、Vercelのサーバーレス環境で動作します。
"""

import os
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, render_template, request, jsonify
from weather_zip_lookup.weather_service import WeatherService
from weather_zip_lookup.exceptions import (
    InvalidPostalCodeError,
    APIError,
    NetworkError,
    MissingAPIKeyError
)

app = Flask(__name__, template_folder='../templates')


@app.route('/')
def index():
    """メインページ"""
    # Vercelでは環境変数からデフォルト郵便番号を取得
    default_postal_code = os.environ.get('DEFAULT_POSTAL_CODE', '1000001')
    return render_template('index.html', default_postal_code=default_postal_code)


@app.route('/api/weather', methods=['POST'])
def get_weather():
    """天気情報を取得するAPIエンドポイント"""
    try:
        # 郵便番号を取得
        postal_code = request.json.get('postal_code', '').strip()
        
        if not postal_code:
            # デフォルト郵便番号を使用
            postal_code = os.environ.get('DEFAULT_POSTAL_CODE', '1000001')
        
        # 環境変数からAPIキーを取得
        api_key = os.environ.get('OPENWEATHER_API_KEY')
        if not api_key:
            return jsonify({
                'error': 'APIキーが設定されていません。管理者に連絡してください。'
            }), 500
        
        # 天気データを取得
        weather_service = WeatherService(api_key)
        weather_data = weather_service.get_weather_by_postal_code(postal_code)
        
        # レスポンスを構築
        return jsonify({
            'success': True,
            'data': {
                'postal_code': weather_data.postal_code,
                'location_name': weather_data.location_name,
                'temperature': weather_data.temperature,
                'precipitation_probability': weather_data.precipitation_probability,
                'alerts': [
                    {
                        'alert_type': alert.alert_type,
                        'description': alert.description,
                        'severity': alert.severity
                    }
                    for alert in weather_data.alerts
                ]
            }
        })
        
    except InvalidPostalCodeError as e:
        return jsonify({'error': str(e)}), 400
    except (APIError, NetworkError, MissingAPIKeyError) as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'予期しないエラーが発生しました: {str(e)}'}), 500


# Vercel用のハンドラー
def handler(request):
    """Vercelのサーバーレス関数ハンドラー"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()
