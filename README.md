# Weather Zip Lookup

郵便番号から天気情報を取得するWebアプリケーション

## 機能

- 📍 郵便番号から天気情報を取得
- 🌡️ 気温の色分け表示（青/緑/赤）
- 💧 降水確率の色分け表示
- ⚠️ 気象警報の視覚的強調表示
- 📱 スマホ対応のレスポンシブデザイン

## ローカルで実行

### 必要なもの

- Python 3.8以上
- OpenWeatherMap APIキー（[こちら](https://openweathermap.org/api)から無料で取得）

### インストール

```bash
# 依存パッケージをインストール
pip install -r requirements.txt

# 設定ファイルを作成
# Windows: C:\Users\<ユーザー名>\AppData\Roaming\weather-zip-lookup\config.json
# Mac/Linux: ~/.config/weather-zip-lookup/config.json

# config.jsonの内容:
{
  "default_postal_code": "1000001",
  "api_key": "your_openweather_api_key_here"
}
```

### CLIで実行

```bash
# デフォルト郵便番号で実行
python weather.py

# 郵便番号を指定して実行
python weather.py 1000001

# ヘルプを表示
python weather.py -h
```

### Webアプリで実行

```bash
# Webサーバーを起動
python web_app.py

# ブラウザでアクセス
# http://localhost:5000
```

## Vercelにデプロイ

### 1. GitHubリポジトリを作成

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/weather-zip-lookup.git
git push -u origin main
```

### 2. Vercelでデプロイ

1. [Vercel](https://vercel.com)にアクセスしてログイン
2. 「New Project」をクリック
3. GitHubリポジトリを選択
4. 「Deploy」をクリック

### 3. 環境変数を設定

Vercelのプロジェクト設定で以下の環境変数を追加：

- `OPENWEATHER_API_KEY`: OpenWeatherMapのAPIキー
- `DEFAULT_POSTAL_CODE`: デフォルトの郵便番号（例: 1000001）

設定方法：
1. Vercelのプロジェクトページで「Settings」タブをクリック
2. 「Environment Variables」セクションに移動
3. 上記の環境変数を追加
4. 「Save」をクリック
5. プロジェクトを再デプロイ

### 4. アクセス

デプロイが完了すると、Vercelが自動的にURLを生成します：
- `https://your-project-name.vercel.app`

## テスト

```bash
# すべてのテストを実行
pytest

# プロパティベーステストを実行
pytest tests/property/

# ユニットテストを実行
pytest tests/unit/
```

## ライセンス

MIT License
