# デザインドキュメント

## 概要

本ドキュメントは、郵便番号から天気情報を取得するクロスプラットフォーム対応のPythonターミナルスクリプトの設計を定義します。スクリプトは、OpenWeatherMap APIを使用して現在の気温、降水確率、気象警報を取得し、色付きでフォーマットされた出力をターミナルに表示します。

## アーキテクチャ

システムは以下のレイヤーで構成されます：

```
┌─────────────────────────────────────┐
│     CLI Interface Layer             │
│  (引数解析、ユーザー入力処理)        │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Configuration Manager Layer       │
│  (設定ファイルの読み書き)            │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Weather Service Layer             │
│  (API呼び出し、データ取得)           │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Output Formatter Layer            │
│  (色付き出力、フォーマット)          │
└─────────────────────────────────────┘
```

### 設計原則

1. **関心の分離**: 各レイヤーは明確な責任を持つ
2. **プラットフォーム非依存性**: 標準ライブラリとクロスプラットフォームライブラリを使用
3. **エラーハンドリング**: 各レイヤーで適切なエラー処理を実装
4. **テスタビリティ**: 各コンポーネントは独立してテスト可能

## コンポーネントとインターフェース

### 1. CLI Interface (`cli.py`)

コマンドライン引数を解析し、メインフローを制御します。

```python
def parse_arguments() -> argparse.Namespace:
    """
    コマンドライン引数を解析
    
    Returns:
        解析された引数を含むNamespaceオブジェクト
    """
    pass

def main() -> int:
    """
    メインエントリーポイント
    
    Returns:
        終了コード（0: 成功、1以上: エラー）
    """
    pass
```

### 2. Configuration Manager (`config.py`)

設定ファイルの読み書きを管理します。

```python
class ConfigManager:
    """設定ファイルを管理するクラス"""
    
    def __init__(self):
        """設定ファイルのパスを初期化"""
        pass
    
    def get_config_path(self) -> Path:
        """
        プラットフォーム固有の設定ファイルパスを取得
        
        Returns:
            設定ファイルのPathオブジェクト
        """
        pass
    
    def load_config(self) -> dict:
        """
        設定ファイルを読み込む
        
        Returns:
            設定データを含む辞書
        """
        pass
    
    def save_config(self, config: dict) -> None:
        """
        設定ファイルに保存
        
        Args:
            config: 保存する設定データ
        """
        pass
    
    def get_default_postal_code(self) -> str:
        """
        デフォルトの郵便番号を取得
        
        Returns:
            郵便番号文字列
        """
        pass
    
    def get_api_key(self) -> str:
        """
        APIキーを取得
        
        Returns:
            APIキー文字列
        """
        pass
```

### 3. Weather Service (`weather_service.py`)

OpenWeatherMap APIとの通信を担当します。

```python
class WeatherService:
    """天気データを取得するサービスクラス"""
    
    def __init__(self, api_key: str):
        """
        Args:
            api_key: OpenWeatherMap APIキー
        """
        pass
    
    def get_weather_by_postal_code(self, postal_code: str) -> WeatherData:
        """
        郵便番号から天気データを取得
        
        Args:
            postal_code: 7桁の日本の郵便番号
            
        Returns:
            天気データを含むWeatherDataオブジェクト
            
        Raises:
            InvalidPostalCodeError: 郵便番号が無効な場合
            APIError: API呼び出しが失敗した場合
            NetworkError: ネットワーク接続が失敗した場合
        """
        pass
    
    def _convert_postal_code_to_coordinates(self, postal_code: str) -> tuple[float, float]:
        """
        郵便番号を緯度経度に変換
        
        Args:
            postal_code: 7桁の日本の郵便番号
            
        Returns:
            (緯度, 経度)のタプル
        """
        pass
    
    def _fetch_current_weather(self, lat: float, lon: float) -> dict:
        """
        現在の天気データを取得
        
        Args:
            lat: 緯度
            lon: 経度
            
        Returns:
            APIレスポンスの辞書
        """
        pass
    
    def _fetch_weather_alerts(self, lat: float, lon: float) -> list[dict]:
        """
        気象警報データを取得
        
        Args:
            lat: 緯度
            lon: 経度
            
        Returns:
            警報データのリスト
        """
        pass
```

