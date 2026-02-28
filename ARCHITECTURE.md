# プロジェクト構造

このドキュメントは、Weather Zip Lookupプロジェクトの構造とアーキテクチャを説明します。

## ディレクトリ構造

```
weather-zip-lookup/
├── weather_zip_lookup/          # メインアプリケーションパッケージ
│   ├── __init__.py             # アプリケーションファクトリ
│   ├── cli.py                  # CLIインターフェース
│   ├── config.py               # 設定管理
│   ├── exceptions.py           # カスタム例外
│   ├── models.py               # データモデル
│   ├── routes/                 # Flaskルート
│   │   ├── __init__.py
│   │   └── main.py            # メインルート
│   ├── services/               # ビジネスロジック層
│   │   ├── __init__.py
│   │   ├── weather_service.py # 天気データ取得サービス
│   │   └── formatter.py       # 出力フォーマッター
│   ├── templates/              # Flaskテンプレート
│   │   └── index.html
│   └── static/                 # 静的ファイル（CSS, JS, 画像）
├── tests/                      # テストスイート
│   ├── e2e/                   # E2Eテスト（Playwright）
│   ├── property/              # プロパティベーステスト（Hypothesis）
│   └── unit/                  # ユニットテスト
├── test-results/              # テスト結果（Git無視）
├── .gitignore                 # Git無視設定
├── pytest.ini                 # Pytest設定
├── README.md                  # プロジェクトドキュメント
├── ARCHITECTURE.md            # このファイル
├── requirements.txt           # Python依存関係
├── run.py                     # 開発サーバー起動スクリプト
├── weather.py                 # CLIエントリーポイント
├── wsgi.py                    # WSGIエントリーポイント（Vercel用）
└── vercel.json                # Vercel設定
```

## アーキテクチャパターン

### アプリケーションファクトリパターン

Flaskのベストプラクティスに従い、アプリケーションファクトリパターンを使用しています。

**メリット**:
- テストが容易
- 複数のアプリケーションインスタンスを作成可能
- 設定の柔軟性

**実装**: `weather_zip_lookup/__init__.py`の`create_app()`関数

### レイヤードアーキテクチャ

```
┌─────────────────────────────────────┐
│  プレゼンテーション層                │
│  (routes/, templates/, CLI)         │
├─────────────────────────────────────┤
│  ビジネスロジック層                  │
│  (services/)                        │
├─────────────────────────────────────┤
│  データアクセス層                    │
│  (models/, config/)                 │
└─────────────────────────────────────┘
```

## 主要コンポーネント

### 1. アプリケーションファクトリ (`__init__.py`)

```python
def create_app(config=None):
    """Flaskアプリケーションを作成"""
    app = Flask(__name__)
    # 設定読み込み
    # ルート登録
    return app
```

### 2. ルート層 (`routes/`)

- HTTPリクエストを処理
- ビジネスロジックを呼び出し
- レスポンスを返す

### 3. サービス層 (`services/`)

- ビジネスロジックを実装
- 外部APIとの通信
- データ変換とフォーマット

### 4. モデル層 (`models.py`)

- データ構造を定義
- データクラスを使用

### 5. 設定管理 (`config.py`)

- 環境変数とローカル設定ファイルをサポート
- プラットフォーム固有のパス処理

## エントリーポイント

### 開発環境

```bash
# Webアプリ
python run.py

# CLI
python weather.py [郵便番号]
```

### 本番環境（Vercel）

- `wsgi.py`がエントリーポイント
- 環境変数から設定を読み込む

## 設定管理

### 優先順位

1. 環境変数（最優先）
2. ローカル設定ファイル
3. デフォルト値

### 環境変数

- `OPENWEATHER_API_KEY`: OpenWeatherMap APIキー
- `DEFAULT_POSTAL_CODE`: デフォルト郵便番号
- `SECRET_KEY`: Flaskシークレットキー

### ローカル設定ファイル

- Windows: `%APPDATA%\weather-zip-lookup\config.json`
- Mac/Linux: `~/.config/weather-zip-lookup/config.json`

## テスト戦略

### ユニットテスト (`tests/unit/`)

- 個別のコンポーネントをテスト
- モックを使用して外部依存を排除

### プロパティベーステスト (`tests/property/`)

- Hypothesisを使用
- ランダムな入力でロバスト性を検証

### E2Eテスト (`tests/e2e/`)

- Playwrightを使用
- 実際のブラウザでWebアプリをテスト
- スクリーンショットと動画を記録

## デプロイ

### Vercel

1. GitHubリポジトリをVercelに接続
2. 環境変数を設定
3. 自動デプロイ

**設定ファイル**: `vercel.json`

## ベストプラクティス

1. **関心の分離**: 各層が明確な責任を持つ
2. **依存性注入**: アプリケーションファクトリで設定を注入
3. **テスタビリティ**: モックとフィクスチャを使用
4. **設定の柔軟性**: 環境変数とローカル設定をサポート
5. **エラーハンドリング**: カスタム例外で明確なエラー処理

## 今後の拡張

- [ ] データベース統合
- [ ] ユーザー認証
- [ ] キャッシング
- [ ] ロギング
- [ ] API レート制限
- [ ] 国際化（i18n）
