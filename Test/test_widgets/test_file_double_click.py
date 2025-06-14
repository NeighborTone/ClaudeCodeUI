#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for file double-click functionality
テスト対象：ファイルダブルクリック時の相対パス取得とオートコンプリート無効化
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add path for module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ClaudeCodeUI'))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from core.workspace_manager import WorkspaceManager
from core.path_converter import PathConverter
from widgets.prompt_input import PromptInputWidget
from ui.main_window import MainWindow

class TestFileDoubleClick:
    """ファイルダブルクリック機能のテストクラス"""
    
    def __init__(self):
        self.temp_dir = None
        self.workspace_manager = None
        self.main_window = None
        self.app = None
        
    def setup_test_environment(self):
        """テスト環境のセットアップ"""
        print("Setting up test environment...")
        
        # QApplicationの作成
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        # 一時ディレクトリの作成
        self.temp_dir = tempfile.mkdtemp(prefix="claude_test_")
        print(f"Temporary directory: {self.temp_dir}")
        
        # テスト用ファイル構造を作成
        test_structure = {
            "project_root": {
                "src": {
                    "main.py": "# Main application file",
                    "utils": {
                        "helper.py": "# Helper functions",
                        "__init__.py": ""
                    }
                },
                "tests": {
                    "test_main.py": "# Test file",
                },
                "README.md": "# Project README"
            }
        }
        
        self._create_file_structure(self.temp_dir, test_structure)
        
        # ワークスペースマネージャーの初期化
        self.workspace_manager = WorkspaceManager()
        project_root = os.path.join(self.temp_dir, "project_root")
        self.workspace_manager.add_workspace(project_root)
        
        # MainWindowの作成
        self.main_window = MainWindow()
        self.main_window.workspace_manager = self.workspace_manager
        
        print("Test environment setup complete!")
        
    def _create_file_structure(self, base_path, structure):
        """ファイル構造を再帰的に作成"""
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                self._create_file_structure(path, content)
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    def test_workspace_relative_path_calculation(self):
        """ワークスペース相対パス計算のテスト"""
        print("\n=== Testing workspace relative path calculation ===")
        
        project_root = os.path.join(self.temp_dir, "project_root")
        test_file = os.path.join(project_root, "src", "utils", "helper.py")
        
        print(f"Project root: {project_root}")
        print(f"Test file: {test_file}")
        
        # 相対パスを計算
        relative_path = os.path.relpath(test_file, project_root)
        print(f"Calculated relative path: {relative_path}")
        
        # PathConverterでパスを変換
        converted_path = PathConverter.convert_path(relative_path, "forward")
        print(f"Converted path: {converted_path}")
        
        # 期待値と比較
        expected_path = "src/utils/helper.py"
        if converted_path == expected_path:
            print("✅ Workspace relative path calculation: PASSED")
            return True
        else:
            print(f"❌ Expected: {expected_path}, Got: {converted_path}")
            return False
    
    def test_file_double_click_functionality(self):
        """ファイルダブルクリック機能のテスト"""
        print("\n=== Testing file double-click functionality ===")
        
        project_root = os.path.join(self.temp_dir, "project_root")
        test_file = os.path.join(project_root, "src", "main.py")
        
        print(f"Simulating double-click on: {test_file}")
        
        # 初期状態でプロンプトをクリア
        self.main_window.prompt_input.set_prompt_text("")
        
        # ファイルダブルクリックをシミュレート
        self.main_window.on_file_double_clicked(test_file)
        
        # 結果を取得
        result_text = self.main_window.prompt_input.get_prompt_text()
        print(f"Result text: '{result_text}'")
        
        # 期待値と比較
        expected_text = "@src/main.py"
        if result_text == expected_text:
            print("✅ File double-click functionality: PASSED")
            return True
        else:
            print(f"❌ Expected: '{expected_text}', Got: '{result_text}'")
            return False
    
    def test_autocompletion_disabled(self):
        """オートコンプリート無効化のテスト"""
        print("\n=== Testing autocompletion disabled during file insertion ===")
        
        project_root = os.path.join(self.temp_dir, "project_root")
        test_file = os.path.join(project_root, "README.md")
        
        # プロンプト入力ウィジェットの補完状態を確認
        prompt_widget = self.main_window.prompt_input
        
        # 補完が非アクティブであることを確認
        initial_completion_active = prompt_widget.completion_active
        print(f"Initial completion active: {initial_completion_active}")
        
        # ファイルダブルクリックを実行
        self.main_window.on_file_double_clicked(test_file)
        
        # 補完が非アクティブのままであることを確認
        final_completion_active = prompt_widget.completion_active
        print(f"Final completion active: {final_completion_active}")
        
        # 補完ウィジェットが隠れていることを確認
        completion_visible = prompt_widget.completion_widget.isVisible()
        print(f"Completion widget visible: {completion_visible}")
        
        if not final_completion_active and not completion_visible:
            print("✅ Autocompletion disabled during file insertion: PASSED")
            return True
        else:
            print("❌ Autocompletion should be disabled during file insertion")
            return False
    
    def test_multiple_file_insertions(self):
        """複数ファイル挿入のテスト"""
        print("\n=== Testing multiple file insertions ===")
        
        project_root = os.path.join(self.temp_dir, "project_root")
        
        # 最初のファイル
        file1 = os.path.join(project_root, "src", "main.py")
        self.main_window.prompt_input.set_prompt_text("")
        self.main_window.on_file_double_clicked(file1)
        result1 = self.main_window.prompt_input.get_prompt_text()
        print(f"After first file: '{result1}'")
        
        # 2番目のファイル
        file2 = os.path.join(project_root, "tests", "test_main.py")
        self.main_window.on_file_double_clicked(file2)
        result2 = self.main_window.prompt_input.get_prompt_text()
        print(f"After second file: '{result2}'")
        
        # 期待値
        expected_result = "@src/main.py\n\n@tests/test_main.py"
        
        if result2 == expected_result:
            print("✅ Multiple file insertions: PASSED")
            return True
        else:
            print(f"❌ Expected: '{expected_result}', Got: '{result2}'")
            return False
    
    def cleanup_test_environment(self):
        """テスト環境のクリーンアップ"""
        print("\nCleaning up test environment...")
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print(f"Removed temporary directory: {self.temp_dir}")
    
    def run_all_tests(self):
        """全テストの実行"""
        print("=" * 60)
        print("FILE DOUBLE-CLICK FUNCTIONALITY TEST")
        print("=" * 60)
        
        try:
            self.setup_test_environment()
            
            # テストの実行
            test_results = []
            test_results.append(self.test_workspace_relative_path_calculation())
            test_results.append(self.test_file_double_click_functionality())
            test_results.append(self.test_autocompletion_disabled())
            test_results.append(self.test_multiple_file_insertions())
            
            # 結果の集計
            passed_tests = sum(test_results)
            total_tests = len(test_results)
            
            print("\n" + "=" * 60)
            print("TEST RESULTS")
            print("=" * 60)
            print(f"Passed: {passed_tests}/{total_tests}")
            
            if passed_tests == total_tests:
                print("🎉 ALL TESTS PASSED!")
                return True
            else:
                print("❌ Some tests failed")
                return False
                
        except Exception as e:
            print(f"Test execution failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.cleanup_test_environment()

def main():
    """メイン関数"""
    tester = TestFileDoubleClick()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ Test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()