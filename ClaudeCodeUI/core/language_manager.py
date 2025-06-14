# -*- coding: utf-8 -*-
"""
Language Manager - 言語設定管理
アプリケーションの言語設定を管理し、自動検出や手動切り替えを提供
"""
from typing import Literal, Dict, Callable, Optional
from core.environment_detector import EnvironmentDetector

LanguageCode = Literal["ja", "en"]

class LanguageManager:
    """言語設定管理クラス"""
    
    def __init__(self, settings_manager=None):
        """初期化"""
        self.settings_manager = settings_manager
        self._current_language: LanguageCode = "en"
        self._language_change_callbacks: Dict[str, Callable[[LanguageCode], None]] = {}
        
        # 初期言語を設定
        self._initialize_language()
    
    def _initialize_language(self):
        """初期言語を設定"""
        # 設定から言語を読み込み
        if self.settings_manager:
            saved_language = self.settings_manager.get("ui.language", None)
            if saved_language in ["ja", "en"]:
                self._current_language = saved_language
                return
        
        # 自動検出された推奨言語を使用
        recommended = EnvironmentDetector.get_recommended_language()
        self._current_language = recommended
        
        # 設定に保存
        if self.settings_manager:
            self.settings_manager.set("ui.language", self._current_language)
    
    def get_current_language(self) -> LanguageCode:
        """現在の言語を取得"""
        return self._current_language
    
    def set_language(self, language: LanguageCode):
        """言語を設定"""
        if language != self._current_language:
            old_language = self._current_language
            self._current_language = language
            
            # 設定に保存
            if self.settings_manager:
                self.settings_manager.set("ui.language", language)
            
            # コールバックを呼び出し
            self._notify_language_change(old_language, language)
    
    def toggle_language(self):
        """言語を切り替え（日本語⇄英語）"""
        new_language = "en" if self._current_language == "ja" else "ja"
        self.set_language(new_language)
    
    def is_japanese(self) -> bool:
        """現在の言語が日本語かどうか"""
        return self._current_language == "ja"
    
    def is_english(self) -> bool:
        """現在の言語が英語かどうか"""
        return self._current_language == "en"
    
    def register_language_change_callback(self, callback_id: str, callback: Callable[[LanguageCode], None]):
        """言語変更時のコールバックを登録"""
        self._language_change_callbacks[callback_id] = callback
    
    def unregister_language_change_callback(self, callback_id: str):
        """言語変更コールバックを削除"""
        if callback_id in self._language_change_callbacks:
            del self._language_change_callbacks[callback_id]
    
    def _notify_language_change(self, old_language: LanguageCode, new_language: LanguageCode):
        """言語変更をコールバックに通知"""
        for callback in self._language_change_callbacks.values():
            try:
                callback(new_language)
            except Exception as e:
                print(f"Language change callback error: {e}")
    
    def get_language_name(self, language: Optional[LanguageCode] = None) -> str:
        """言語名を取得"""
        lang = language or self._current_language
        if lang == "ja":
            return "日本語" if self.is_japanese() else "Japanese"
        else:
            return "English" if self.is_english() else "英語"
    
    def get_language_info(self) -> Dict:
        """言語情報を取得"""
        env_info = EnvironmentDetector.get_environment_info()
        return {
            "current_language": self._current_language,
            "language_name": self.get_language_name(),
            "environment": env_info["environment"],
            "has_japanese_font": env_info["has_japanese_font"],
            "recommended_language": EnvironmentDetector.get_recommended_language(),
            "is_auto_detected": self._current_language == EnvironmentDetector.get_recommended_language()
        }

# グローバルインスタンス（シングルトンパターン）
_language_manager_instance: Optional[LanguageManager] = None

def get_language_manager(settings_manager=None) -> LanguageManager:
    """LanguageManagerのグローバルインスタンスを取得"""
    global _language_manager_instance
    if _language_manager_instance is None:
        _language_manager_instance = LanguageManager(settings_manager)
    return _language_manager_instance

def set_language_manager(language_manager: LanguageManager):
    """LanguageManagerのグローバルインスタンスを設定"""
    global _language_manager_instance
    _language_manager_instance = language_manager

# 便利関数
def get_current_language() -> LanguageCode:
    """現在の言語を取得"""
    return get_language_manager().get_current_language()

def is_japanese() -> bool:
    """現在の言語が日本語かどうか"""
    return get_language_manager().is_japanese()

def is_english() -> bool:
    """現在の言語が英語かどうか"""
    return get_language_manager().is_english()

if __name__ == "__main__":
    # テスト実行
    print("=== Language Manager Test ===")
    
    # 環境情報を表示
    from core.environment_detector import EnvironmentDetector
    print(f"Environment: {EnvironmentDetector.detect_environment()}")
    print(f"Has Japanese font: {EnvironmentDetector.has_japanese_font_support()}")
    print(f"Recommended language: {EnvironmentDetector.get_recommended_language()}")
    
    # LanguageManagerのテスト
    manager = LanguageManager()
    print(f"Initial language: {manager.get_current_language()}")
    print(f"Language name: {manager.get_language_name()}")
    
    # 言語切り替えテスト
    manager.set_language("ja")
    print(f"After setting to Japanese: {manager.get_current_language()}")
    print(f"Language name: {manager.get_language_name()}")
    
    manager.set_language("en")
    print(f"After setting to English: {manager.get_current_language()}")
    print(f"Language name: {manager.get_language_name()}")
    
    # 言語情報
    print("\n=== Language Info ===")
    import json
    info = manager.get_language_info()
    print(json.dumps(info, indent=2, ensure_ascii=False))