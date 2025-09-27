#!/usr/bin/env python3
"""
MANUAL TEST: Test the scrolling display system
Run directly with: python tests/manual_test_scroll.py
"""

from display import display

# Test scrolling behavior
display.clear_content()
display.set_header("Scrolling Test")

# Add some initial content
display.add_line("Line 1: Starting test")
display.add_line("Line 2: Adding more content")
display.add_line("Line 3: This should scroll")

# Simulate what happens with menu
print("\n=== Testing menu display ===")
options = ["Option 1", "Option 2", "Option 3"]
status = "This is the status text\nIt has multiple lines\nAnd should appear line by line"

# Test the menu function
choice = display.display_menu("Test Menu", options, status)
print(f"You chose: {choice}")