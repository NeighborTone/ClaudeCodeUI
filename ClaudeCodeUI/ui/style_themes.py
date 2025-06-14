"""
UIテーマ定義モジュール（レガシー互換性維持）
新しいテーマは ui/themes/ パッケージを使用してください
"""

# 新しいthemesパッケージからインポート
from .themes import theme_manager, apply_theme, get_completion_widget_style, get_main_font

# レガシー互換性のためのエクスポート
__all__ = ['theme_manager', 'apply_theme', 'get_completion_widget_style', 'get_main_font']