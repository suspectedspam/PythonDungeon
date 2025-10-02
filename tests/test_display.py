#!/usr/bin/env python3
"""
Test suite for the display system.
Tests console display functionality, text scrolling, and menu systems.
"""

import pytest
from unittest.mock import Mock, patch, call
import io
import sys
from src.ui.display import Display


class TestDisplaySystem:
    """Test the core display system functionality."""
    
    def test_display_creation(self):
        """Test display system initialization."""
        display = Display()
        
        assert display.lines == []
        assert display.footer == ""
        assert display.debug_mode is False
        assert display.line_delay == 0.3
        assert display.exposition_line_delay == 0.8
    
    def test_debug_mode_toggle(self):
        """Test debug mode functionality."""
        display = Display()
        
        # Test enabling debug mode
        display.debug_mode = True
        assert display.debug_mode is True
        
        # Test disabling debug mode  
        display.debug_mode = False
        assert display.debug_mode is False
    
    def test_add_line_basic(self):
        """Test adding lines to the display."""
        display = Display()
        
        display.add_line("Test line")
        assert len(display.lines) == 1
        assert display.lines[0] == "Test line"
    
    def test_add_line_multiple(self):
        """Test adding multiple lines."""
        display = Display()
        
        display.add_line("First line")
        display.add_line("Second line")
        display.add_line("Third line")
        
        assert len(display.lines) == 3
        assert display.lines[0] == "First line"
        assert display.lines[1] == "Second line"
        assert display.lines[2] == "Third line"
    
    @patch('time.sleep')
    def test_add_line_with_delay(self, mock_sleep):
        """Test that add_line respects delay parameter."""
        display = Display()
        
        # Test with custom delay
        display.add_line("Delayed line", delay=0.5)
        mock_sleep.assert_called_once_with(0.5)
    
    @patch('time.sleep')
    def test_add_line_debug_mode_delay(self, mock_sleep):
        """Test that debug mode uses faster delays."""
        display = Display()
        display.debug_mode = True
        
        display.add_line("Debug line", delay=0.5)
        mock_sleep.assert_called_once_with(0.05)  # Debug mode faster delay
    
    @patch('time.sleep')
    def test_add_line_no_delay(self, mock_sleep):
        """Test add_line with delay=None (no sleep)."""
        display = Display()
        
        display.add_line("No delay line", delay=None)
        mock_sleep.assert_not_called()
    
    def test_add_lines_list(self):
        """Test adding multiple lines at once."""
        display = Display()
        
        lines_to_add = ["Line 1", "Line 2", "Line 3"]
        
        with patch('time.sleep'):  # Mock sleep to speed up test
            display.add_lines(lines_to_add)
        
        assert len(display.lines) == 3
        assert display.lines == lines_to_add
    
    @patch('time.sleep')
    def test_add_lines_with_delay(self, mock_sleep):
        """Test add_lines with delay parameter."""
        display = Display()
        
        lines = ["First", "Second"]
        display.add_lines(lines, delay=0.2)
        
        # Should call sleep for each line
        assert mock_sleep.call_count == 2
        mock_sleep.assert_has_calls([call(0.2), call(0.2)])
    
    def test_set_footer(self):
        """Test setting the footer text."""
        display = Display()
        
        display.set_footer("Test footer")
        assert display.footer == "Test footer"
        
        display.set_footer("")
        assert display.footer == ""
    
    def test_clear_screen(self):
        """Test screen clearing functionality."""
        display = Display()
        
        # Add some content
        display.add_line("Content to clear")
        display.set_footer("Footer to clear")
        
        # Clear screen
        display.clear_screen()
        
        assert display.lines == []
        assert display.footer == ""
    
    @patch('builtins.print')
    @patch('os.system')
    def test_refresh_display_windows(self, mock_system, mock_print):
        """Test display refresh on Windows."""
        display = Display()
        
        display.add_line("Test content")
        display.set_footer("Test footer")
        
        with patch('sys.platform', 'win32'):
            display.refresh_display()
        
        # Should clear screen and print content
        mock_system.assert_called_once_with('cls')
        assert mock_print.called
    
    @patch('builtins.print')
    @patch('os.system')  
    def test_refresh_display_unix(self, mock_system, mock_print):
        """Test display refresh on Unix systems."""
        display = Display()
        
        display.add_line("Test content")
        
        with patch('sys.platform', 'linux'):
            display.refresh_display()
        
        # Should clear screen with 'clear' command
        mock_system.assert_called_once_with('clear')
        assert mock_print.called


