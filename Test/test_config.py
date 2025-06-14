# -*- coding: utf-8 -*-
"""
Test configuration and utilities
"""
import sys
import os
import unittest
from unittest.mock import Mock

# Add ClaudeCodeUI to path
CLAUDECODEUI_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ClaudeCodeUI')
sys.path.insert(0, CLAUDECODEUI_PATH)

class MockQtBase:
    """Mock Qt base class for testing without PySide6"""
    def __init__(self, *args, **kwargs):
        pass
    
    def connect(self, *args, **kwargs):
        pass
    
    def emit(self, *args, **kwargs):
        pass
    
    def setText(self, text):
        self._text = text
    
    def text(self):
        return getattr(self, '_text', '')
    
    def addWidget(self, widget):
        pass
    
    def addLayout(self, layout):
        pass
    
    def setCurrentIndex(self, index):
        self._index = index
    
    def currentIndex(self):
        return getattr(self, '_index', 0)

def setup_mock_qt():
    """Setup mock Qt modules for testing without PySide6"""
    mock_modules = [
        'PySide6',
        'PySide6.QtWidgets',
        'PySide6.QtCore',
        'PySide6.QtGui'
    ]
    
    for module_name in mock_modules:
        if module_name not in sys.modules:
            sys.modules[module_name] = Mock()
    
    # Create mock Qt classes
    from unittest.mock import MagicMock
    
    sys.modules['PySide6.QtWidgets'].QWidget = type('QWidget', (MockQtBase,), {})
    sys.modules['PySide6.QtWidgets'].QVBoxLayout = type('QVBoxLayout', (MockQtBase,), {})
    sys.modules['PySide6.QtWidgets'].QHBoxLayout = type('QHBoxLayout', (MockQtBase,), {})
    sys.modules['PySide6.QtWidgets'].QComboBox = type('QComboBox', (MockQtBase,), {
        'addItem': lambda self, text, data=None: None,
        'currentData': lambda self: 'mock_data',
        'currentTextChanged': Mock(),
        'count': lambda self: 5,
        'itemData': lambda self, index: f'item_{index}'
    })
    sys.modules['PySide6.QtWidgets'].QLabel = type('QLabel', (MockQtBase,), {})
    sys.modules['PySide6.QtWidgets'].QTextEdit = type('QTextEdit', (MockQtBase,), {
        'toPlainText': lambda self: getattr(self, '_plain_text', ''),
        'setPlainText': lambda self, text: setattr(self, '_plain_text', text),
        'textCursor': lambda self: Mock(),
        'setTextCursor': lambda self, cursor: None
    })
    sys.modules['PySide6.QtWidgets'].QPushButton = type('QPushButton', (MockQtBase,), {})
    sys.modules['PySide6.QtWidgets'].QListWidget = type('QListWidget', (MockQtBase,), {})
    sys.modules['PySide6.QtWidgets'].QMainWindow = type('QMainWindow', (MockQtBase,), {})
    sys.modules['PySide6.QtWidgets'].QApplication = type('QApplication', (MockQtBase,), {
        'clipboard': lambda: Mock()
    })
    
    sys.modules['PySide6.QtCore'].Signal = Mock
    sys.modules['PySide6.QtCore'].Qt = Mock()
    sys.modules['PySide6.QtCore'].QTimer = type('QTimer', (MockQtBase,), {
        'setSingleShot': lambda self, single: None,
        'start': lambda self, timeout=None: None,
        'stop': lambda self: None,
        'timeout': Mock()
    })
    
    sys.modules['PySide6.QtGui'].QKeyEvent = Mock
    sys.modules['PySide6.QtGui'].QTextCursor = Mock
    sys.modules['PySide6.QtGui'].QFont = Mock

class BaseTestCase(unittest.TestCase):
    """Base test case with common setup"""
    
    @classmethod
    def setUpClass(cls):
        """Setup class-level test fixtures"""
        setup_mock_qt()
    
    def setUp(self):
        """Setup test fixtures"""
        # Create temp directories for testing
        self.test_temp_dir = '/tmp/test_claudecodeui'
        os.makedirs(self.test_temp_dir, exist_ok=True)
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Clean up temp files if needed
        pass

def run_single_test(test_class, method_name=None):
    """Run a single test class or method"""
    if method_name:
        suite = unittest.TestSuite()
        suite.addTest(test_class(method_name))
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)