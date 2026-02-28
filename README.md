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
python run.py

# ブラウザでアクセス
# http://localhost:5000
```

## Vercelにデプロイ

### 前提条件

- GitHubアカウント
- Vercelアカウント（無料）
- OpenWeatherMap APIキー（[こちら](https://openweathermap.org/api)から無料で取得）

### 1. GitHubリポジトリにプッシュ

```bash
# すでにリポジトリがある場合
git add .
git commit -m "Update for Vercel deployment"
git push origin main

# 新規リポジトリの場合
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
3. GitHubリポジトリを選択（`weather-zip-lookup`）
4. **Build & Development Settings**:
   - Framework Preset: `Other`
   - Build Command: （空欄のまま）
   - Output Directory: （空欄のまま）
   - Install Command: `pip install -r requirements-prod.txt`
5. 「Deploy」をクリック

### 3. 環境変数を設定

デプロイ後、Vercelのプロジェクト設定で以下の環境変数を追加：

| 変数名 | 値 | 説明 |
|--------|-----|------|
| `OPENWEATHER_API_KEY` | `your_api_key_here` | OpenWeatherMapのAPIキー |
| `DEFAULT_POSTAL_CODE` | `1000001` | デフォルトの郵便番号（任意） |

**設定方法**:
1. Vercelのプロジェクトページで「Settings」タブをクリック
2. 「Environment Variables」セクションに移動
3. 上記の環境変数を追加
4. 「Save」をクリック
5. **「Redeploy」をクリックして再デプロイ**（重要！）

### 4. デプロイの確認

デプロイが完了すると、Vercelが自動的にURLを生成します：
- `https://your-project-name.vercel.app`

ブラウザでアクセスして動作を確認してください。

### トラブルシューティング

#### デプロイが失敗する場合

1. **ビルドログを確認**: Vercelのデプロイメントページでログを確認
2. **環境変数を確認**: `OPENWEATHER_API_KEY`が正しく設定されているか
3. **再デプロイ**: 環境変数を変更した後は必ず再デプロイ

#### アプリが動作しない場合

1. **Function Logs を確認**: Vercelダッシュボードで実行時エラーを確認
2. **APIキーを確認**: OpenWeatherMapのAPIキーが有効か確認
3. **郵便番号を確認**: 7桁の日本の郵便番号を使用しているか確認
4. 「Save」をクリック
5. **「Redeploy」をクリックして再デプロイ**（重要！）

### 4. デプロイの確認

デプロイが完了すると、Vercelが自動的にURLを生成します：
- `https://your-project-name.vercel.app`

ブラウザでアクセスして動作を確認してください。

### トラブルシューティング

#### デプロイが失敗する場合

1. **ビルドログを確認**: Vercelのデプロイメントページでログを確認
2. **環境変数を確認**: `OPENWEATHER_API_KEY`が正しく設定されているか
3. **再デプロイ**: 環境変数を変更した後は必ず再デプロイ

#### アプリが動作しない場合

1. **Function Logs を確認**: Vercelダッシュボードで実行時エラーを確認
2. **APIキーを確認**: OpenWeatherMapのAPIキーが有効か確認
3. **郵便番号を確認**: 7桁の日本の郵便番号を使用しているか確認

### 5. カスタムドメインの設定（オプション）

Vercelダッシュボードの「Domains」セクションでカスタムドメインを追加できます。

### 詳細なデプロイ手順

より詳細なデプロイ手順とトラブルシューティングについては、[DEPLOYMENT.md](DEPLOYMENT.md)を参照してください。

## テスト

```bash
# すべてのテストを実行
pytest

# ユニットテストを実行
pytest tests/unit/

# プロパティベーステストを実行
pytest tests/property/

# E2Eテストを実行（スクリーンショット・動画付き）
pytest tests/e2e/ -v --screenshot=on --video=on
```

### テスト結果

テスト結果は `test-results/reports/` ディレクトリに保存されます：

- 📊 [テスト結果サマリー](test-results/reports/README.md)
- 📝 [ユニットテスト結果](test-results/reports/unit-tests.md)
- 🌐 [E2Eテスト結果](test-results/reports/e2e-tests.md)
- 📸 スクリーンショット: `test-results/screenshots/`
- 🎥 動画: `test-results/tests-e2e-test-web-app-py-*/video.webm`

**最新のテスト結果**:
- ✅ ユニットテスト: 62/62 PASSED
- ✅ プロパティベーステスト: 3/3 PASSED
- ✅ E2Eテスト: 8/8 PASSED
- 🎯 成功率: 100% (73/73)

## プロジェクト構造

プロジェクトの詳細なアーキテクチャについては、[ARCHITECTURE.md](ARCHITECTURE.md)を参照してください。

## ライセンス

MIT License
