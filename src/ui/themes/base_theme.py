# -*- coding: utf-8 -*-
"""
Base Theme - テーマ基底クラス
"""
from PySide6.QtGui import QFont
from abc import ABC, abstractmethod


class BaseTheme(ABC):
    """テーマ基底クラス"""
    
    def __init__(self):
        self.theme_data = self._build_theme()
    
    @abstractmethod
    def _build_theme(self):
        """テーマデータを構築（各テーマで実装）"""
        pass
    
    @abstractmethod
    def get_display_name(self):
        """表示名を取得（各テーマで実装）"""
        pass
    
    def get_main_style(self):
        """メインスタイルシートを取得"""
        return self.theme_data.get("main", "")
    
    def get_completion_widget_style(self):
        """ファイル補完ウィジェットスタイルを取得"""
        return self.theme_data.get("completion_widget", "")
    
    def get_main_font(self):
        """メインフォントを取得"""
        return self.theme_data.get("main_font", QFont("Segoe UI", 10))
    
    def get_theme_data(self):
        """テーマデータ全体を取得"""
        return self.theme_data