"""WSGI エントリーポイント - Vercelデプロイ用"""

from weather_zip_lookup import create_app

app = create_app()
