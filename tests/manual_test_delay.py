#!/usr/bin/env python3
"""
MANUAL TEST: Test the delay parameter in display system
Run directly with: python tests/manual_test_delay.py
"""

from display import display

print("Testing delay parameter...")

display.clear_content()
display.set_header("Delay Test")

print("Adding lines with delays...")
display.add_line("Line 1 - no delay", delay=0)
display.add_line("Line 2 - 1 second delay", delay=1.0)
display.add_line("Line 3 - 2 second delay", delay=2.0)
display.add_line("Line 4 - no delay", delay=0)

print("Test complete!")