### 4. Output Formatter (`formatter.py`)

天気データを色付きでフォーマットして表示します。

```python
class OutputFormatter:
    """出力をフォーマットするクラス"""
    
    def format_weather_output(self, weather_data: WeatherData) -> str:
        """
        天気データをフォーマット
        
        Args:
            weather_data: 表示する天気データ
            
        Returns:
            フォーマットされた文字列
        """
        pass
    
    def _format_temperature(self, temp: float) -> str:
        """気温をフォーマット"""
        pass
    
    def _format_precipitation(self, probability: float) -> str:
        """降水確率をフォーマット"""
        pass
    
    def _format_alerts(self, alerts: list[WeatherAlert]) -> str:
        """気象警報をフォーマット"""
        pass
```

## データモデル

### WeatherData

```python
@dataclass
class WeatherData:
    """天気データを表すデータクラス"""
    postal_code: str
    temperature: float  # 摂氏
    precipitation_probability: float  # パーセンテージ (0-100)
    alerts: list[WeatherAlert]
    location_name: str
```

### WeatherAlert

```python
@dataclass
class WeatherAlert:
    """気象警報を表すデータクラス"""
    alert_type: str  # 熱波、寒波、強風、雪、濃霧、大雨、雷
    description: str
    severity: str  # 重要度レベル
```

### 設定ファイル形式

JSON形式で保存：

```json
{
  "default_postal_code": "1000001",
  "api_key": "your_api_key_here"
}
```

設定ファイルの場所：
- **Mac OS / Linux**: `~/.config/weather-zip-lookup/config.json`
- **Windows**: `%APPDATA%\weather-zip-lookup\config.json`

## API統合の詳細

### OpenWeatherMap API

使用するエンドポイント：

1. **Geocoding API**: 郵便番号を緯度経度に変換
   - エンドポイント: `http://api.openweathermap.org/geo/1.0/zip`
   - パラメータ: `zip={postal_code},JP&appid={api_key}`

2. **Current Weather Data API**: 現在の天気データを取得
   - エンドポイント: `https://api.openweathermap.org/data/2.5/weather`
   - パラメータ: `lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=ja`

3. **One Call API 3.0**: 気象警報を取得
   - エンドポイント: `https://api.openweathermap.org/data/3.0/onecall`
   - パラメータ: `lat={lat}&lon={lon}&appid={api_key}&exclude=minutely,hourly,daily`

### エラーハンドリング

APIエラーコードのマッピング：
- `401`: 無効なAPIキー
- `404`: 郵便番号が見つからない
- `429`: レート制限超過
- `500-599`: サーバーエラー

## 使用ライブラリ

- **requests**: HTTP通信
- **colorama**: クロスプラットフォーム対応の色付き出力
- **argparse**: コマンドライン引数解析（標準ライブラリ）
- **pathlib**: ファイルパス処理（標準ライブラリ）
- **json**: 設定ファイル処理（標準ライブラリ）
- **dataclasses**: データモデル定義（標準ライブラリ）

## 正確性プロパティ

プロパティとは、システムのすべての有効な実行において真であるべき特性や動作のことです。プロパティは、人間が読める仕様と機械で検証可能な正確性保証の橋渡しとなります。


### プロパティ1: 天気データ取得の完全性

*任意の*有効な郵便番号に対して、Weather_Scriptは気温と降水確率の両方を含む完全な天気データを取得するべきである

**検証: 要件 1.1, 1.2**

### プロパティ2: APIレスポンス解析の正確性