class TestDisplayMenu:
    """Test the display menu system."""
    
    @patch('builtins.input')
    @patch('src.ui.display.Display.refresh_display')
    def test_display_menu_basic(self, mock_refresh, mock_input):
        """Test basic menu display and input."""
        display = Display()
        mock_input.return_value = "1"
        
        options = ["Option 1", "Option 2", "Option 3"]
        result = display.display_menu("Test Menu", options, "Status text")
        
        assert result == "1"
        assert mock_refresh.called
    
    @patch('builtins.input')
    @patch('src.ui.display.Display.refresh_display')
    def test_display_menu_with_exposition(self, mock_refresh, mock_input):
        """Test menu with exposition intro."""
        display = Display()
        mock_input.return_value = "2"
        
        options = ["Choice A", "Choice B"]
        
        with patch('time.sleep'):  # Mock sleep for faster test
            result = display.display_menu("Menu Title", options, "Status", exposition_intro=True)
        
        assert result == "2"
    
    @patch('builtins.input')
    @patch('src.ui.display.Display.refresh_display')
    def test_display_menu_quit_command(self, mock_refresh, mock_input):
        """Test menu quit command handling."""
        display = Display()
        mock_input.return_value = "quit"
        
        options = ["Option 1", "Option 2"]
        result = display.display_menu("Test Menu", options, "Status")
        
        assert result == "quit"
    
    @patch('builtins.input')
    @patch('src.ui.display.Display.refresh_display')
    def test_display_menu_invalid_then_valid(self, mock_refresh, mock_input):
        """Test menu with invalid input followed by valid input."""
        display = Display()
        
        # First return invalid, then valid
        mock_input.side_effect = ["invalid", "1"]
        
        options = ["Valid Option"]
        result = display.display_menu("Test Menu", options, "Status")
        
        assert result == "1"
        # Should have been called twice due to invalid input
        assert mock_input.call_count == 2
    
    @patch('builtins.input')
    @patch('src.ui.display.Display.refresh_display')
    def test_display_menu_keyboard_interrupt(self, mock_refresh, mock_input):
        """Test menu handling of keyboard interrupt."""
        display = Display()
        mock_input.side_effect = KeyboardInterrupt()
        
        options = ["Option 1"]
        result = display.display_menu("Test Menu", options, "Status")
        
        assert result == "quit"
    
    @patch('builtins.input')
    @patch('src.ui.display.Display.refresh_display')
    def test_display_menu_eof_error(self, mock_refresh, mock_input):
        """Test menu handling of EOF error."""
        display = Display()
        mock_input.side_effect = EOFError()
        
        options = ["Option 1"]
        result = display.display_menu("Test Menu", options, "Status")
        
        assert result == "quit"


class TestDisplayFormatting:
    """Test display formatting functionality."""
    
    def test_format_menu_options(self):
        """Test menu options formatting."""
        display = Display()
        
        options = ["First Option", "Second Option", "Third Option"]
        
        # This tests internal formatting - we'll check via display_menu
        with patch('builtins.input', return_value="1"):
            with patch.object(display, 'refresh_display'):
                display.display_menu("Test", options, "Status")
        
        # Check that lines were added (menu was formatted)
        assert len(display.lines) > 0
    
    def test_menu_numbering(self):
        """Test that menu options are properly numbered."""
        display = Display()
        
        options = ["Alpha", "Beta", "Gamma"]
        
        with patch('builtins.input', return_value="2"):
            with patch.object(display, 'refresh_display'):
                display.display_menu("Test", options, "Status")
        
        # Check that menu lines contain numbering
        menu_content = "\n".join(display.lines)
        assert "1" in menu_content
        assert "2" in menu_content  
        assert "3" in menu_content
    
    def test_status_text_inclusion(self):
        """Test that status text is included in display."""
        display = Display()
        
        status_text = "Important status information"
        
        with patch('builtins.input', return_value="1"):
            with patch.object(display, 'refresh_display'):
                display.display_menu("Test", ["Option"], status_text)
        
        # Status text should be in the display lines
        all_content = "\n".join(display.lines)
        assert status_text in all_content


