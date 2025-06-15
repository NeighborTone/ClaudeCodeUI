# -*- coding: utf-8 -*-
"""
Localization Manager - 外部ファイルベースの多言語管理システム
JSON、CSV、YAMLファイルからローカライゼーションデータを読み込み・管理
"""
import json
import csv
import os
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from core.language_manager import get_language_manager, LanguageCode

# YAML support is optional
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class LocalizationManager:
    """外部ファイルベースの多言語管理クラス"""
    
    def __init__(self, locales_dir: Optional[str] = None):
        """
        初期化
        
        Args:
            locales_dir: 言語ファイル格納ディレクトリ（指定しない場合はデフォルト）
        """
        if locales_dir is None:
            # アプリケーションディレクトリ内のconfig/localesフォルダ
            app_dir = Path(__file__).parent.parent
            self.locales_dir = app_dir / "config" / "locales"
        else:
            self.locales_dir = Path(locales_dir)
        
        # ローカライゼーションデータ格納用
        self._strings: Dict[str, Dict[LanguageCode, str]] = {}
        self._supported_languages: List[LanguageCode] = ["ja", "en"]
        self._fallback_language: LanguageCode = "en"
        
        # ディレクトリが存在しない場合は作成
        self.locales_dir.mkdir(parents=True, exist_ok=True)
        
        # 言語データを読み込み
        self.reload_translations()
    
    def reload_translations(self) -> None:
        """翻訳データを再読み込み"""
        self._strings.clear()
        
        # サポートされているファイル形式を順次試行
        loaded = False
        
        # 1. JSON形式を試行
        json_file = self.locales_dir / "strings.json"
        if json_file.exists():
            try:
                self._load_json_file(json_file)
                loaded = True
                print(f"Loaded translations from JSON: {json_file}")
            except Exception as e:
                print(f"Failed to load JSON file {json_file}: {e}")
        
        # 2. YAML形式を試行（YAMLサポートが利用可能な場合のみ）
        if not loaded and YAML_AVAILABLE:
            yaml_file = self.locales_dir / "strings.yaml"
            if yaml_file.exists():
                try:
                    self._load_yaml_file(yaml_file)
                    loaded = True
                    print(f"Loaded translations from YAML: {yaml_file}")
                except Exception as e:
                    print(f"Failed to load YAML file {yaml_file}: {e}")
        
        # 3. CSV形式を試行
        if not loaded:
            csv_file = self.locales_dir / "strings.csv"
            if csv_file.exists():
                try:
                    self._load_csv_file(csv_file)
                    loaded = True
                    print(f"Loaded translations from CSV: {csv_file}")
                except Exception as e:
                    print(f"Failed to load CSV file {csv_file}: {e}")
        
        # 4. 個別言語ファイルを試行
        if not loaded:
            for lang in self._supported_languages:
                lang_file = self.locales_dir / f"{lang}.json"
                if lang_file.exists():
                    try:
                        self._load_language_file(lang_file, lang)
                        loaded = True
                    except Exception as e:
                        print(f"Failed to load language file {lang_file}: {e}")
        
        if not loaded:
            print(f"Warning: No translation files found in {self.locales_dir}")
            # デフォルトの翻訳データを作成
            self._create_default_translations()
    
    def _load_json_file(self, file_path: Path) -> None:
        """JSON形式のファイルを読み込み"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # データ形式検証
        if 'strings' in data:
            # 新形式: {"languages": ["ja", "en"], "strings": {...}}
            if 'languages' in data:
                self._supported_languages = data['languages']
            self._strings = data['strings']
        else:
            # 旧形式: 直接文字列データ
            self._strings = data
    
    def _load_yaml_file(self, file_path: Path) -> None:
        """YAML形式のファイルを読み込み"""
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML is required for YAML support. Install with: pip install PyYAML")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if 'strings' in data:
            if 'languages' in data:
                self._supported_languages = data['languages']
            self._strings = data['strings']
        else:
            self._strings = data
    
    def _load_csv_file(self, file_path: Path) -> None:
        """CSV形式のファイルを読み込み"""
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            
            # ヘッダーから言語を検出
            fieldnames = reader.fieldnames
            if not fieldnames or 'key' not in fieldnames:
                raise ValueError("CSV file must have 'key' column")
            
            languages = [col for col in fieldnames if col != 'key' and col in ['ja', 'en']]
            self._supported_languages = languages
            
            # データを読み込み
            for row in reader:
                key = row['key']
                if key:
                    self._strings[key] = {}
                    for lang in languages:
                        if lang in row and row[lang]:
                            self._strings[key][lang] = row[lang]
    
    def _load_language_file(self, file_path: Path, language: LanguageCode) -> None:
        """個別言語ファイルを読み込み"""
        with open(file_path, 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        
        # 言語データをマージ
        for key, text in lang_data.items():
            if key not in self._strings:
                self._strings[key] = {}
            self._strings[key][language] = text
    
    def _create_default_translations(self) -> None:
        """デフォルトの翻訳データを作成"""
        # 最小限の翻訳データ
        default_strings = {
            "app_title": {
                "ja": "Claude Code PromptUI",
                "en": "Claude Code PromptUI"
            },
            "status_ready": {
                "ja": "準備完了",
                "en": "Ready"
            }
        }
        self._strings = default_strings
        
        # JSONファイルとして保存
        self.save_to_json()
    
    def get_string(self, key: str, language: Optional[LanguageCode] = None, **kwargs) -> str:
        """
        翻訳文字列を取得
        
        Args:
            key: 文字列キー
            language: 言語コード（指定しない場合は現在の言語）
            **kwargs: プレースホルダー置換用パラメータ
            
        Returns:
            翻訳された文字列
        """
        if language is None:
            language = get_language_manager().get_current_language()
        
        # キーが存在しない場合
        if key not in self._strings:
            print(f"Warning: Translation key '{key}' not found")
            return key
        
        # 指定言語が存在しない場合、フォールバックを試行
        if language not in self._strings[key]:
            if self._fallback_language in self._strings[key]:
                language = self._fallback_language
            else:
                print(f"Warning: No translation found for key '{key}' in language '{language}'")
                return key
        
        text = self._strings[key][language]
        
        # プレースホルダーを置換
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError as e:
                print(f"Warning: Missing placeholder {e} in string '{key}'")
        
        return text
    
    def add_string(self, key: str, translations: Dict[LanguageCode, str]) -> None:
        """新しい翻訳文字列を追加"""
        self._strings[key] = translations
    
    def remove_string(self, key: str) -> None:
        """翻訳文字列を削除"""
        if key in self._strings:
            del self._strings[key]
    
    def get_all_keys(self) -> List[str]:
        """すべての翻訳キーを取得"""
        return list(self._strings.keys())
    
    def get_supported_languages(self) -> List[LanguageCode]:
        """サポートされている言語リストを取得"""
        return self._supported_languages.copy()
    
    def save_to_json(self, file_path: Optional[Path] = None) -> None:
        """現在の翻訳データをJSONファイルに保存"""
        if file_path is None:
            file_path = self.locales_dir / "strings.json"
        
        data = {
            "languages": self._supported_languages,
            "strings": self._strings
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Translations saved to {file_path}")
    
    def save_to_csv(self, file_path: Optional[Path] = None) -> None:
        """現在の翻訳データをCSVファイルに保存"""
        if file_path is None:
            file_path = self.locales_dir / "strings.csv"
        
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['key'] + self._supported_languages
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for key, translations in self._strings.items():
                row = {'key': key}
                for lang in self._supported_languages:
                    row[lang] = translations.get(lang, '')
                writer.writerow(row)
        
        print(f"Translations saved to {file_path}")
    
    def save_to_yaml(self, file_path: Optional[Path] = None) -> None:
        """現在の翻訳データをYAMLファイルに保存"""
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML is required for YAML support. Install with: pip install PyYAML")
        
        if file_path is None:
            file_path = self.locales_dir / "strings.yaml"
        
        data = {
            "languages": self._supported_languages,
            "strings": self._strings
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        
        print(f"Translations saved to {file_path}")
    
    def export_for_translation(self, language: LanguageCode, file_path: Optional[Path] = None) -> None:
        """特定言語の翻訳用ファイルをエクスポート"""
        if file_path is None:
            file_path = self.locales_dir / f"export_{language}.json"
        
        # 翻訳対象のキーと現在の値を抽出
        export_data = {}
        for key, translations in self._strings.items():
            export_data[key] = translations.get(language, "")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"Translation export for '{language}' saved to {file_path}")
    
    def import_from_translation(self, language: LanguageCode, file_path: Path) -> None:
        """翻訳ファイルからインポート"""
        with open(file_path, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        # データをマージ
        for key, text in import_data.items():
            if key in self._strings:
                self._strings[key][language] = text
            else:
                self._strings[key] = {language: text}
        
        print(f"Translations imported from {file_path}")


# シングルトンインスタンス用
_localization_manager_instance: Optional[LocalizationManager] = None


def get_localization_manager() -> LocalizationManager:
    """LocalizationManagerのシングルトンインスタンスを取得"""
    global _localization_manager_instance
    if _localization_manager_instance is None:
        _localization_manager_instance = LocalizationManager()
    return _localization_manager_instance


def set_localization_manager(manager: LocalizationManager) -> None:
    """LocalizationManagerのシングルトンインスタンスを設定"""
    global _localization_manager_instance
    _localization_manager_instance = manager


# 便利関数
def tr_external(key: str, **kwargs) -> str:
    """外部ファイルベースの翻訳便利関数"""
    return get_localization_manager().get_string(key, **kwargs)