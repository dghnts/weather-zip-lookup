"""Weather Zip Lookup - 郵便番号から天気情報を取得するアプリケーション"""

import os
from flask import Flask


def create_app(config=None):
    """アプリケーションファクトリ
    
    Args:
        config: 設定辞書（オプション）
    
    Returns:
        Flask: 設定済みのFlaskアプリケーション
    """
    app = Flask(__name__)
    
    # デフォルト設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        OPENWEATHER_API_KEY=None,
        DEFAULT_POSTAL_CODE='',
    )
    
    # 環境変数から設定を読み込む
    if os.environ.get('OPENWEATHER_API_KEY'):
        app.config['OPENWEATHER_API_KEY'] = os.environ.get('OPENWEATHER_API_KEY')
    
    if os.environ.get('DEFAULT_POSTAL_CODE'):
        app.config['DEFAULT_POSTAL_CODE'] = os.environ.get('DEFAULT_POSTAL_CODE')
    
    # ローカル設定ファイルから読み込む（環境変数がない場合）
    if not app.config['OPENWEATHER_API_KEY'] or not app.config['DEFAULT_POSTAL_CODE']:
        try:
            from .config import ConfigManager
            config_manager = ConfigManager()
            
            if not app.config['OPENWEATHER_API_KEY']:
                app.config['OPENWEATHER_API_KEY'] = config_manager.get_api_key()
            
            if not app.config['DEFAULT_POSTAL_CODE']:
                app.config['DEFAULT_POSTAL_CODE'] = config_manager.get_default_postal_code() or ''
        except Exception:
            pass  # 設定ファイルがない場合は無視
    
    # カスタム設定を適用
    if config:
        app.config.from_mapping(config)
    
    # ルートを登録
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app


__version__ = '1.0.0'
