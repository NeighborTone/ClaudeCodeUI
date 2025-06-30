# -*- coding: utf-8 -*-
"""
Application Logger - Simple file-based logging system
"""
import os
import time
from datetime import datetime
from typing import Optional


class ApplicationLogger:
    """Simple application logger that writes to file"""
    
    _instance: Optional['ApplicationLogger'] = None
    
    def __init__(self, log_file: str = "debug.log"):
        self.log_file = log_file
        self.enabled = True
    
    @classmethod
    def get_instance(cls) -> 'ApplicationLogger':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _write_log(self, level: str, message: str):
        """Write log message to file"""
        if not self.enabled:
            return
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception:
            # Don't fail if logging fails
            pass
    
    def debug(self, message: str):
        """Log debug message"""
        self._write_log("DEBUG", message)
    
    def info(self, message: str):
        """Log info message"""
        self._write_log("INFO", message)
    
    def warning(self, message: str):
        """Log warning message"""
        self._write_log("WARNING", message)
    
    def error(self, message: str):
        """Log error message"""
        self._write_log("ERROR", message)
    
    def clear(self):
        """Clear log file"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("")
        except Exception:
            pass
    
    def disable(self):
        """Disable logging"""
        self.enabled = False
    
    def enable(self):
        """Enable logging"""
        self.enabled = True


# Global logger instance
logger = ApplicationLogger.get_instance()


def log_startup_timing(operation: str, start_time: float):
    """Log startup timing information"""
    elapsed = time.time() - start_time
    logger.info(f"Startup: {operation} completed in {elapsed:.3f}s")


def log_indexing_operation(operation: str, details: str = ""):
    """Log indexing operations"""
    logger.info(f"Indexing: {operation} {details}".strip())


def log_performance(operation: str, duration: float, details: str = ""):
    """Log performance metrics"""
    logger.info(f"Performance: {operation} took {duration:.3f}s {details}".strip())


def get_logger(name: str = __name__) -> ApplicationLogger:
    """Get logger instance (standardized interface)"""
    return ApplicationLogger.get_instance()