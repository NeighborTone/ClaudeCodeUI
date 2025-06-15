# -*- coding: utf-8 -*-
"""
Template Manager - 定型文管理システム
プリプロンプトとポストプロンプトのテンプレート管理
"""
import os
import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class TemplateManager:
    """定型文管理クラス"""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        初期化
        
        Args:
            templates_dir: テンプレート格納ディレクトリ（指定しない場合はデフォルト）
        """
        if templates_dir is None:
            # アプリケーションディレクトリ内のtemplatesフォルダ
            app_dir = Path(__file__).parent.parent
            self.templates_dir = app_dir / "templates"
        else:
            self.templates_dir = Path(templates_dir)
        
        # テンプレート格納用辞書
        self._pre_templates: Dict[str, str] = {}
        self._post_templates: Dict[str, str] = {}
        
        # テンプレートディレクトリが存在しない場合は作成
        self.templates_dir.mkdir(exist_ok=True)
        (self.templates_dir / "pre").mkdir(exist_ok=True)
        (self.templates_dir / "post").mkdir(exist_ok=True)
        
        # テンプレートを読み込み
        self.reload_templates()
    
    def reload_templates(self) -> None:
        """テンプレートを再読み込み"""
        self._pre_templates.clear()
        self._post_templates.clear()
        
        # プリプロンプトテンプレートを読み込み
        pre_dir = self.templates_dir / "pre"
        if pre_dir.exists():
            for file_path in pre_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'title' in data and 'content' in data:
                            self._pre_templates[data['title']] = data['content']
                except (json.JSONDecodeError, KeyError, OSError) as e:
                    print(f"Warning: Failed to load pre-template {file_path}: {e}")
        
        # ポストプロンプトテンプレートを読み込み
        post_dir = self.templates_dir / "post"
        if post_dir.exists():
            for file_path in post_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'title' in data and 'content' in data:
                            self._post_templates[data['title']] = data['content']
                except (json.JSONDecodeError, KeyError, OSError) as e:
                    print(f"Warning: Failed to load post-template {file_path}: {e}")
    
    def get_pre_template_names(self) -> List[str]:
        """プリプロンプトテンプレート名一覧を取得"""
        return sorted(self._pre_templates.keys())
    
    def get_post_template_names(self) -> List[str]:
        """ポストプロンプトテンプレート名一覧を取得"""
        return sorted(self._post_templates.keys())
    
    def get_pre_template_content(self, name: str) -> Optional[str]:
        """
        プリプロンプトテンプレートの内容を取得
        
        Args:
            name: テンプレート名
            
        Returns:
            テンプレート内容（存在しない場合はNone）
        """
        return self._pre_templates.get(name)
    
    def get_post_template_content(self, name: str) -> Optional[str]:
        """
        ポストプロンプトテンプレートの内容を取得
        
        Args:
            name: テンプレート名
            
        Returns:
            テンプレート内容（存在しない場合はNone）
        """
        return self._post_templates.get(name)
    
    def create_template(self, template_type: str, title: str, content: str) -> bool:
        """
        新しいテンプレートを作成
        
        Args:
            template_type: "pre" または "post"
            title: テンプレートタイトル
            content: テンプレート内容
            
        Returns:
            作成成功可否
        """
        if template_type not in ["pre", "post"]:
            return False
        
        # ファイル名として使用できるようにタイトルをサニタイズ
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')
        
        template_data = {
            "title": title,
            "content": content
        }
        
        template_dir = self.templates_dir / template_type
        file_path = template_dir / f"{safe_title}.json"
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)
            
            # メモリ内のテンプレートも更新
            if template_type == "pre":
                self._pre_templates[title] = content
            else:
                self._post_templates[title] = content
            
            return True
        except OSError as e:
            print(f"Error: Failed to create template {file_path}: {e}")
            return False
    
    def delete_template(self, template_type: str, title: str) -> bool:
        """
        テンプレートを削除
        
        Args:
            template_type: "pre" または "post"
            title: テンプレートタイトル
            
        Returns:
            削除成功可否
        """
        if template_type not in ["pre", "post"]:
            return False
        
        # メモリからも削除
        if template_type == "pre":
            if title in self._pre_templates:
                del self._pre_templates[title]
            else:
                return False
        else:
            if title in self._post_templates:
                del self._post_templates[title]
            else:
                return False
        
        # ファイルを削除
        template_dir = self.templates_dir / template_type
        for file_path in template_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('title') == title:
                        file_path.unlink()
                        return True
            except (json.JSONDecodeError, KeyError, OSError):
                continue
        
        return False
    
    def build_final_prompt(self, thinking_level: str, pre_template: Optional[str], 
                          main_content: str, post_template: Optional[str]) -> str:
        """
        最終的なプロンプトを構築
        
        Args:
            thinking_level: 思考レベル（"none"の場合は追加しない）
            pre_template: プリプロンプトテンプレート名（Noneの場合は追加しない）
            main_content: メインコンテンツ
            post_template: ポストプロンプトテンプレート名（Noneの場合は追加しない）
            
        Returns:
            構築されたプロンプト
        """
        parts = []
        
        # 思考レベルを追加
        if thinking_level and thinking_level.lower() != "none":
            parts.append(thinking_level)
        
        # プリプロンプトを追加
        if pre_template:
            pre_content = self.get_pre_template_content(pre_template)
            if pre_content:
                parts.append(pre_content)
        
        # メインコンテンツを追加
        if main_content.strip():
            parts.append(main_content.strip())
        
        # ポストプロンプトを追加
        if post_template:
            post_content = self.get_post_template_content(post_template)
            if post_content:
                parts.append(post_content)
        
        # 空行で結合
        return "\n\n".join(parts)
    
    def get_templates_directory(self) -> Path:
        """テンプレートディレクトリのパスを取得"""
        return self.templates_dir
    
    def create_sample_templates(self) -> None:
        """サンプルテンプレートを作成"""
        # サンプルプリプロンプトテンプレート
        sample_pre_templates = [
            {
                "title": "Code Review",
                "content": "Please review the following code carefully and provide suggestions for improvement, focusing on:\n- Code quality and best practices\n- Performance optimizations\n- Security considerations\n- Maintainability"
            },
            {
                "title": "Bug Analysis",
                "content": "Please analyze the following code to identify potential bugs and issues:\n- Logic errors\n- Edge cases\n- Memory leaks\n- Race conditions"
            },
            {
                "title": "Documentation",
                "content": "Please help me create comprehensive documentation for the following code:\n- Function/method descriptions\n- Parameter explanations\n- Usage examples\n- Best practices"
            }
        ]
        
        # サンプルポストプロンプトテンプレート
        sample_post_templates = [
            {
                "title": "Explanation Request",
                "content": "Please provide a clear, step-by-step explanation of your solution and reasoning."
            },
            {
                "title": "Alternative Solutions",
                "content": "Please also suggest alternative approaches or solutions to this problem."
            },
            {
                "title": "Testing Guidance",
                "content": "Please provide guidance on how to test this code, including edge cases to consider."
            }
        ]
        
        # サンプルテンプレートを作成
        for template in sample_pre_templates:
            self.create_template("pre", template["title"], template["content"])
        
        for template in sample_post_templates:
            self.create_template("post", template["title"], template["content"])


# シングルトンインスタンス用
_template_manager_instance: Optional[TemplateManager] = None

def get_template_manager() -> TemplateManager:
    """テンプレートマネージャーのシングルトンインスタンスを取得"""
    global _template_manager_instance
    if _template_manager_instance is None:
        _template_manager_instance = TemplateManager()
    return _template_manager_instance


if __name__ == "__main__":
    # テスト実行
    print("=== Template Manager Test ===")
    
    manager = TemplateManager()
    
    # サンプルテンプレートを作成
    manager.create_sample_templates()
    
    # テンプレート一覧を表示
    print("\nPre-templates:")
    for name in manager.get_pre_template_names():
        content = manager.get_pre_template_content(name)
        print(f"- {name}: {content[:50]}...")
    
    print("\nPost-templates:")
    for name in manager.get_post_template_names():
        content = manager.get_post_template_content(name)
        print(f"- {name}: {content[:50]}...")
    
    # プロンプト構築テスト
    print("\n=== Prompt Building Test ===")
    final_prompt = manager.build_final_prompt(
        thinking_level="think step by step",
        pre_template="Code Review",
        main_content="def hello_world():\n    print('Hello, World!')",
        post_template="Explanation Request"
    )
    print("Final prompt:")
    print(final_prompt)