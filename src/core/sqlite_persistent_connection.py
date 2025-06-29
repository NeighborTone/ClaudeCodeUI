# -*- coding: utf-8 -*-
"""
SQLite Persistent Connection Manager - 持続的なデータベース接続管理
"""
import sqlite3
import threading
from typing import Optional


class SQLitePersistentConnection:
    """SQLiteの持続的な接続を管理するシングルトンクラス"""
    
    _instance = None
    _lock = threading.RLock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.connection = None
        self.db_path = None
    
    def connect(self, db_path: str) -> sqlite3.Connection:
        """データベースに接続"""
        with self._lock:
            if self.connection is None or self.db_path != db_path:
                if self.connection:
                    self.connection.close()
                
                self.db_path = db_path
                self.connection = sqlite3.connect(db_path, check_same_thread=False)
                self.connection.row_factory = sqlite3.Row
                
                # WALモードで高速化
                self.connection.execute("PRAGMA journal_mode=WAL")
                self.connection.execute("PRAGMA synchronous=NORMAL")
                self.connection.execute("PRAGMA cache_size=10000")
                self.connection.execute("PRAGMA temp_store=MEMORY")
                
            return self.connection
    
    def get_connection(self) -> Optional[sqlite3.Connection]:
        """現在の接続を取得"""
        return self.connection
    
    def close(self):
        """接続を閉じる"""
        with self._lock:
            if self.connection:
                self.connection.close()
                self.connection = None
                self.db_path = None
    
    def is_connected(self) -> bool:
        """接続されているかチェック"""
        return self.connection is not None