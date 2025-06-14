# -*- coding: utf-8 -*-
"""
Environment Detector - 実行環境の検出
WSL、Windows、Linuxなどの環境を自動検出する
"""
import os
import platform
import sys
from typing import Literal, Dict, Any

EnvironmentType = Literal["wsl", "windows", "linux", "macos", "unknown"]

class EnvironmentDetector:
    """実行環境検出クラス"""
    
    _cache: Dict[str, Any] = {}
    
    @classmethod
    def detect_environment(cls) -> EnvironmentType:
        """実行環境を検出"""
        if "environment" in cls._cache:
            return cls._cache["environment"]
        
        environment = cls._detect_environment_impl()
        cls._cache["environment"] = environment
        return environment
    
    @classmethod
    def _detect_environment_impl(cls) -> EnvironmentType:
        """実行環境の実際の検出処理"""
        # WSL環境の検出
        if cls._is_wsl():
            return "wsl"
        
        # プラットフォーム判定
        system = platform.system().lower()
        
        if system == "windows":
            return "windows"
        elif system == "linux":
            return "linux"
        elif system == "darwin":
            return "macos"
        else:
            return "unknown"
    
    @classmethod
    def _is_wsl(cls) -> bool:
        """WSL環境かどうかを判定"""
        # 方法1: 環境変数で判定
        if os.environ.get("WSL_DISTRO_NAME"):
            return True
        
        # 方法2: /proc/versionの内容を確認
        try:
            with open("/proc/version", "r") as f:
                version_info = f.read().lower()
                if "microsoft" in version_info or "wsl" in version_info:
                    return True
        except (FileNotFoundError, PermissionError):
            pass
        
        # 方法3: /proc/sys/kernel/osreleaseの確認
        try:
            with open("/proc/sys/kernel/osrelease", "r") as f:
                osrelease = f.read().lower()
                if "microsoft" in osrelease or "wsl" in osrelease:
                    return True
        except (FileNotFoundError, PermissionError):
            pass
        
        # 方法4: platform.unameの結果を確認
        try:
            uname = platform.uname()
            if "microsoft" in uname.release.lower() or "wsl" in uname.release.lower():
                return True
        except Exception:
            pass
        
        return False
    
    @classmethod
    def is_wsl(cls) -> bool:
        """WSL環境かどうかを返す"""
        return cls.detect_environment() == "wsl"
    
    @classmethod
    def is_windows(cls) -> bool:
        """Windows環境かどうかを返す"""
        return cls.detect_environment() == "windows"
    
    @classmethod
    def is_linux(cls) -> bool:
        """Linux環境かどうかを返す"""
        return cls.detect_environment() == "linux"
    
    @classmethod
    def is_macos(cls) -> bool:
        """macOS環境かどうかを返す"""
        return cls.detect_environment() == "macos"
    
    @classmethod
    def has_japanese_font_support(cls) -> bool:
        """日本語フォントサポートがあるかを判定"""
        environment = cls.detect_environment()
        
        # WSL環境では基本的に日本語フォントがない
        if environment == "wsl":
            return False
        
        # Windows環境では基本的にサポートあり
        if environment == "windows":
            return True
        
        # Linux環境では確認が必要だが、とりあえずサポートありとする
        if environment == "linux":
            return True
        
        # macOS環境では基本的にサポートあり
        if environment == "macos":
            return True
        
        # 不明な環境では安全のためサポートなしとする
        return False
    
    @classmethod
    def get_environment_info(cls) -> Dict[str, Any]:
        """環境情報を取得"""
        environment = cls.detect_environment()
        return {
            "environment": environment,
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version,
            "has_japanese_font": cls.has_japanese_font_support(),
            "is_wsl": cls.is_wsl(),
            "wsl_distro": os.environ.get("WSL_DISTRO_NAME", "Unknown") if cls.is_wsl() else None
        }
    
    @classmethod
    def get_recommended_language(cls) -> Literal["ja", "en"]:
        """推奨言語を取得"""
        # 日本語フォントサポートがない場合は英語を推奨
        if not cls.has_japanese_font_support():
            return "en"
        
        # 日本語ロケールかどうかを確認
        import locale
        try:
            current_locale = locale.getdefaultlocale()[0]
            if current_locale and current_locale.startswith("ja"):
                return "ja"
        except Exception:
            pass
        
        # 環境変数で日本語判定
        lang_env = os.environ.get("LANG", "").lower()
        if "ja" in lang_env or "japanese" in lang_env:
            return "ja"
        
        # デフォルトは英語
        return "en"

if __name__ == "__main__":
    # テスト実行
    detector = EnvironmentDetector()
    
    print("=== Environment Detection Test ===")
    print(f"Environment: {detector.detect_environment()}")
    print(f"Is WSL: {detector.is_wsl()}")
    print(f"Is Windows: {detector.is_windows()}")
    print(f"Is Linux: {detector.is_linux()}")
    print(f"Is macOS: {detector.is_macos()}")
    print(f"Has Japanese font support: {detector.has_japanese_font_support()}")
    print(f"Recommended language: {detector.get_recommended_language()}")
    
    print("\n=== Full Environment Info ===")
    import json
    env_info = detector.get_environment_info()
    print(json.dumps(env_info, indent=2, ensure_ascii=False))