class TestDisplayDelays:
    """Test display delay functionality."""
    
    def test_get_line_delay_normal(self):
        """Test getting line delay in normal mode."""
        display = Display()
        display.debug_mode = False
        
        delay = display.get_line_delay()
        assert delay == 0.3  # Default line delay
    
    def test_get_line_delay_debug(self):
        """Test getting line delay in debug mode."""
        display = Display()
        display.debug_mode = True
        
        delay = display.get_line_delay()
        assert delay == 0.05  # Debug mode faster delay
    
    def test_get_exposition_delay_normal(self):
        """Test getting exposition delay in normal mode."""
        display = Display()
        display.debug_mode = False
        
        delay = display.get_exposition_delay()
        assert delay == 0.8  # Default exposition delay
    
    def test_get_exposition_delay_debug(self):
        """Test getting exposition delay in debug mode."""
        display = Display()
        display.debug_mode = True
        
        delay = display.get_exposition_delay()
        assert delay == 0.05  # Debug mode faster delay
    
    @patch('time.sleep')
    def test_delay_application_normal_mode(self, mock_sleep):
        """Test that delays are applied correctly in normal mode."""
        display = Display()
        display.debug_mode = False
        
        display.add_line("Test line", delay=0.5)
        mock_sleep.assert_called_once_with(0.5)
    
    @patch('time.sleep')
    def test_delay_application_debug_mode(self, mock_sleep):
        """Test that delays are overridden in debug mode."""
        display = Display()
        display.debug_mode = True
        
        display.add_line("Test line", delay=0.5)
        mock_sleep.assert_called_once_with(0.05)


class TestDisplayIntegration:
    """Integration tests for display system."""
    
    def test_display_singleton_behavior(self):
        """Test that display behaves as a singleton."""
        from src.ui.display import display  # Import the singleton instance
        
        # Should be the same instance
        assert isinstance(display, Display)
        
        # Test that we can use it
        display.add_line("Test singleton")
        assert "Test singleton" in display.lines
    
    @patch('builtins.input')
    def test_complete_menu_interaction(self, mock_input):
        """Test a complete menu interaction scenario."""
        display = Display()
        mock_input.return_value = "2"
        
        options = ["Go to forest", "Rest at inn", "Check stats"]
        status = "You are at the village square."
        
        with patch.object(display, 'refresh_display'):
            result = display.display_menu("Village Square", options, status)
        
        assert result == "2"
        assert len(display.lines) > 0
        
        # Clean up for next test
        display.clear_screen()
    
    def test_error_handling_in_display(self):
        """Test error handling in display methods."""
        display = Display()
        
        # Test with None values (should not crash)
        try:
            display.add_line(None)
            display.set_footer(None)
            # If we get here, error handling worked or method was defensive
            assert True
        except Exception:
            # If an exception occurs, it should be handled gracefully
            assert False, "Display methods should handle None values gracefully"
    
    def test_large_content_handling(self):
        """Test display with large amounts of content."""
        display = Display()
        
        # Add many lines
        for i in range(100):
            display.add_line(f"Line {i}")
        
        assert len(display.lines) == 100
        
        # Should be able to refresh without issues
        with patch('os.system'), patch('builtins.print'):
            try:
                display.refresh_display()
                assert True
            except Exception:
                assert False, "Should handle large content gracefully"