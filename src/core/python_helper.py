# -*- coding: utf-8 -*-
"""
Python Helper - Python execution utilities for WSL/Windows compatibility
"""
import os
import subprocess
import shutil
from typing import Optional, List, Dict
from src.core.ui_strings import tr


class PythonHelper:
    """Python実行環境のヘルパークラス"""
    
    @staticmethod
    def is_wsl_environment() -> bool:
        """WSL環境かどうかを判定"""
        return 'WSL_DISTRO_NAME' in os.environ or 'WSL_INTEROP' in os.environ
    
    @staticmethod
    def find_python_executables() -> List[Dict[str, str]]:
        """
        利用可能なPython実行可能ファイルを検索
        
        Returns:
            List of dicts with 'path', 'version', 'type' keys
        """
        executables = []
        
        # Common Python executable names
        python_names = ['python', 'python3', 'python3.8', 'python3.9', 'python3.10', 'python3.11', 'python3.12']
        
        for name in python_names:
            # Check system PATH
            path = shutil.which(name)
            if path:
                version = PythonHelper.get_python_version(path)
                if version:
                    executables.append({
                        'path': path,
                        'version': version,
                        'type': 'system'
                    })
        
        # If in WSL, also check Windows Python installations
        if PythonHelper.is_wsl_environment():
            windows_python_paths = [
                '/mnt/c/Python39/python.exe',
                '/mnt/c/Python310/python.exe',
                '/mnt/c/Python311/python.exe',
                '/mnt/c/Python312/python.exe',
                '/mnt/c/Users/*/AppData/Local/Programs/Python/Python*/python.exe',
                '/mnt/c/Program Files/Python*/python.exe',
                '/mnt/c/Program Files (x86)/Python*/python.exe',
            ]
            
            for pattern in windows_python_paths:
                if '*' in pattern:
                    # Use glob-like search
                    import glob
                    for path in glob.glob(pattern):
                        if os.path.exists(path):
                            version = PythonHelper.get_python_version(path)
                            if version:
                                executables.append({
                                    'path': path,
                                    'version': version,
                                    'type': 'windows'
                                })
                else:
                    if os.path.exists(pattern):
                        version = PythonHelper.get_python_version(pattern)
                        if version:
                            executables.append({
                                'path': pattern,
                                'version': version,
                                'type': 'windows'
                            })
        
        return executables
    
    @staticmethod
    def get_python_version(python_path: str) -> Optional[str]:
        """
        Python実行可能ファイルのバージョンを取得
        
        Args:
            python_path: Python実行可能ファイルのパス
            
        Returns:
            Version string or None if failed
        """
        try:
            result = subprocess.run(
                [python_path, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return result.stderr.strip()
        except Exception:
            return None
    
    @staticmethod
    def get_recommended_python() -> Optional[str]:
        """
        推奨されるPython実行可能ファイルのパスを取得
        
        Returns:
            Recommended Python executable path
        """
        executables = PythonHelper.find_python_executables()
        
        if not executables:
            return None
        
        # WSL環境の場合、システムのPythonを優先
        if PythonHelper.is_wsl_environment():
            for exe in executables:
                if exe['type'] == 'system' and 'python3' in exe['path']:
                    return exe['path']
        
        # 最初に見つかったものを返す
        return executables[0]['path']
    
    @staticmethod
    def create_run_script(script_path: str) -> str:
        """
        WSL環境でPythonスクリプトを実行するためのシェルスクリプトを作成
        
        Args:
            script_path: 実行するPythonスクリプトのパス
            
        Returns:
            Created shell script path
        """
        python_exe = PythonHelper.get_recommended_python()
        if not python_exe:
            python_exe = 'python3'
        
        script_dir = os.path.dirname(script_path)
        run_script_path = os.path.join(script_dir, 'run.sh')
        
        script_content = f"""#!/bin/bash
# Auto-generated run script for WSL compatibility

# Navigate to script directory
cd "{script_dir}"

# Run Python script with recommended Python executable
{python_exe} "{os.path.basename(script_path)}" "$@"
"""
        
        with open(run_script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Make script executable
        os.chmod(run_script_path, 0o755)
        
        return run_script_path
    
    @staticmethod
    def get_execution_instructions() -> str:
        """
        実行方法の説明テキストを取得
        
        Returns:
            Instruction text
        """
        is_wsl = PythonHelper.is_wsl_environment()
        python_exe = PythonHelper.get_recommended_python()
        executables = PythonHelper.find_python_executables()
        
        instructions = []
        
        if is_wsl:
            instructions.append(tr("python_env_wsl_header"))
            instructions.append("")
            
            if python_exe:
                instructions.append(tr("python_env_recommended"))
                instructions.append(f"```bash")
                instructions.append(f"{python_exe} main.py")
                instructions.append(f"```")
                instructions.append("")
            
            instructions.append(tr("python_env_available"))
            for exe in executables:
                instructions.append(f"- {exe['path']} ({exe['version']}) - {exe['type']}")
            
            instructions.append("")
            instructions.append(tr("python_env_wsl_notes_header"))
            instructions.append(tr("python_env_wsl_note1"))
            instructions.append(tr("python_env_wsl_note2"))
            instructions.append(tr("python_env_wsl_note3"))
            instructions.append("  ```bash")
            instructions.append("  pip install -r requirements.txt")
            instructions.append("  ```")
        else:
            instructions.append(tr("python_env_windows_header"))
            instructions.append("")
            
            if python_exe:
                instructions.append(tr("python_env_recommended"))
                instructions.append(f"```cmd")
                instructions.append(f"{python_exe} main.py")
                instructions.append(f"```")
            
            instructions.append("")
            instructions.append(tr("python_env_available"))
            for exe in executables:
                instructions.append(f"- {exe['path']} ({exe['version']})")
        
        return "\n".join(instructions)