#!/usr/bin/env python3
"""
Test runner script for PythonDungeon
Provides convenient commands for running different types of tests
"""

import sys
import subprocess
import os


def run_command(cmd):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    return result.returncode == 0


def main():
    """Main test runner."""
    if len(sys.argv) < 2:
        print("""
PythonDungeon Test Runner

Usage:
    python run_tests.py <command>

Commands:
    all         - Run all tests with coverage
    unit        - Run only unit tests
    integration - Run only integration tests  
    fast        - Run tests excluding slow ones
    coverage    - Run tests and generate coverage report
    specific    - Run specific test file (requires filename)
    
Examples:
    python run_tests.py all
    python run_tests.py unit
    python run_tests.py specific test_player.py
        """)
        return
    
    command = sys.argv[1].lower()
    
    # Base pytest command
    base_cmd = ["python", "-m", "pytest"]
    
    if command == "all":
        cmd = base_cmd + ["-v"]
        
    elif command == "unit":
        cmd = base_cmd + ["-m", "unit", "-v"]
        
    elif command == "integration":
        cmd = base_cmd + ["-m", "integration", "-v"]
        
    elif command == "fast":
        cmd = base_cmd + ["-m", "not slow", "-v"]
        
    elif command == "coverage":
        cmd = base_cmd + ["--cov=.", "--cov-report=html", "--cov-report=term", "-v"]
        
    elif command == "specific":
        if len(sys.argv) < 3:
            print("Error: Please specify a test file")
            return
        test_file = sys.argv[2]
        cmd = base_cmd + [f"tests/{test_file}", "-v"]
        
    else:
        print(f"Unknown command: {command}")
        return
    
    # Run the tests
    success = run_command(cmd)
    
    if success:
        print("✅ Tests passed!")
        if command == "coverage":
            print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print("❌ Tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()