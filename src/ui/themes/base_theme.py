# -*- coding: utf-8 -*-
"""
Base Theme - テーマ基底クラス
"""
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt
from abc import ABC, abstractmethod
import os


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
    
    def create_colored_icon(self, icon_path, color_hex):
        """
        白いアイコンを指定色に変更
        
        Args:
            icon_path: アイコンファイルのパス
            color_hex: 変更したい色 (例: "#00FFAA")
            
        Returns:
            QPixmap: 色付きアイコン
        """
        # 元のアイコンを読み込み
        original_pixmap = QPixmap(icon_path)
        if original_pixmap.isNull():
            return QPixmap()
        
        # 新しいピクスマップを作成
        colored_pixmap = QPixmap(original_pixmap.size())
        colored_pixmap.fill(Qt.transparent)
        
        # ペインターで色を適用
        painter = QPainter(colored_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        
        # 元のアイコンの形状を保持しながら色を変更
        painter.drawPixmap(0, 0, original_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(colored_pixmap.rect(), QColor(color_hex))
        painter.end()
        
        return colored_pixmap
    
    def get_theme_directory_name(self):
        """テーマのディレクトリ名を取得（英語）"""
        display_name = self.get_display_name()
        
        # 日本語テーマ名を英語ディレクトリ名にマッピング
        name_mapping = {
            "サイバーパンク": "cyber",
            "ダークモード": "dark", 
            "ライトモード": "light",
            "ノルディック": "nordic",
            "Cyberpunk": "cyber",
            "Dark Mode": "dark",
            "Light Mode": "light", 
            "Nordic": "nordic"
        }
        
        return name_mapping.get(display_name, display_name.lower().replace(" ", "_"))
    
    def save_colored_icons(self, expanded_color, collapsed_color):
        """
        テーマ用の色付きアイコンを生成・保存
        
        Args:
            expanded_color: 展開時のアイコン色
            collapsed_color: 折りたたみ時のアイコン色
        """
        theme_dir = self.get_theme_directory_name()
        
        # 保存先ディレクトリを作成
        save_dir = f"assets/icons/treeview/{theme_dir}"
        os.makedirs(save_dir, exist_ok=True)
        
        # 元のアイコンパス
        arrow_down_path = "assets/icons/treeview/arrow_down.png"
        arrow_right_path = "assets/icons/treeview/arrow_right.png"
        
        # 色付きアイコンを生成・保存
        if os.path.exists(arrow_down_path):
            colored_down = self.create_colored_icon(arrow_down_path, expanded_color)
            colored_down.save(f"{save_dir}/arrow_down.png")
        
        if os.path.exists(arrow_right_path):
            colored_right = self.create_colored_icon(arrow_right_path, collapsed_color)
            colored_right.save(f"{save_dir}/arrow_right.png")
    
    def get_tree_branch_styles(self, expanded_color="#ffffff", collapsed_color="#ffffff"):
        """
        ツリーブランチ用のカスタムアイコンスタイルを取得
        
        Args:
            expanded_color: 展開時のアイコン色
            collapsed_color: 折りたたみ時のアイコン色
        """
        theme_dir = self.get_theme_directory_name()
        
        # テーマ用の色付きアイコンを生成
        self.save_colored_icons(expanded_color, collapsed_color)
        
        return f"""
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {{
                border-image: none;
                image: url(assets/icons/treeview/{theme_dir}/arrow_right.png);
            }}
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {{
                border-image: none;
                image: url(assets/icons/treeview/{theme_dir}/arrow_down.png);
            }}
            QTreeWidget::branch:has-siblings:!adjoins-item {{
                border-image: none;
            }}
            QTreeWidget::branch:has-siblings:adjoins-item {{
                border-image: none;
            }}
            QTreeWidget::branch:!has-children:!has-siblings:adjoins-item {{
                border-image: none;
            }}
        """