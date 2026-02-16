#!/usr/bin/env python3
"""
天気情報取得スクリプトのメインエントリーポイント

郵便番号から天気情報を取得して表示します。
"""

import sys
from weather_zip_lookup.cli import main

if __name__ == '__main__':
    sys.exit(main())
