# -*- coding: utf-8 -*-
"""
UI Strings - UI文字列の多言語対応
アプリケーション内で使用される全ての文字列を管理
"""
from typing import Dict, Any
from core.language_manager import get_language_manager, LanguageCode

class UIStrings:
    """UI文字列管理クラス"""
    
    # 文字列定義
    STRINGS: Dict[str, Dict[LanguageCode, str]] = {
        # === アプリケーション基本情報 ===
        "app_title": {
            "ja": "Claude Code PromptUI",
            "en": "Claude Code PromptUI"
        },
        "app_version": {
            "ja": "バージョン 1.0.0",
            "en": "Version 1.0.0"
        },
        
        # === メニュー ===
        "menu_file": {
            "ja": "ファイル(&F)",
            "en": "&File"
        },
        "menu_edit": {
            "ja": "編集(&E)",
            "en": "&Edit"
        },
        "menu_view": {
            "ja": "表示(&V)",
            "en": "&View"
        },
        "menu_settings": {
            "ja": "設定(&S)",
            "en": "&Settings"
        },
        "menu_help": {
            "ja": "ヘルプ(&H)",
            "en": "&Help"
        },
        
        # === ファイルメニュー ===
        "menu_add_workspace": {
            "ja": "ワークスペースを追加(&A)",
            "en": "&Add Workspace"
        },
        "menu_exit": {
            "ja": "終了(&X)",
            "en": "E&xit"
        },
        
        # === 表示メニュー ===
        "menu_theme": {
            "ja": "テーマ(&T)",
            "en": "&Theme"
        },
        "menu_theme_light": {
            "ja": "ライトモード",
            "en": "Light Mode"
        },
        "menu_theme_dark": {
            "ja": "ダークモード",
            "en": "Dark Mode"
        },
        "menu_theme_cyberpunk": {
            "ja": "サイバーパンク",
            "en": "Cyberpunk"
        },
        "menu_theme_nordic": {
            "ja": "ノルディック",
            "en": "Nordic"
        },
        "menu_toggle_preview": {
            "ja": "プレビューの表示/非表示",
            "en": "Toggle Preview"
        },
        
        # === テーマ表示名（個別） ===
        "theme_light_name": {
            "ja": "ライトモード",
            "en": "Light Mode"
        },
        "theme_dark_name": {
            "ja": "ダークモード",
            "en": "Dark Mode"
        },
        "theme_cyberpunk_name": {
            "ja": "サイバーパンク",
            "en": "Cyberpunk"
        },
        "theme_nordic_name": {
            "ja": "ノルディック",
            "en": "Nordic"
        },
        
        # === 設定メニュー ===
        "menu_language": {
            "ja": "言語(&L)",
            "en": "&Language"
        },
        "menu_language_japanese": {
            "ja": "日本語",
            "en": "Japanese"
        },
        "menu_language_english": {
            "ja": "英語",
            "en": "English"
        },
        "menu_path_mode": {
            "ja": "パスモード(&P)",
            "en": "&Path Mode"
        },
        
        # === ヘルプメニュー ===
        "menu_usage": {
            "ja": "使い方(&U)",
            "en": "&Usage"
        },
        "menu_python_env": {
            "ja": "Python実行環境(&P)",
            "en": "&Python Environment"
        },
        "menu_about": {
            "ja": "バージョン情報(&A)",
            "en": "&About"
        },
        
        # === ウィジェットラベル ===
        "label_thinking_level": {
            "ja": "思考レベル:",
            "en": "Thinking Level:"
        },
        "label_path_mode": {
            "ja": "パスモード:",
            "en": "Path Mode:"
        },
        "label_workspace": {
            "ja": "ワークスペース",
            "en": "Workspace"
        },
        "label_preview": {
            "ja": "プレビュー",
            "en": "Preview"
        },
        "label_prompt": {
            "ja": "プロンプト",
            "en": "Prompt"
        },
        
        # === ボタン ===
        "button_add_folder": {
            "ja": "フォルダ追加",
            "en": "Add Folder"
        },
        "button_refresh": {
            "ja": "更新",
            "en": "Refresh"
        },
        "button_generate": {
            "ja": "生成&コピー (Shift+Enter)",
            "en": "Generate & Copy (Shift+Enter)"
        },
        "button_clear": {
            "ja": "クリア",
            "en": "Clear"
        },
        
        # === プロンプト入力 ===
        "prompt_header": {
            "ja": "プロンプト (Enterで改行, Shift+Enterで生成&コピー):",
            "en": "Prompt (Enter for new line, Shift+Enter to generate & copy):"
        },
        "prompt_placeholder": {
            "ja": "プロンプトを入力してください...\n- Enterで改行\n- Shift+Enterで生成&コピー\n- @filename でファイル・フォルダを指定",
            "en": "Enter your prompt...\n- Enter for new line\n- Shift+Enter to generate & copy\n- @filename to specify files/folders"
        },
        "prompt_tokens": {
            "ja": "トークン",
            "en": "tokens"
        },
        
        # === ファイル補完 ===
        "completion_header": {
            "ja": "ファイル・フォルダを選択: (Escで閉じる)",
            "en": "Select file/folder: (Esc to close)"
        },
        "completion_file": {
            "ja": "(ファイル)",
            "en": "(File)"
        },
        "completion_folder": {
            "ja": "(フォルダ)",
            "en": "(Folder)"
        },
        
        # === ファイルツリー ===
        "tree_header": {
            "ja": "プロジェクト",
            "en": "Projects"
        },
        
        # === コンテキストメニュー ===
        "context_remove_workspace": {
            "ja": "ワークスペースを削除",
            "en": "Remove Workspace"
        },
        "context_copy_path": {
            "ja": "パスをコピー",
            "en": "Copy Path"
        },
        
        # === ダイアログ ===
        "dialog_select_folder": {
            "ja": "プロジェクトフォルダを選択",
            "en": "Select Project Folder"
        },
        "dialog_confirm": {
            "ja": "確認",
            "en": "Confirm"
        },
        "dialog_warning": {
            "ja": "警告",
            "en": "Warning"
        },
        "dialog_error": {
            "ja": "エラー",
            "en": "Error"
        },
        "dialog_success": {
            "ja": "成功",
            "en": "Success"
        },
        
        # === メッセージ ===
        "msg_folder_already_exists": {
            "ja": "このフォルダは既に追加されています。",
            "en": "This folder has already been added."
        },
        "msg_confirm_remove_workspace": {
            "ja": "ワークスペースを削除しますか？\\n{path}",
            "en": "Remove workspace?\\n{path}"
        },
        "msg_folders_added": {
            "ja": "{count} 個のフォルダがワークスペースに追加されました",
            "en": "{count} folder(s) added to workspace"
        },
        "msg_no_valid_folders": {
            "ja": "有効なフォルダがドロップされていないか、フォルダが既に存在します",
            "en": "No valid folders were dropped or folders already exist"
        },
        
        # === ステータスメッセージ ===
        "status_ready": {
            "ja": "準備完了",
            "en": "Ready"
        },
        "status_thinking_level_changed": {
            "ja": "思考レベルを '{level}' に変更しました",
            "en": "Thinking level changed to '{level}'"
        },
        "status_path_mode_changed": {
            "ja": "パスモードを '{mode}' に変更しました",
            "en": "Path mode changed to '{mode}'"
        },
        "status_prompt_copied": {
            "ja": "プロンプトをクリップボードにコピーしました ({lines}行, {chars}文字)",
            "en": "Prompt copied to clipboard ({lines} lines, {chars} chars)"
        },
        "status_file_selected": {
            "ja": "選択: {filename}",
            "en": "Selected: {filename}"
        },
        "status_file_added": {
            "ja": "ファイルをプロンプトに追加: {filename}",
            "en": "File added to prompt: {filename}"
        },
        "status_language_changed": {
            "ja": "言語を '{language}' に変更しました",
            "en": "Language changed to '{language}'"
        },
        "status_theme_changed": {
            "ja": "テーマを '{theme}' に変更しました",
            "en": "Theme changed to '{theme}'"
        },
        "status_thinking_level_changed": {
            "ja": "思考レベルを '{level}' に変更しました",
            "en": "Thinking level changed to '{level}'"
        },
        "status_path_mode_changed": {
            "ja": "パスモードを '{mode}' に変更しました",
            "en": "Path mode changed to '{mode}'"
        },
        "status_preview_shown": {
            "ja": "プレビューを表示しました",
            "en": "Preview shown"
        },
        "status_preview_hidden": {
            "ja": "プレビューを非表示にしました",
            "en": "Preview hidden"
        },
        
        # === 使い方ダイアログ ===
        "usage_title": {
            "ja": "使い方",
            "en": "Usage"
        },
        "usage_content": {
            "ja": """Claude Code PromptUI 使い方

■ 基本操作
- Enterで改行
- Shift+Enterで生成&コピー
- @filename でファイルを指定
- 左側のファイルツリーからファイルを選択
- 中央でファイル内容をプレビュー

■ ファイル指定
- @を入力すると補完候補が表示されます
- 矢印キーで選択、Enterで確定
- Escapeで補完をキャンセル

■ 思考レベル
- Claude Codeの思考レベルを設定できます
- think, think harder, think step by step等

■ テーマ
- ライト、ダーク、サイバーパンク、ノルディックから選択

■ ショートカット
- Ctrl+F: フォルダ追加
- Ctrl+R: ファイルツリー更新
- Shift+Enter: プロンプト生成&コピー""",
            "en": """Claude Code PromptUI Usage

■ Basic Operations
- Enter for new line
- Shift+Enter to generate & copy
- @filename to specify files
- Select files from left tree
- Preview file content in center

■ File Specification
- Type @ to show completion candidates
- Use arrow keys to select, Enter to confirm
- Escape to cancel completion

■ Thinking Level
- Set Claude Code thinking level
- think, think harder, think step by step, etc.

■ Themes
- Choose from Light, Dark, Cyberpunk, Nordic

■ Shortcuts
- Ctrl+F: Add folder
- Ctrl+R: Refresh file tree
- Shift+Enter: Generate & copy prompt"""
        },
        
        # === Python環境ダイアログ ===
        "python_env_title": {
            "ja": "Python実行環境",
            "en": "Python Environment"
        },
        "python_env_wsl_header": {
            "ja": "## WSL環境での実行方法",
            "en": "## Execution in WSL Environment"
        },
        "python_env_windows_header": {
            "ja": "## Windows環境での実行方法",
            "en": "## Execution in Windows Environment"
        },
        "python_env_recommended": {
            "ja": "### 推奨実行方法:",
            "en": "### Recommended execution method:"
        },
        "python_env_available": {
            "ja": "### 利用可能なPython実行環境:",
            "en": "### Available Python environments:"
        },
        "python_env_wsl_notes_header": {
            "ja": "### WSL環境でのPython実行の注意点:",
            "en": "### Notes for Python execution in WSL:"
        },
        "python_env_wsl_note1": {
            "ja": "- WSL内のPythonを使用することを推奨します",
            "en": "- We recommend using Python within WSL"
        },
        "python_env_wsl_note2": {
            "ja": "- Windows側のPythonを使用する場合は、パス変換に注意が必要です",
            "en": "- When using Windows Python, be careful with path conversion"
        },
        "python_env_wsl_note3": {
            "ja": "- 依存関係はWSL環境内にインストールしてください:",
            "en": "- Install dependencies within the WSL environment:"
        },
        
        # === バージョン情報ダイアログ ===
        "about_title": {
            "ja": "バージョン情報",
            "en": "About"
        },
        "about_content": {
            "ja": """Claude Code PromptUI

Claude Codeのプロンプト入力を改善するツール

バージョン: 1.0.0
作者: Claude Code User

機能:
- ファイルツリー表示
- ファイル補完機能
- 思考レベル設定
- テーマ切り替え
- プレビュー機能""",
            "en": """Claude Code PromptUI

A tool to improve prompt input for Claude Code

Version: 1.0.0
Author: Claude Code User

Features:
- File tree display
- File completion
- Thinking level settings
- Theme switching
- Preview functionality"""
        }
    }
    
    @classmethod
    def get(cls, key: str, **kwargs) -> str:
        """文字列を取得"""
        language = get_language_manager().get_current_language()
        
        if key not in cls.STRINGS:
            print(f"Warning: UI string key '{key}' not found")
            return key
        
        if language not in cls.STRINGS[key]:
            # フォールバック: 英語を試す
            if "en" in cls.STRINGS[key]:
                language = "en"
            else:
                print(f"Warning: No translation found for key '{key}' in language '{language}'")
                return key
        
        text = cls.STRINGS[key][language]
        
        # プレースホルダーを置換
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError as e:
                print(f"Warning: Missing placeholder {e} in string '{key}'")
        
        return text
    
    @classmethod
    def get_thinking_level_display(cls, level: str) -> str:
        """思考レベルの表示名を取得"""
        language = get_language_manager().get_current_language()
        
        # すべての言語で純粋なレベル名のみを表示（説明なし）
        return level
    
    @classmethod
    def get_path_mode_display(cls, mode: str) -> str:
        """パスモードの表示名を取得"""
        language = get_language_manager().get_current_language()
        
        if language == "ja":
            mode_descriptions = {
                "forward": "Forward (/) - WSL対応",
                "windows": "Windows (\\) - Windows形式",
                "wsl": "WSL (/mnt/c/) - WSL専用"
            }
            return mode_descriptions.get(mode, mode)
        else:
            mode_descriptions = {
                "forward": "Forward (/) - WSL compatible",
                "windows": "Windows (\\) - Windows format", 
                "wsl": "WSL (/mnt/c/) - WSL specific"
            }
            return mode_descriptions.get(mode, mode)

