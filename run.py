#!/usr/bin/env python3
"""開発サーバー起動スクリプト"""

from weather_zip_lookup import create_app

if __name__ == '__main__':
    app = create_app()
    
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
