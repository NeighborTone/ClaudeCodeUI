# -*- coding: utf-8 -*-
"""
Template Manager - 定型文管理システム
プリプロンプトとポストプロンプトのテンプレート管理
"""
import os
import json
import yaml
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
            app_dir = Path(__file__).parent.parent.parent  # Go up to project root
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
            # YAMLファイルを読み込み
            for file_path in pre_dir.glob("*.yaml"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict) and 'title' in data and 'content' in data:
                            self._pre_templates[data['title']] = data['content']
                except (yaml.YAMLError, KeyError, OSError) as e:
                    print(f"Warning: Failed to load pre-template {file_path}: {e}")
            
            # JSONファイルも読み込み（下位互換性）
            for file_path in pre_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'title' in data and 'content' in data:
                            # YAMLファイルが既に存在する場合はスキップ
                            yaml_path = file_path.with_suffix('.yaml')
                            if not yaml_path.exists():
                                self._pre_templates[data['title']] = data['content']
                except (json.JSONDecodeError, KeyError, OSError) as e:
                    print(f"Warning: Failed to load pre-template {file_path}: {e}")
        
        # ポストプロンプトテンプレートを読み込み
        post_dir = self.templates_dir / "post"
        if post_dir.exists():
            # YAMLファイルを読み込み
            for file_path in post_dir.glob("*.yaml"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict) and 'title' in data and 'content' in data:
                            self._post_templates[data['title']] = data['content']
                except (yaml.YAMLError, KeyError, OSError) as e:
                    print(f"Warning: Failed to load post-template {file_path}: {e}")
            
            # JSONファイルも読み込み（下位互換性）
            for file_path in post_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'title' in data and 'content' in data:
                            # YAMLファイルが既に存在する場合はスキップ
                            yaml_path = file_path.with_suffix('.yaml')
                            if not yaml_path.exists():
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
        新しいテンプレートを作成（YAML形式で保存）
        
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
        file_path = template_dir / f"{safe_title}.yaml"
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(template_data, f, default_flow_style=False, 
                         allow_unicode=True, indent=2, sort_keys=False)
            
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
        テンプレートを削除（YAMLとJSONファイル両方をチェック）
        
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
        
        # ファイルを削除（YAMLファイルを優先）
        template_dir = self.templates_dir / template_type
        deleted = False
        
        # YAMLファイルをチェック
        for file_path in template_dir.glob("*.yaml"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict) and data.get('title') == title:
                        file_path.unlink()
                        deleted = True
            except (yaml.YAMLError, KeyError, OSError):
                continue
        
        # JSONファイルもチェック（YAMLが見つからなかった場合）
        if not deleted:
            for file_path in template_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get('title') == title:
                            file_path.unlink()
                            deleted = True
                except (json.JSONDecodeError, KeyError, OSError):
                    continue
        
        return deleted
    
    def build_final_prompt(self, pre_template: Optional[str],
                          main_content: str, post_template: Optional[str]) -> str:
        """
        最終的なプロンプトを構築

        Args:
            pre_template: プリプロンプトテンプレート名（Noneの場合は追加しない）
            main_content: メインコンテンツ
            post_template: ポストプロンプトテンプレート名（Noneの場合は追加しない）

        Returns:
            構築されたプロンプト
        """
        parts = []

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
        pre_template="Code Review",
        main_content="def hello_world():\n    print('Hello, World!')",
        post_template="Explanation Request"
    )
    print("Final prompt:")
    print(final_prompt)