*任意の*有効なAPIレスポンスに対して、解析後に抽出された気温と降水確率の値は、元のレスポンスの値と一致するべきである

**検証: 要件 1.3**

### プロパティ3: エラー条件の適切な処理

*任意の*APIエラー（ネットワークエラー、サーバーエラー、認証エラーなど）に対して、Weather_Scriptは説明的なエラーメッセージを表示し、適切な終了コードで終了するべきである

**検証: 要件 1.4, 7.1, 7.2, 7.5**

### プロパティ4: 入力検証

*任意の*無効な郵便番号形式（7桁以外、非数字文字を含むなど）に対して、Weather_Scriptは検証エラーメッセージを表示するべきである

**検証: 要件 1.5**

### プロパティ5: コマンドライン引数の優先

*任意の*有効な郵便番号がコマンドライン引数として提供された場合、Weather_Scriptはその郵便番号を使用し、設定ファイルのデフォルト値を無視するべきである

**検証: 要件 2.1**

### プロパティ6: 郵便番号形式の受け入れ

*任意の*7桁の数字文字列に対して、Weather_Scriptはそれを有効な郵便番号として受け入れるべきである

**検証: 要件 2.3**

### プロパティ7: 設定ファイルのラウンドトリップ

*任意の*有効な郵便番号とAPIキーに対して、設定ファイルに保存してから読み取った値は、元の値と一致するべきである

**検証: 要件 3.2, 3.5, 6.2**

### プロパティ8: 設定ファイルエラーの処理

*任意の*破損した設定ファイルまたは存在しない設定ファイルに対して、Weather_Scriptは適切なプロンプトまたはエラーメッセージを表示するべきである

**検証: 要件 3.3, 7.4**

### プロパティ9: プラットフォーム固有のパス生成

*任意の*プラットフォーム（Mac OS、Windows、Linux）に対して、Weather_Scriptはそのプラットフォームに適した設定ファイルパスを生成するべきである

**検証: 要件 3.4, 4.4**

### プロパティ10: 文字エンコーディングの一貫性

*任意の*Unicode文字を含むデータ（郵便番号、場所名、警報説明など）に対して、Weather_Scriptはすべてのプラットフォームで一貫して処理するべきである

**検証: 要件 4.5**

### プロパティ11: 出力の完全性

*任意の*天気データに対して、フォーマットされた出力は郵便番号、気温（摂氏記号付き）、降水確率（パーセンテージ記号付き）を含むべきである

**検証: 要件 5.2, 5.3, 5.4**

### プロパティ12: 色付き出力の生成

*任意の*天気データに対して、フォーマットされた出力は色コード（ANSIエスケープシーケンス）を含むべきである

**検証: 要件 5.1**

### プロパティ13: APIリクエストへのキー含有

*任意の*APIキーに対して、構築されたAPIリクエストURLまたはヘッダーにそのキーが含まれるべきである

**検証: 要件 6.4**

### プロパティ14: 気象警報の完全な取得

*任意の*複数の警報を含むAPIレスポンスに対して、Weather_Scriptはすべての警報を取得し、いずれも欠落させないべきである

**検証: 要件 8.1**

### プロパティ15: 警報情報の表示

*任意の*気象警報に対して、フォーマットされた出力は警報の種類と説明の両方を含むべきである

**検証: 要件 8.2, 8.3**

### プロパティ16: 警報の視覚的強調

*任意の*気象警報に対して、フォーマットされた警報出力は特別な色コードまたはアイコンを含むべきである

**検証: 要件 8.4**

## エラーハンドリング

### エラーの種類と処理

1. **ネットワークエラー**
   - 例外: `NetworkError`
   - 終了コード: 1
   - メッセージ: "ネットワーク接続に失敗しました。インターネット接続を確認してください。"

