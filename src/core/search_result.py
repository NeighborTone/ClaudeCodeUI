# -*- coding: utf-8 -*-
"""
Search Result - コンテンツ検索結果のデータクラス
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SearchMatch:
    """個々のマッチ結果"""
    line_number: int  # 1-indexed
    line_content: str  # マッチした行の内容
    match_start: int  # マッチ開始位置（行内）
    match_end: int  # マッチ終了位置（行内）
    context_before: List[str] = field(default_factory=list)  # 前後の行
    context_after: List[str] = field(default_factory=list)


@dataclass
class FileSearchResult:
    """ファイル単位の検索結果"""
    file_path: str  # 絶対パス
    relative_path: str  # ワークスペース相対パス
    matches: List[SearchMatch] = field(default_factory=list)

    @property
    def match_count(self) -> int:
        """マッチ数を取得"""
        return len(self.matches)


@dataclass
class SearchResults:
    """検索結果全体"""
    query: str  # 検索クエリ
    file_results: List[FileSearchResult] = field(default_factory=list)
    search_time: float = 0.0  # 検索時間（秒）
    is_regex: bool = False  # 正規表現検索かどうか
    is_case_sensitive: bool = False  # 大文字小文字を区別
    is_word_match: bool = False  # 単語単位マッチ
    truncated: bool = False  # 結果が上限に達したか
    error_message: Optional[str] = None  # エラーメッセージ

    @property
    def total_matches(self) -> int:
        """総マッチ数を取得"""
        return sum(fr.match_count for fr in self.file_results)

    @property
    def file_count(self) -> int:
        """マッチしたファイル数を取得"""
        return len(self.file_results)

    def is_empty(self) -> bool:
        """結果が空かどうか"""
        return len(self.file_results) == 0

    def has_error(self) -> bool:
        """エラーがあるかどうか"""
        return self.error_message is not None


@dataclass
class SearchOptions:
    """検索オプション"""
    query: str = ""
    is_regex: bool = False
    is_case_sensitive: bool = False
    is_word_match: bool = False
    include_patterns: List[str] = field(default_factory=list)  # 含めるファイルパターン（例: *.py）
    exclude_patterns: List[str] = field(default_factory=list)  # 除外パターン
    max_results: int = 1000  # 最大結果数
    context_lines: int = 2  # 前後のコンテキスト行数
    max_file_size: int = 100 * 1024 * 1024  # 100MB

    def validate(self) -> Optional[str]:
        """オプションを検証し、エラーがあればメッセージを返す"""
        if not self.query:
            return "検索クエリが空です"
        if self.max_results <= 0:
            return "最大結果数は正の数である必要があります"
        if self.context_lines < 0:
            return "コンテキスト行数は0以上である必要があります"
        return None
