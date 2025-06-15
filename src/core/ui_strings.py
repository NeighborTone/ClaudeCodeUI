# -*- coding: utf-8 -*-
"""
UI Strings (New) - 外部ファイルベースの多言語対応
既存のUIStringsクラスとの互換性を保ちつつ、外部ファイルから翻訳データを読み込み
"""
from typing import Dict, Any, Optional
from src.core.language_manager import get_language_manager, LanguageCode
from src.core.localization_manager import get_localization_manager


class UIStrings:
    """UI文字列管理クラス（外部ファイルベース）"""
    
    @classmethod
    def get(cls, key: str, **kwargs) -> str:
        """
        文字列を取得（LocalizationManagerに委譲）
        
        Args:
            key: 文字列キー
            **kwargs: プレースホルダー置換用パラメータ
            
        Returns:
            翻訳された文字列
        """
        return get_localization_manager().get_string(key, **kwargs)
    
    @classmethod
    def get_thinking_level_display(cls, level: str) -> str:
        """思考レベルの表示名を取得"""
        # すべての言語で純粋なレベル名のみを表示（説明なし）
        return level


# 便利関数
def tr(key: str, **kwargs) -> str:
    """文字列翻訳の便利関数"""
    return UIStrings.get(key, **kwargs)


# 下位互換性のため旧インターフェースも保持
def get_ui_string(key: str, language: Optional[LanguageCode] = None, **kwargs) -> str:
    """下位互換性用の関数"""
    if language:
        return get_localization_manager().get_string(key, language, **kwargs)
    else:
        return tr(key, **kwargs)


if __name__ == "__main__":
    # テスト実行
    from core.language_manager import LanguageManager, set_language_manager
    from core.localization_manager import LocalizationManager, set_localization_manager
    
    print("=== New UI Strings Test ===")
    
    # マネージャーのセットアップ
    lang_manager = LanguageManager()
    loc_manager = LocalizationManager()
    set_language_manager(lang_manager)
    set_localization_manager(loc_manager)
    
    # 日本語でテスト
    lang_manager.set_language("ja")
    print("Japanese strings:")
    print(f"- App title: {tr('app_title')}")
    print(f"- Menu file: {tr('menu_file')}")
    print(f"- Button generate: {tr('button_generate')}")
    
    # 英語でテスト
    lang_manager.set_language("en")
    print("\nEnglish strings:")
    print(f"- App title: {tr('app_title')}")
    print(f"- Menu file: {tr('menu_file')}")
    print(f"- Button generate: {tr('button_generate')}")
    
