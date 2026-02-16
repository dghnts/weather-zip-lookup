"""
天気情報取得Webアプリケーション

スマホのブラウザからアクセスして天気情報を確認できます。
"""

from flask import Flask, render_template, request, jsonify
from weather_zip_lookup.config import ConfigManager
from weather_zip_lookup.weather_service import WeatherService
from weather_zip_lookup.exceptions import (
    InvalidPostalCodeError,
    APIError,
    NetworkError,
    MissingAPIKeyError
)

app = Flask(__name__)

# 設定マネージャーを初期化
config_manager = ConfigManager()


@app.route('/')
def index():
    """メインページ"""
    default_postal_code = config_manager.get_default_postal_code() or ""
    return render_template('index.html', default_postal_code=default_postal_code)


@app.route('/api/weather', methods=['POST'])
def get_weather():
    """天気情報を取得するAPIエンドポイント"""
    try:
        # 郵便番号を取得
        postal_code = request.json.get('postal_code', '').strip()
        
        if not postal_code:
            postal_code = config_manager.get_default_postal_code()
            if not postal_code:
                return jsonify({
                    'error': '郵便番号が指定されていません'
                }), 400
        
        # APIキーを取得
        api_key = config_manager.get_api_key()
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


if __name__ == '__main__':
    print("=" * 60)
    print("天気情報Webアプリを起動しています...")
    print("=" * 60)
    print()
    print("スマホからアクセスするには:")
    print("1. PCとスマホを同じWi-Fiに接続")
    print("2. スマホのブラウザで以下のURLにアクセス:")
    print("   http://<PCのIPアドレス>:5000")
    print()
    print("ローカルでテストする場合:")
    print("   http://localhost:5000")
    print()
    print("=" * 60)
    
    # 0.0.0.0でバインドすることで、同じネットワーク内の他のデバイスからアクセス可能
    app.run(host='0.0.0.0', port=5000, debug=True)
