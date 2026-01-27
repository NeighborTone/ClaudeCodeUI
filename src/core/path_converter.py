# -*- coding: utf-8 -*-
"""
Path Converter - Unified forward slash path formatting
"""
import os
import sys
import urllib.parse


class PathConverter:
    """Path conversion utility for unified forward slash formatting"""

    @staticmethod
    def normalize_path(path: str) -> str:
        """
        Normalize path to use forward slashes only.

        Args:
            path: The path to normalize

        Returns:
            Path with forward slashes only
        """
        return path.replace('\\', '/')

    @staticmethod
    def from_file_uri(uri: str) -> str:
        """
        file:// URI形式をOS標準のローカルパスに変換する。

        Args:
            uri: file:// URI形式の文字列 (例: file:///C:/path/to/file)

        Returns:
            OS標準形式のローカルパス
            - Windows: C:\\path\\to\\file
            - Linux/macOS: /path/to/file
        """
        if not uri.startswith('file://'):
            return uri

        # file://を除去してパスを取得
        path = uri[7:]  # 'file://' の長さは7

        # URLデコード（%20 -> スペース等）
        path = urllib.parse.unquote(path)

        # Windowsの場合: /C:/path → C:/path
        if sys.platform == 'win32' and path.startswith('/') and len(path) > 2 and path[2] == ':':
            path = path[1:]

        # OS標準のパス区切りに変換
        path = os.path.normpath(path)

        return path

    @staticmethod
    def to_os_native_path(path: str) -> str:
        """
        パスをOS標準の区切り文字に変換する。

        Args:
            path: 変換するパス

        Returns:
            OS標準形式のパス
        """
        return os.path.normpath(path)