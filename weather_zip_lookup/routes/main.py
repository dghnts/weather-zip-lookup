"""メインルート - Webアプリケーションのエンドポイント"""

from flask import Blueprint, render_template, request, jsonify, current_app
from weather_zip_lookup.services import WeatherService
from weather_zip_lookup.exceptions import (
    InvalidPostalCodeError,
    APIError,
    NetworkError,
    MissingAPIKeyError
)

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """メインページ"""
    default_postal_code = current_app.config.get('DEFAULT_POSTAL_CODE', '')
    return render_template('index.html', default_postal_code=default_postal_code)


@bp.route('/api/weather', methods=['POST'])
def get_weather():
    """天気情報を取得するAPIエンドポイント"""
    try:
        # 郵便番号を取得
        postal_code = request.json.get('postal_code', '').strip()
        
        if not postal_code:
            postal_code = current_app.config.get('DEFAULT_POSTAL_CODE')
            if not postal_code:
                return jsonify({
                    'error': '郵便番号が指定されていません'
                }), 400
        
        # APIキーを取得
        api_key = current_app.config.get('OPENWEATHER_API_KEY')
        if not api_key:
            return jsonify({
                'error': 'APIキーが設定されていません'
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
