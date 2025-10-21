"""Type definitions for ClaudeCodeUI application.

This module provides TypedDict definitions for common data structures
used throughout the application, improving type safety and IDE support.
"""

from typing import TypedDict, Literal, Optional, Any


# File and folder information types
class FileInfo(TypedDict):
    """ファイル情報を表す型定義"""
    name: str
    path: str
    relative_path: str
    workspace: str
    type: Literal['file']
    size: Optional[int]


class FolderInfo(TypedDict):
    """フォルダ情報を表す型定義"""
    name: str
    path: str
    relative_path: str
    workspace: str
    type: Literal['folder']


class FileEntry(TypedDict):
    """ファイルエントリ（ファイルまたはフォルダ）を表す型定義"""
    name: str
    path: str
    relative_path: str
    workspace: str
    type: Literal['file', 'folder']


# Search result types
class SearchResult(TypedDict):
    """検索結果を表す型定義"""
    name: str
    path: str
    relative_path: str
    workspace: str
    type: Literal['file', 'folder']
    score: float
    match_type: Literal['exact', 'prefix', 'fuzzy']


# Workspace types
class WorkspaceInfo(TypedDict):
    """ワークスペース情報を表す型定義"""
    path: str
    name: str
    folders: list[str]
    files_count: int
    last_scanned: Optional[str]


# Settings types
class WindowSettings(TypedDict, total=False):
    """ウィンドウ設定を表す型定義"""
    width: int
    height: int
    x: int
    y: int
    geometry: str
    state: str


class UISettings(TypedDict, total=False):
    """UI設定を表す型定義"""
    theme: str
    language: Literal['ja', 'en']
    thinking_level: str
    font_family: str
    font_size: int
    preview_visible: bool


class IndexingSettings(TypedDict, total=False):
    """インデックス設定を表す型定義"""
    enabled: bool
    batch_size: int
    max_file_size_mb: int
    excluded_dirs: list[str]
    allowed_extensions: list[str]


class SettingsDict(TypedDict, total=False):
    """アプリケーション設定全体を表す型定義"""
    window: WindowSettings
    ui: UISettings
    indexing: IndexingSettings
    workspace: dict[str, Any]


# Template types
class TemplateInfo(TypedDict):
    """テンプレート情報を表す型定義"""
    title: str
    content: str
    path: Optional[str]


# History types
class PromptHistoryEntry(TypedDict):
    """プロンプト履歴エントリを表す型定義"""
    timestamp: str
    prompt: str
    thinking_level: str
    templates: dict[str, str]
    token_count: int


# Tree node types (for file tree)
class TreeNodeData(TypedDict, total=False):
    """ツリーノードデータを表す型定義"""
    type: Literal['workspace', 'folder', 'file', 'placeholder']
    path: str
    name: str
    is_loaded: bool
    has_children: bool
    is_placeholder: bool


# Database query result types
class DBFileEntry(TypedDict):
    """データベースファイルエントリを表す型定義"""
    id: int
    workspace_path: str
    relative_path: str
    file_name: str
    file_type: Literal['file', 'folder']
    size: Optional[int]
    last_modified: Optional[str]


# Indexing progress types
class IndexingProgress(TypedDict):
    """インデックス作成進捗を表す型定義"""
    current: int
    total: int
    percentage: float
    current_file: str
    workspace: str


# Language types
LanguageCode = Literal['ja', 'en']
ThinkingLevel = Literal[
    'think',
    'think more',
    'think harder',
    'think deeply',
    'think extremely',
    'think extensively',
    'think thoroughly',
    'think massively',
    'think intensely',
    'think profoundly',
    'think comprehensively',
    'think meticulously',
    'ultrathink',
    'suprathink'
]
