# Vercelデプロイガイド

このドキュメントは、Weather Zip LookupアプリケーションをVercelにデプロイする詳細な手順を説明します。

## 目次

1. [前提条件](#前提条件)
2. [初回デプロイ](#初回デプロイ)
3. [環境変数の設定](#環境変数の設定)
4. [更新のデプロイ](#更新のデプロイ)
5. [トラブルシューティング](#トラブルシューティング)

## 前提条件

### 必要なアカウント

- ✅ GitHubアカウント
- ✅ Vercelアカウント（[vercel.com](https://vercel.com)で無料登録）
- ✅ OpenWeatherMap APIキー（[openweathermap.org/api](https://openweathermap.org/api)で無料取得）

### リポジトリの準備

```bash
# 最新の変更をコミット
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

## 初回デプロイ

### ステップ1: Vercelにログイン

1. [Vercel](https://vercel.com)にアクセス
2. 「Sign Up」または「Log In」をクリック
3. GitHubアカウントで認証

### ステップ2: 新規プロジェクトを作成

1. Vercelダッシュボードで「Add New...」→「Project」をクリック
2. 「Import Git Repository」セクションでGitHubリポジトリを検索
3. `weather-zip-lookup`リポジトリを選択
4. 「Import」をクリック

### ステップ3: プロジェクト設定

**Configure Project**画面で以下を設定：

| 設定項目 | 値 |
|---------|-----|
| Framework Preset | `Other` |
| Root Directory | `.` (デフォルト) |
| Build Command | （空欄） |
| Output Directory | （空欄） |
| Install Command | `pip install -r requirements-prod.txt` |

**重要**: Install Commandを必ず設定してください。これにより、本番環境に必要な依存関係のみがインストールされます。

### ステップ4: デプロイ

1. 「Deploy」ボタンをクリック
2. ビルドプロセスを監視（通常1-2分）
3. デプロイ完了を待つ

**注意**: 初回デプロイは環境変数が未設定のため、アプリは正常に動作しません。次のステップで環境変数を設定します。

## 環境変数の設定

### ステップ1: 設定画面に移動

1. デプロイ完了後、プロジェクトダッシュボードに移動
2. 上部メニューの「Settings」タブをクリック
3. 左サイドバーの「Environment Variables」をクリック

### ステップ2: 環境変数を追加

以下の環境変数を追加します：

#### 必須: OPENWEATHER_API_KEY

```
Key: OPENWEATHER_API_KEY
Value: your_actual_api_key_here
Environment: Production, Preview, Development (すべて選択)
```

**APIキーの取得方法**:
1. [OpenWeatherMap](https://openweathermap.org/api)にアクセス
2. 無料アカウントを作成
3. APIキーを生成（Free tierで十分）
4. APIキーをコピー

#### オプション: DEFAULT_POSTAL_CODE

```
Key: DEFAULT_POSTAL_CODE
Value: 1000001
Environment: Production, Preview, Development (すべて選択)
```

デフォルトの郵便番号を設定します（任意）。

### ステップ3: 再デプロイ

**重要**: 環境変数を追加した後は、必ず再デプロイが必要です。

1. 上部メニューの「Deployments」タブをクリック
2. 最新のデプロイメントの右側にある「...」メニューをクリック
3. 「Redeploy」を選択
4. 「Redeploy」ボタンをクリックして確認

## 更新のデプロイ

コードを更新した場合、Vercelは自動的に再デプロイします。

### 自動デプロイ

```bash
# ローカルで変更を加える
git add .
git commit -m "Update feature"
git push origin main
```

GitHubにプッシュすると、Vercelが自動的に検知して再デプロイします。

### 手動デプロイ

Vercelダッシュボードから手動で再デプロイすることもできます：

1. 「Deployments」タブに移動
2. 任意のデプロイメントの「...」メニューから「Redeploy」を選択

## プロジェクト構造とVercel

### デプロイされるファイル

```
weather-zip-lookup/
├── weather_zip_lookup/      # アプリケーションコード
│   ├── routes/
│   ├── services/
│   ├── templates/
│   └── static/
├── wsgi.py                  # Vercelエントリーポイント
├── vercel.json              # Vercel設定
├── requirements-prod.txt    # 本番依存関係
└── .vercelignore           # デプロイ除外ファイル
```

### 除外されるファイル

`.vercelignore`により、以下は除外されます：
- テストファイル（`tests/`）
- 開発用スクリプト（`run.py`, `weather.py`）
- ドキュメント（`ARCHITECTURE.md`）
- IDE設定（`.vscode/`, `.idea/`）

## トラブルシューティング

### デプロイが失敗する

#### エラー: "No module named 'weather_zip_lookup'"

**原因**: Pythonパスが正しく設定されていない

**解決策**:
1. `vercel.json`に`PYTHONPATH`が設定されているか確認
2. プロジェクトルートが正しいか確認

#### エラー: "Could not find a version that satisfies the requirement"

**原因**: 依存関係のインストールに失敗

**解決策**:
1. `requirements-prod.txt`の内容を確認
2. Install Commandが`pip install -r requirements-prod.txt`になっているか確認

### アプリが動作しない

#### エラー: "APIキーが設定されていません"

**原因**: 環境変数が設定されていない、または再デプロイされていない

**解決策**:
1. Settings → Environment Variables で`OPENWEATHER_API_KEY`を確認
2. 環境変数を追加/変更した後、必ず再デプロイ

#### エラー: "郵便番号が指定されていません"

**原因**: デフォルト郵便番号が設定されていない

**解決策**:
1. フォームに郵便番号を入力する
2. または、`DEFAULT_POSTAL_CODE`環境変数を設定

#### 500 Internal Server Error

**原因**: サーバー側のエラー

**解決策**:
1. Vercelダッシュボードの「Functions」タブでログを確認
2. エラーメッセージを確認して対処

### ログの確認方法

1. Vercelダッシュボードに移動
2. プロジェクトを選択
3. 「Functions」タブをクリック
4. 最新のリクエストログを確認

## パフォーマンス最適化

### キャッシング

Vercelは自動的に静的ファイルをキャッシュします。

### 関数の最適化

- Lambda関数のサイズ制限: 15MB（`vercel.json`で設定済み）
- コールドスタート時間: 通常1-2秒

## セキュリティ

### 環境変数の管理

- ✅ APIキーは環境変数として保存（コードにハードコードしない）
- ✅ `.gitignore`で機密情報を除外
- ✅ Vercelの環境変数は暗号化されて保存

### HTTPS

Vercelは自動的にHTTPSを有効化します。

## カスタムドメイン

### ドメインの追加

1. Vercelダッシュボードの「Settings」→「Domains」に移動
2. 「Add」ボタンをクリック
3. ドメイン名を入力
4. DNSレコードを設定（Vercelが指示を表示）

### SSL証明書

Vercelは自動的にSSL証明書を発行・更新します（Let's Encrypt使用）。

## サポート

問題が解決しない場合：

1. [Vercelドキュメント](https://vercel.com/docs)を確認
2. [Vercelコミュニティ](https://github.com/vercel/vercel/discussions)で質問
3. プロジェクトのGitHub Issuesで報告

## 参考リンク

- [Vercel公式ドキュメント](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Flask on Vercel](https://vercel.com/guides/using-flask-with-vercel)
- [OpenWeatherMap API](https://openweathermap.org/api)
