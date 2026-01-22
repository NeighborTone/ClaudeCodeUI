# -*- coding: utf-8 -*-
"""
Content Searcher - ripgrep優先、Pythonフォールバックのコンテンツ検索エンジン
"""
import os
import re
import json
import shutil
import subprocess
import time
from typing import List, Optional, Callable, Tuple
from pathlib import Path
from functools import lru_cache

from src.core.search_result import (
    SearchMatch,
    FileSearchResult,
    SearchResults,
    SearchOptions,
)
from src.core.logger import get_logger

logger = get_logger(__name__)


class ContentSearcher:
    """ファイル内コンテンツ検索エンジン"""

    # デフォルトの除外パターン
    DEFAULT_EXCLUDE_PATTERNS = [
        "node_modules",
        "__pycache__",
        ".git",
        ".svn",
        ".hg",
        "Binaries",
        "Intermediate",
        "DerivedDataCache",
        ".vs",
        "obj",
        "bin",
        "build",
        "dist",
        "out",
    ]

    def __init__(self):
        self._ripgrep_path: Optional[str] = None
        self._ripgrep_available: Optional[bool] = None
        self._cancel_requested = False

    @property
    def ripgrep_available(self) -> bool:
        """ripgrepが利用可能かどうか"""
        if self._ripgrep_available is None:
            self._check_ripgrep()
        return self._ripgrep_available

    def _check_ripgrep(self) -> None:
        """ripgrepの存在をチェック"""
        # rgコマンドを探す
        rg_path = shutil.which("rg")
        if rg_path:
            self._ripgrep_path = rg_path
            self._ripgrep_available = True
            logger.info(f"ripgrepが見つかりました: {rg_path}")
        else:
            self._ripgrep_path = None
            self._ripgrep_available = False
            logger.info("ripgrepが見つかりません。Pythonフォールバックを使用します")

    def cancel(self) -> None:
        """検索をキャンセル"""
        self._cancel_requested = True

    def reset_cancel(self) -> None:
        """キャンセル状態をリセット"""
        self._cancel_requested = False

    def search(
        self,
        search_paths: List[str],
        options: SearchOptions,
        progress_callback: Optional[Callable[[float, str], None]] = None,
    ) -> SearchResults:
        """
        コンテンツ検索を実行

        Args:
            search_paths: 検索対象のパスリスト
            options: 検索オプション
            progress_callback: 進捗コールバック (progress%, message)

        Returns:
            SearchResults: 検索結果
        """
        self.reset_cancel()
        start_time = time.time()

        # オプション検証
        validation_error = options.validate()
        if validation_error:
            return SearchResults(
                query=options.query,
                error_message=validation_error,
            )

        # 検索パスのフィルタリング（存在するパスのみ）
        valid_paths = [p for p in search_paths if os.path.exists(p)]
        if not valid_paths:
            return SearchResults(
                query=options.query,
                error_message="有効な検索パスがありません",
            )

        # ripgrep or Python検索
        if self.ripgrep_available:
            results = self._search_with_ripgrep(valid_paths, options, progress_callback)
        else:
            results = self._search_with_python(valid_paths, options, progress_callback)

        results.search_time = time.time() - start_time
        return results

    def _search_with_ripgrep(
        self,
        search_paths: List[str],
        options: SearchOptions,
        progress_callback: Optional[Callable[[float, str], None]] = None,
    ) -> SearchResults:
        """ripgrepを使用した検索"""
        if progress_callback:
            progress_callback(0, "ripgrepで検索中...")

        # ripgrepコマンドを構築
        cmd = [self._ripgrep_path, "--json"]

        # オプション
        if not options.is_case_sensitive:
            cmd.append("-i")

        if options.is_regex:
            # ripgrepはデフォルトで正規表現
            pass
        else:
            # 固定文字列検索
            cmd.append("-F")

        if options.is_word_match:
            cmd.append("-w")

        # コンテキスト行
        if options.context_lines > 0:
            cmd.extend(["-B", str(options.context_lines)])
            cmd.extend(["-A", str(options.context_lines)])

        # 最大結果数
        cmd.extend(["-m", str(options.max_results)])

        # ファイルサイズ制限
        cmd.extend(["--max-filesize", f"{options.max_file_size}"])

        # 含めるパターン
        for pattern in options.include_patterns:
            cmd.extend(["-g", pattern])

        # 除外パターン
        exclude_patterns = (
            options.exclude_patterns
            if options.exclude_patterns
            else self.DEFAULT_EXCLUDE_PATTERNS
        )
        for pattern in exclude_patterns:
            cmd.extend(["-g", f"!{pattern}"])
            cmd.extend(["-g", f"!**/{pattern}/**"])

        # 検索クエリ
        cmd.append(options.query)

        # 検索パス
        cmd.extend(search_paths)

        logger.debug(f"ripgrepコマンド: {' '.join(cmd)}")

        try:
            # ripgrepを実行
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            results = SearchResults(
                query=options.query,
                is_regex=options.is_regex,
                is_case_sensitive=options.is_case_sensitive,
                is_word_match=options.is_word_match,
            )

            file_results_map = {}
            match_count = 0
            context_buffer = {}  # パス -> (before_lines, after_lines_needed)

            # 出力を行単位で処理
            for line in process.stdout:
                if self._cancel_requested:
                    process.terminate()
                    break

                line = line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)
                    msg_type = data.get("type")

                    if msg_type == "match":
                        match_data = data.get("data", {})
                        file_path = match_data.get("path", {}).get("text", "")
                        line_number = match_data.get("line_number", 0)
                        line_content = match_data.get("lines", {}).get("text", "").rstrip("\n\r")

                        # マッチ位置を取得
                        submatches = match_data.get("submatches", [])
                        if submatches:
                            match_start = submatches[0].get("start", 0)
                            match_end = submatches[0].get("end", len(line_content))
                        else:
                            match_start = 0
                            match_end = len(line_content)

                        # ファイル結果を取得または作成
                        if file_path not in file_results_map:
                            # 相対パスを計算
                            relative_path = self._compute_relative_path(
                                file_path, search_paths
                            )
                            file_results_map[file_path] = FileSearchResult(
                                file_path=file_path,
                                relative_path=relative_path,
                            )

                        file_result = file_results_map[file_path]

                        # コンテキスト情報を取得
                        context_before = context_buffer.get(file_path, {}).get(
                            "before", []
                        )

                        match = SearchMatch(
                            line_number=line_number,
                            line_content=line_content,
                            match_start=match_start,
                            match_end=match_end,
                            context_before=context_before.copy(),
                            context_after=[],
                        )
                        file_result.matches.append(match)
                        match_count += 1

                        # コンテキストバッファをクリア
                        context_buffer[file_path] = {"before": [], "last_match": match}

                    elif msg_type == "context":
                        # コンテキスト行
                        context_data = data.get("data", {})
                        file_path = context_data.get("path", {}).get("text", "")
                        line_content = (
                            context_data.get("lines", {}).get("text", "").rstrip("\n\r")
                        )

                        if file_path not in context_buffer:
                            context_buffer[file_path] = {"before": [], "last_match": None}

                        buf = context_buffer[file_path]
                        if buf.get("last_match"):
                            # 直前のマッチのafter contextに追加
                            buf["last_match"].context_after.append(line_content)
                        else:
                            # before contextに追加
                            buf["before"].append(line_content)
                            # 制限
                            if len(buf["before"]) > options.context_lines:
                                buf["before"] = buf["before"][-options.context_lines :]

                    elif msg_type == "summary":
                        # 検索完了のサマリー
                        pass

                except json.JSONDecodeError:
                    continue

            process.wait()

            # 結果を整理
            results.file_results = list(file_results_map.values())
            results.truncated = match_count >= options.max_results

            if progress_callback:
                progress_callback(100, f"検索完了: {match_count}件")

            return results

        except Exception as e:
            logger.error(f"ripgrep検索エラー: {e}")
            return SearchResults(
                query=options.query,
                error_message=f"ripgrep検索エラー: {str(e)}",
            )

    def _search_with_python(
        self,
        search_paths: List[str],
        options: SearchOptions,
        progress_callback: Optional[Callable[[float, str], None]] = None,
    ) -> SearchResults:
        """Pythonを使用した検索（フォールバック）"""
        if progress_callback:
            progress_callback(0, "Python検索エンジンで検索中...")

        results = SearchResults(
            query=options.query,
            is_regex=options.is_regex,
            is_case_sensitive=options.is_case_sensitive,
            is_word_match=options.is_word_match,
        )

        # 正規表現パターンをコンパイル
        try:
            pattern = self._compile_pattern(options)
        except re.error as e:
            results.error_message = f"正規表現エラー: {str(e)}"
            return results

        # 除外パターン
        exclude_patterns = (
            options.exclude_patterns
            if options.exclude_patterns
            else self.DEFAULT_EXCLUDE_PATTERNS
        )

        # 含めるパターンをコンパイル
        include_patterns = [
            self._glob_to_regex(p) for p in options.include_patterns
        ] if options.include_patterns else []

        file_results_map = {}
        total_matches = 0
        files_searched = 0

        # ファイルを列挙
        all_files = []
        for search_path in search_paths:
            if os.path.isfile(search_path):
                all_files.append(search_path)
            elif os.path.isdir(search_path):
                for root, dirs, files in os.walk(search_path):
                    # 除外ディレクトリをスキップ
                    dirs[:] = [
                        d
                        for d in dirs
                        if not any(
                            self._matches_pattern(d, ep) for ep in exclude_patterns
                        )
                    ]

                    for filename in files:
                        file_path = os.path.join(root, filename)

                        # 除外パターンをチェック
                        if any(
                            self._matches_pattern(filename, ep)
                            for ep in exclude_patterns
                        ):
                            continue

                        # 含めるパターンをチェック
                        if include_patterns:
                            if not any(
                                re.match(ip, filename) for ip in include_patterns
                            ):
                                continue

                        all_files.append(file_path)

        total_files = len(all_files)

        # ファイルを検索
        for file_idx, file_path in enumerate(all_files):
            if self._cancel_requested:
                break

            if total_matches >= options.max_results:
                results.truncated = True
                break

            # 進捗報告
            if progress_callback and total_files > 0:
                progress = (file_idx / total_files) * 100
                progress_callback(progress, f"検索中: {os.path.basename(file_path)}")

            # ファイルサイズチェック
            try:
                file_size = os.path.getsize(file_path)
                if file_size > options.max_file_size:
                    continue
            except OSError:
                continue

            # ファイルを検索
            matches = self._search_file(file_path, pattern, options)
            if matches:
                relative_path = self._compute_relative_path(file_path, search_paths)
                file_result = FileSearchResult(
                    file_path=file_path,
                    relative_path=relative_path,
                    matches=matches,
                )
                file_results_map[file_path] = file_result
                total_matches += len(matches)

            files_searched += 1

        results.file_results = list(file_results_map.values())

        if progress_callback:
            progress_callback(100, f"検索完了: {total_matches}件")

        return results

    def _compile_pattern(self, options: SearchOptions) -> re.Pattern:
        """検索パターンをコンパイル"""
        query = options.query

        if not options.is_regex:
            # 固定文字列の場合はエスケープ
            query = re.escape(query)

        if options.is_word_match:
            query = rf"\b{query}\b"

        flags = 0 if options.is_case_sensitive else re.IGNORECASE
        return re.compile(query, flags)

    def _search_file(
        self, file_path: str, pattern: re.Pattern, options: SearchOptions
    ) -> List[SearchMatch]:
        """ファイル内を検索"""
        matches = []

        try:
            # エンコーディングを試行
            encodings = ["utf-8", "cp932", "euc-jp", "latin-1"]

            for encoding in encodings:
                try:
                    with open(file_path, "r", encoding=encoding) as f:
                        lines = f.readlines()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                # どのエンコーディングでも読めない
                return []

            # 各行を検索
            for line_idx, line in enumerate(lines):
                line_content = line.rstrip("\n\r")

                for match in pattern.finditer(line_content):
                    # コンテキストを取得
                    context_before = []
                    context_after = []

                    if options.context_lines > 0:
                        start_idx = max(0, line_idx - options.context_lines)
                        context_before = [
                            lines[i].rstrip("\n\r") for i in range(start_idx, line_idx)
                        ]

                        end_idx = min(len(lines), line_idx + options.context_lines + 1)
                        context_after = [
                            lines[i].rstrip("\n\r")
                            for i in range(line_idx + 1, end_idx)
                        ]

                    search_match = SearchMatch(
                        line_number=line_idx + 1,  # 1-indexed
                        line_content=line_content,
                        match_start=match.start(),
                        match_end=match.end(),
                        context_before=context_before,
                        context_after=context_after,
                    )
                    matches.append(search_match)

        except (IOError, OSError) as e:
            logger.debug(f"ファイル読み込みエラー: {file_path}: {e}")

        return matches

    def _compute_relative_path(self, file_path: str, search_paths: List[str]) -> str:
        """検索パスからの相対パスを計算"""
        file_path = os.path.normpath(file_path)

        for search_path in search_paths:
            search_path = os.path.normpath(search_path)
            if file_path.startswith(search_path):
                try:
                    return os.path.relpath(file_path, search_path)
                except ValueError:
                    pass

        return os.path.basename(file_path)

    def _glob_to_regex(self, glob_pattern: str) -> str:
        """globパターンを正規表現に変換"""
        regex = ""
        i = 0
        while i < len(glob_pattern):
            c = glob_pattern[i]
            if c == "*":
                if i + 1 < len(glob_pattern) and glob_pattern[i + 1] == "*":
                    regex += ".*"
                    i += 2
                    continue
                else:
                    regex += "[^/]*"
            elif c == "?":
                regex += "."
            elif c == "[":
                j = i + 1
                while j < len(glob_pattern) and glob_pattern[j] != "]":
                    j += 1
                regex += glob_pattern[i : j + 1]
                i = j
            elif c in ".^$+{}|()":
                regex += "\\" + c
            else:
                regex += c
            i += 1
        return f"^{regex}$"

    def _matches_pattern(self, name: str, pattern: str) -> bool:
        """名前がパターンにマッチするかチェック"""
        # シンプルなワイルドカードマッチ
        if pattern.startswith("*") and pattern.endswith("*"):
            return pattern[1:-1] in name
        elif pattern.startswith("*"):
            return name.endswith(pattern[1:])
        elif pattern.endswith("*"):
            return name.startswith(pattern[:-1])
        else:
            return name == pattern
