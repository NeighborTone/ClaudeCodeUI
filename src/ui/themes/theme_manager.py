# -*- coding: utf-8 -*-
"""
Theme Manager - テーマ管理システム
"""
from .light_theme import LightTheme
from .dark_theme import DarkTheme
from .cyberpunk_theme import CyberpunkTheme
from .nordic_theme import NordicTheme


class ThemeManager:
    """テーマ管理クラス"""
    
    def __init__(self):
        # 利用可能なテーマクラスを登録
        self._theme_classes = {
            "light": LightTheme,
            "dark": DarkTheme,
            "cyberpunk": CyberpunkTheme,
            "nordic": NordicTheme
        }
        
        # テーマインスタンスのキャッシュ
        self._theme_instances = {}
        
        # デフォルトテーマ
        self.current_theme = "cyberpunk"
    
    def get_theme_names(self):
        """利用可能なテーマ名のリストを取得"""
        return list(self._theme_classes.keys())
    
    def get_theme_display_names(self):
        """表示用のテーマ名マッピングを取得"""
        display_names = {}
        for theme_name in self._theme_classes:
            theme_instance = self._get_theme_instance(theme_name)
            display_names[theme_name] = theme_instance.get_display_name()
        return display_names
    
    def set_theme(self, theme_name):
        """テーマを設定"""
        if theme_name in self._theme_classes:
            self.current_theme = theme_name
            return True
        return False
    
    def get_current_theme_style(self):
        """現在のテーマのスタイルシートを取得"""
        theme_instance = self._get_theme_instance(self.current_theme)
        return theme_instance.get_main_style()
    
    def get_completion_widget_style(self):
        """現在のテーマのファイル補完ウィジェットスタイルを取得"""
        theme_instance = self._get_theme_instance(self.current_theme)
        return theme_instance.get_completion_widget_style()
    
    def get_main_font(self):
        """現在のテーマのメインフォントを取得"""
        theme_instance = self._get_theme_instance(self.current_theme)
        return theme_instance.get_main_font()
    
    def add_theme(self, theme_name, theme_class):
        """新しいテーマを追加（拡張性のため）"""
        self._theme_classes[theme_name] = theme_class
        # キャッシュから削除（次回アクセス時に再作成）
        if theme_name in self._theme_instances:
            del self._theme_instances[theme_name]
    
    def _get_theme_instance(self, theme_name):
        """テーマインスタンスを取得（キャッシュ機能付き）"""
        if theme_name not in self._theme_instances:
            if theme_name in self._theme_classes:
                self._theme_instances[theme_name] = self._theme_classes[theme_name]()
            else:
                # フォールバック: デフォルトテーマを使用
                self._theme_instances[theme_name] = self._theme_classes["cyberpunk"]()
        
        return self._theme_instances[theme_name]


# グローバルインスタンス
theme_manager = ThemeManager()


def apply_theme(widget, theme_name=None):
    """ウィジェットにテーマを適用"""
    if theme_name:
        theme_manager.set_theme(theme_name)
    widget.setStyleSheet(theme_manager.get_current_theme_style())


def get_completion_widget_style():
    """ファイル補完ウィジェットのスタイルを取得"""
    return theme_manager.get_completion_widget_style()


def get_main_font():
    """メインフォントを取得"""
    return theme_manager.get_main_font()