# Theme System

この`themes`パッケージは、アプリケーションのテーマシステムを管理します。

## 構造

```
ui/themes/
├── __init__.py              # パッケージ初期化
├── README.md               # このファイル
├── base_theme.py           # テーマ基底クラス
├── theme_manager.py        # テーママネージャー
├── light_theme.py          # ライトテーマ
├── dark_theme.py           # ダークテーマ
├── cyberpunk_theme.py      # サイバーパンクテーマ
└── nordic_theme.py         # ノルディックテーマ（例）
```

## 新しいテーマの追加方法

### 1. テーマファイルの作成

`ui/themes/`ディレクトリに新しいテーマファイルを作成します：

```python
# -*- coding: utf-8 -*-
"""
My Custom Theme - カスタムテーマ定義
"""
from PySide6.QtGui import QFont
from .base_theme import BaseTheme


class MyCustomTheme(BaseTheme):
    """カスタムテーマクラス"""
    
    def get_display_name(self):
        return "カスタムテーマ"
    
    def _build_theme(self):
        return {
            "main": """
            QWidget {
                background-color: #your-color;
                color: #text-color;
                /* その他のスタイル */
            }
            /* 各UIコンポーネントのスタイル */
            """,
            "completion_widget": """
            /* ファイル補完ウィジェットのスタイル */
            """,
            "main_font": QFont("Font Name", 10)
        }
```

### 2. テーママネージャーに登録

`theme_manager.py`を編集：

```python
# インポートを追加
from .my_custom_theme import MyCustomTheme

class ThemeManager:
    def __init__(self):
        self._theme_classes = {
            "light": LightTheme,
            "dark": DarkTheme,
            "cyberpunk": CyberpunkTheme,
            "nordic": NordicTheme,
            "my_custom": MyCustomTheme  # 追加
        }
```

### 3. 完了

新しいテーマが表示メニューに自動的に追加されます。

## BaseTheme API

すべてのテーマは`BaseTheme`クラスを継承し、以下のメソッドを実装する必要があります：

### 必須メソッド

- `get_display_name()`: メニューに表示される名前を返す
- `_build_theme()`: テーマデータ辞書を返す

### テーマデータ構造

```python
{
    "main": "メインQSSスタイルシート",
    "completion_widget": "ファイル補完ウィジェットのQSSスタイルシート", 
    "main_font": QFont("フォント名", サイズ)
}
```

## 使用方法

```python
from ui.themes import theme_manager, apply_theme

# テーマを設定
theme_manager.set_theme("my_custom")

# ウィジェットにテーマを適用
apply_theme(widget)

# 補完ウィジェットのスタイルを取得
style = theme_manager.get_completion_widget_style()
```

## 注意事項

- テーマ名は一意である必要があります
- QSSスタイルシートの構文に従う必要があります
- テーマファイルは`themes`パッケージ内に配置してください
- 既存のテーマを参考にして一貫性を保ってください