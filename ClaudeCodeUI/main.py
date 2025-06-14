# -*- coding: utf-8 -*-
"""
Claude Code PromptUI - Main Application
Claude Code prompt input improvement tool
"""
import sys
import os

# Add path for module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.main_window import MainWindow


def main():
    """Main function"""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Claude Code PromptUI")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("StudioEmbroidery")
    
    # Application settings
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create main window
    main_window = MainWindow()
    main_window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()