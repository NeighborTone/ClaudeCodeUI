# -*- coding: utf-8 -*-
"""
Settings Manager - Application settings management
"""
import json
import os
from typing import Any, Dict, Optional
from pathlib import Path


class SettingsManager:
    """設定管理クラス"""
    
    def __init__(self, config_file: str = "saved/settings.json"):
        self.config_file = config_file
        self.settings: Dict[str, Any] = self.load_default_settings()
        self.load_settings()
    
    def load_default_settings(self) -> Dict[str, Any]:
        """デフォルト設定を読み込み"""
        return {
            "window": {
                "width": 1200,
                "height": 800,
                "x": 100,
                "y": 100
            },
            "ui": {
                "thinking_level": "think",
                "font_size": 10,
                "font_family": "Consolas",
                "theme": "cyberpunk",
                "preview_visible": True,
                "splitter_sizes": [300, 400, 500]  # [file_tree, preview, prompt_input]
            },
            "file_search": {
                "max_results": 10,
                "max_preview_lines": 10
            },
            "indexing": {
                "use_sqlite": True,
                "auto_index_on_startup": True,
                "cache_ttl": 300
            },
            "workspaces": {
                "auto_load": True,
                "max_depth": 3
            },
            "templates": {
                "selected_pre_template": "",
                "selected_post_template": ""
            }
        }
    
    def load_settings(self) -> None:
        """設定ファイルから設定を読み込み"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.merge_settings(loaded_settings)
        except Exception as e:
            print(f"設定読み込みエラー: {e}")
    
    def merge_settings(self, loaded_settings: Dict[str, Any]) -> None:
        """読み込んだ設定をデフォルト設定にマージ"""
        def merge_dict(default: Dict, loaded: Dict) -> Dict:
            result = default.copy()
            for key, value in loaded.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dict(result[key], value)
                else:
                    result[key] = value
            return result
        
        self.settings = merge_dict(self.settings, loaded_settings)
    
    def save_settings(self) -> None:
        """設定をファイルに保存"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"設定保存エラー: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """設定値を取得（ドット記法でネストしたキーにアクセス可能）"""
        keys = key_path.split('.')
        value = self.settings
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """設定値を設定（ドット記法でネストしたキーにアクセス可能）"""
        keys = key_path.split('.')
        current = self.settings
        
        # 最後のキー以外を辿る
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # 最後のキーに値を設定
        current[keys[-1]] = value
    
    def get_window_geometry(self) -> Dict[str, int]:
        """ウィンドウジオメトリを取得"""
        return {
            'x': self.get('window.x', 100),
            'y': self.get('window.y', 100),
            'width': self.get('window.width', 1200),
            'height': self.get('window.height', 800)
        }
    
    def set_window_geometry(self, x: int, y: int, width: int, height: int) -> None:
        """ウィンドウジオメトリを設定"""
        self.set('window.x', x)
        self.set('window.y', y)
        self.set('window.width', width)
        self.set('window.height', height)
    
    def get_thinking_level(self) -> str:
        """思考レベルを取得"""
        return self.get('ui.thinking_level', 'think')
    
    def set_thinking_level(self, level: str) -> None:
        """思考レベルを設定"""
        self.set('ui.thinking_level', level)
    
    def get_font_settings(self) -> Dict[str, Any]:
        """フォント設定を取得"""
        return {
            'family': self.get('ui.font_family', 'Consolas'),
            'size': self.get('ui.font_size', 10)
        }
    
    def set_font_settings(self, family: str, size: int) -> None:
        """フォント設定を設定"""
        self.set('ui.font_family', family)
        self.set('ui.font_size', size)
    
    def get_theme(self) -> str:
        """テーマ名を取得"""
        return self.get('ui.theme', 'cyberpunk')
    
    def set_theme(self, theme: str) -> None:
        """テーマを設定"""
        self.set('ui.theme', theme)
    
    
    def get_preview_visible(self) -> bool:
        """プレビュー表示状態を取得"""
        return self.get('ui.preview_visible', True)
    
    def set_preview_visible(self, visible: bool) -> None:
        """プレビュー表示状態を設定"""
        self.set('ui.preview_visible', visible)
    
    def get_splitter_sizes(self) -> list:
        """スプリッターサイズを取得"""
        return self.get('ui.splitter_sizes', [300, 400, 500])
    
    def set_splitter_sizes(self, sizes: list) -> None:
        """スプリッターサイズを設定"""
        self.set('ui.splitter_sizes', sizes)
    
    def get_selected_pre_template(self) -> str:
        """選択されたプリテンプレートを取得"""
        return self.get('templates.selected_pre_template', '')
    
    def set_selected_pre_template(self, template_name: str) -> None:
        """選択されたプリテンプレートを設定"""
        self.set('templates.selected_pre_template', template_name)
    
    def get_selected_post_template(self) -> str:
        """選択されたポストテンプレートを取得"""
        return self.get('templates.selected_post_template', '')
    
    def set_selected_post_template(self, template_name: str) -> None:
        """選択されたポストテンプレートを設定"""
        self.set('templates.selected_post_template', template_name)