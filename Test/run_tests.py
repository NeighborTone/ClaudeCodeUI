#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test runner for ClaudeCodeUI modules
"""
import sys
import os
import unittest
import time
from io import StringIO

# Add ClaudeCodeUI to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ClaudeCodeUI'))

# Import test configuration
from test_config import setup_mock_qt

class TestResult:
    """Custom test result tracking"""
    
    def __init__(self):
        self.tests_run = 0
        self.failures = []
        self.errors = []
        self.successes = []
        self.skipped = []
        self.start_time = None
        self.end_time = None
    
    def add_success(self, test):
        self.successes.append(test)
    
    def add_failure(self, test, err):
        self.failures.append((test, err))
    
    def add_error(self, test, err):
        self.errors.append((test, err))
    
    def add_skip(self, test, reason):
        self.skipped.append((test, reason))
    
    def get_success_rate(self):
        if self.tests_run == 0:
            return 0
        return len(self.successes) / self.tests_run * 100
    
    def get_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0

class ColoredTestResult(unittest.TextTestResult):
    """Colored test result output"""
    
    def __init__(self, stream, descriptions, verbosity, result_tracker):
        super().__init__(stream, descriptions, verbosity)
        self.result_tracker = result_tracker
        self._verbosity = verbosity
    
    def startTest(self, test):
        super().startTest(test)
        self.result_tracker.tests_run += 1
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.result_tracker.add_success(test)
        if self._verbosity > 1:
            self.stream.write("✓ ")
            self.stream.flush()
    
    def addError(self, test, err):
        super().addError(test, err)
        self.result_tracker.add_error(test, err)
        if self._verbosity > 1:
            self.stream.write("✗ ")
            self.stream.flush()
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.result_tracker.add_failure(test, err)
        if self._verbosity > 1:
            self.stream.write("✗ ")
            self.stream.flush()
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.result_tracker.add_skip(test, reason)
        if self._verbosity > 1:
            self.stream.write("⊝ ")
            self.stream.flush()

def discover_tests(test_dir=None):
    """Discover all test modules"""
    if test_dir is None:
        test_dir = os.path.dirname(__file__)
    
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_*.py')
    return suite

def run_module_tests(module_name, verbosity=2):
    """Run tests for a specific module"""
    print(f"\n{'='*60}")
    print(f"Testing {module_name}")
    print(f"{'='*60}")
    
    result_tracker = TestResult()
    result_tracker.start_time = time.time()
    
    try:
        # Import the specific test module
        test_module = __import__(f'{module_name}', fromlist=[''])
        
        # Load tests from module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test_module)
        
        # Run tests with custom result class
        stream = StringIO() if verbosity == 0 else sys.stdout
        runner = unittest.TextTestRunner(
            stream=stream,
            verbosity=verbosity,
            resultclass=lambda stream, descriptions, verbosity: 
                ColoredTestResult(stream, descriptions, verbosity, result_tracker)
        )
        
        result = runner.run(suite)
        result_tracker.end_time = time.time()
        
        # Print summary
        print(f"\n{'-'*40}")
        print(f"Module: {module_name}")
        print(f"Tests run: {result_tracker.tests_run}")
        print(f"Successes: {len(result_tracker.successes)}")
        print(f"Failures: {len(result_tracker.failures)}")
        print(f"Errors: {len(result_tracker.errors)}")
        print(f"Skipped: {len(result_tracker.skipped)}")
        print(f"Success rate: {result_tracker.get_success_rate():.1f}%")
        print(f"Duration: {result_tracker.get_duration():.2f}s")
        
        return result_tracker
        
    except ImportError as e:
        print(f"Failed to import {module_name}: {e}")
        return None
    except Exception as e:
        print(f"Error running tests for {module_name}: {e}")
        return None

def run_all_tests(verbosity=2):
    """Run all tests and generate report"""
    print("ClaudeCodeUI Module Test Suite")
    print("="*60)
    
    # Setup mock Qt environment
    setup_mock_qt()
    
    # Test modules to run
    test_modules = [
        # Core modules
        'test_core.test_token_counter',
        'test_core.test_path_converter',
        'test_core.test_python_helper',
        'test_core.test_settings',
        'test_core.test_workspace_manager',
        'test_core.test_file_searcher',
        
        # Widget modules
        'test_widgets.test_thinking_selector',
        'test_widgets.test_path_mode_selector',
        
        # UI modules
        'test_ui.test_style_themes'
    ]
    
    overall_results = {
        'total_tests': 0,
        'total_successes': 0,
        'total_failures': 0,
        'total_errors': 0,
        'total_skipped': 0,
        'module_results': {},
        'start_time': time.time()
    }
    
    # Run each module's tests
    for module_name in test_modules:
        result = run_module_tests(module_name, verbosity)
        
        if result:
            overall_results['total_tests'] += result.tests_run
            overall_results['total_successes'] += len(result.successes)
            overall_results['total_failures'] += len(result.failures)
            overall_results['total_errors'] += len(result.errors)
            overall_results['total_skipped'] += len(result.skipped)
            overall_results['module_results'][module_name] = result
    
    overall_results['end_time'] = time.time()
    
    # Generate final report
    generate_final_report(overall_results)
    
    return overall_results

def generate_final_report(results):
    """Generate final test report"""
    print(f"\n{'='*60}")
    print("FINAL TEST REPORT")
    print(f"{'='*60}")
    
    total_tests = results['total_tests']
    total_successes = results['total_successes']
    total_failures = results['total_failures']
    total_errors = results['total_errors']
    total_skipped = results['total_skipped']
    
    success_rate = (total_successes / total_tests * 100) if total_tests > 0 else 0
    duration = results['end_time'] - results['start_time']
    
    print(f"Total tests run: {total_tests}")
    print(f"Successes: {total_successes} ✓")
    print(f"Failures: {total_failures} ✗")
    print(f"Errors: {total_errors} ✗")
    print(f"Skipped: {total_skipped} ⊝")
    print(f"Overall success rate: {success_rate:.1f}%")
    print(f"Total duration: {duration:.2f}s")
    
    # Module breakdown
    print(f"\n{'-'*40}")
    print("MODULE BREAKDOWN:")
    print(f"{'-'*40}")
    
    for module_name, result in results['module_results'].items():
        success_rate = result.get_success_rate()
        status = "✓ PASS" if success_rate == 100 else "⚠ PARTIAL" if success_rate > 0 else "✗ FAIL"
        print(f"{module_name:<35} {status} ({success_rate:.1f}%)")
    
    # Overall status
    print(f"\n{'-'*40}")
    if total_failures == 0 and total_errors == 0:
        print("🎉 ALL TESTS PASSED!")
        exit_code = 0
    elif total_successes > 0:
        print("⚠️  SOME TESTS FAILED")
        exit_code = 1
    else:
        print("❌ ALL TESTS FAILED")
        exit_code = 2
    
    print(f"Exit code: {exit_code}")
    return exit_code

def main():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ClaudeCodeUI Test Runner')
    parser.add_argument('--module', '-m', help='Run tests for specific module')
    parser.add_argument('--verbose', '-v', action='count', default=2, 
                       help='Increase verbosity')
    parser.add_argument('--quiet', '-q', action='store_true', 
                       help='Minimal output')
    
    args = parser.parse_args()
    
    verbosity = 0 if args.quiet else args.verbose
    
    if args.module:
        # Run specific module
        result = run_module_tests(args.module, verbosity)
        if result:
            exit_code = 0 if (len(result.failures) == 0 and len(result.errors) == 0) else 1
        else:
            exit_code = 2
    else:
        # Run all tests
        results = run_all_tests(verbosity)
        exit_code = 0 if (results['total_failures'] == 0 and results['total_errors'] == 0) else 1
    
    sys.exit(exit_code)

if __name__ == '__main__':
    main()