# 便利関数
def tr(key: str, **kwargs) -> str:
    """文字列翻訳の便利関数"""
    return UIStrings.get(key, **kwargs)

if __name__ == "__main__":
    # テスト実行
    from core.language_manager import LanguageManager
    
    print("=== UI Strings Test ===")
    
    # 言語マネージャーのテスト
    manager = LanguageManager()
    
    # 日本語でテスト
    manager.set_language("ja")
    print("Japanese strings:")
    print(f"- App title: {tr('app_title')}")
    print(f"- Menu file: {tr('menu_file')}")
    print(f"- Button generate: {tr('button_generate')}")
    print(f"- Status message: {tr('status_file_added', filename='test.py')}")
    
    # 英語でテスト
    manager.set_language("en")
    print("\nEnglish strings:")
    print(f"- App title: {tr('app_title')}")
    print(f"- Menu file: {tr('menu_file')}")
    print(f"- Button generate: {tr('button_generate')}")
    print(f"- Status message: {tr('status_file_added', filename='test.py')}")
    
    # 思考レベル表示テスト
    print("\nThinking level displays:")
    print(f"- Japanese: {UIStrings.get_thinking_level_display('think harder')}")
    manager.set_language("en")
    print(f"- English: {UIStrings.get_thinking_level_display('think harder')}")