2. **APIエラー**
   - 例外: `APIError`
   - 終了コード: 2
   - メッセージ: APIエラーコードに応じた詳細メッセージ
     - 401: "無効なAPIキーです。設定を確認してください。"
     - 404: "指定された郵便番号が見つかりませんでした。"
     - 429: "APIレート制限を超えました。しばらく待ってから再試行してください。"
     - 500-599: "天気サービスが一時的に利用できません。後でもう一度お試しください。"

3. **入力検証エラー**
   - 例外: `InvalidPostalCodeError`
   - 終了コード: 3
   - メッセージ: "無効な郵便番号形式です。7桁の数字を入力してください。"

4. **設定ファイルエラー**
   - 例外: `ConfigError`
   - 終了コード: 4
   - メッセージ: "設定ファイルの読み取りまたは書き込みに失敗しました。"

5. **APIキー欠落**
   - 例外: `MissingAPIKeyError`
   - 終了コード: 5
   - メッセージ: "APIキーが設定されていません。OpenWeatherMapからAPIキーを取得してください。"

### エラーハンドリング戦略

- すべてのAPI呼び出しは`try-except`ブロックで囲む
- ユーザーフレンドリーなエラーメッセージを日本語で表示
- エラーの種類に応じて適切な終了コードを返す
- ログファイルに詳細なエラー情報を記録（オプション）

## テスト戦略

### デュアルテストアプローチ

本プロジェクトでは、ユニットテストとプロパティベーステストの両方を使用します：

- **ユニットテスト**: 特定の例、エッジケース、エラー条件を検証
- **プロパティテスト**: すべての入力にわたる普遍的なプロパティを検証

両方のアプローチは補完的であり、包括的なカバレッジに必要です。

### ユニットテスト

ユニットテストは以下に焦点を当てます：

- 特定の例（例: 特定の郵便番号での天気取得）
- 統合ポイント（例: API呼び出しとレスポンス解析の連携）
- エッジケース（例: 空の警報リスト、極端な気温値）
- エラー条件（例: ネットワークタイムアウト、無効なJSON）

### プロパティベーステスト

プロパティテストには**Hypothesis**ライブラリを使用します。

**設定**:
- 各プロパティテストは最低100回の反復を実行
- 各テストは設計ドキュメントのプロパティを参照
- タグ形式: `# Feature: weather-zip-lookup, Property {番号}: {プロパティテキスト}`

**テスト対象のプロパティ**:
- プロパティ1-16（上記の正確性プロパティセクションで定義）

### テストファイル構成

```
tests/
├── unit/
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_weather_service.py
│   └── test_formatter.py
└── property/
    ├── test_properties_data_retrieval.py
    ├── test_properties_config.py
    ├── test_properties_output.py
    └── test_properties_error_handling.py
```

### モックとスタブ

- API呼び出しには`responses`ライブラリを使用してモック
- ファイルシステム操作には`pytest`のfixtureを使用
- 環境変数とプラットフォーム検出にはモンキーパッチを使用

## 実装の注意事項

### 郵便番号から座標への変換

日本の郵便番号は、OpenWeatherMap Geocoding APIを使用して緯度経度に変換します。郵便番号は`1000001`のような7桁の形式で、ハイフンなしで処理します。

### 降水確率の取得

OpenWeatherMap APIの現在の天気データには降水確率が含まれていない場合があります。その場合は、One Call API 3.0の`hourly`データから次の1時間の降水確率を取得します。

### 色付き出力

`colorama`ライブラリを使用して、クロスプラットフォーム対応の色付き出力を実現します：

- 気温: 青（寒い）、緑（快適）、赤（暑い）
- 降水確率: 灰色（低）、黄色（中）、赤（高）
- 警報: 赤背景に白文字、警告アイコン付き

### 気象警報のマッピング

OpenWeatherMap APIの警報イベントを日本語の警報タイプにマッピング：

- `Extreme temperature` → 熱波/寒波
- `Wind` → 強風
- `Snow` → 雪
- `Fog` → 濃霧
- `Rain` → 大雨
- `Thunderstorm` → 雷
