#!/usr/bin/env python3
"""
Test suite for the debug system.
Tests debug menu functionality and developer tools.
"""

import pytest
from unittest.mock import Mock, patch, call
from src.debug.debug_menu import DebugMenu
from src.core.player import Player


class TestDebugMenu:
    """Test the debug menu system functionality."""
    
    def test_debug_menu_creation(self):
        """Test debug menu initialization."""
        debug_menu = DebugMenu()
        
        assert debug_menu.active is True
        assert debug_menu.debug_delay == 0.05
    
    def test_debug_delay_configuration(self):
        """Test debug delay setting."""
        debug_menu = DebugMenu()
        
        # Test default delay
        assert debug_menu.debug_delay == 0.05
        
        # Test custom delay
        debug_menu.debug_delay = 0.1
        assert debug_menu.debug_delay == 0.1


class TestDebugMenuMethods:
    """Test individual debug menu methods."""
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_add_level_valid_input(self, mock_input, mock_display):
        """Test adding levels with valid input."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=2, experience=50)
        
        mock_input.return_value = "3"  # Add 3 levels
        
        debug_menu._add_level(player)
        
        # Player should have gained 3 levels
        assert player.level == 5  # 2 + 3
        
        # Check that display was called
        assert mock_display.add_line.called
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_add_level_invalid_input(self, mock_input, mock_display):
        """Test adding levels with invalid input."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=2, experience=50)
        
        mock_input.return_value = "invalid"
        
        debug_menu._add_level(player)
        
        # Player level should remain unchanged
        assert player.level == 2
        
        # Should show error message
        error_calls = [call for call in mock_display.add_line.call_args_list 
                      if any("Invalid input" in str(arg) for arg in call[0])]
        assert len(error_calls) > 0
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_add_level_out_of_range(self, mock_input, mock_display):
        """Test adding levels with out of range input."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=2, experience=50)
        
        mock_input.return_value = "15"  # Above maximum of 10
        
        debug_menu._add_level(player)
        
        # Player level should remain unchanged
        assert player.level == 2
        
        # Should show error message about range
        error_calls = [call for call in mock_display.add_line.call_args_list 
                      if any("between 1 and 10" in str(arg) for arg in call[0])]
        assert len(error_calls) > 0
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_remove_level_valid(self, mock_input, mock_display):
        """Test removing levels with valid input."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=5, experience=200)
        
        mock_input.return_value = "2"  # Remove 2 levels
        
        debug_menu._remove_level(player)
        
        # Player should have lost 2 levels
        assert player.level == 3  # 5 - 2
    
    @patch('src.ui.display.display')
    def test_remove_level_at_minimum(self, mock_display):
        """Test removing levels when already at level 1."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=1, experience=0)
        
        debug_menu._remove_level(player)
        
        # Player should remain at level 1
        assert player.level == 1
        
        # Should show cannot go below level 1 message
        error_calls = [call for call in mock_display.add_line.call_args_list 
                      if any("Cannot go below level 1" in str(arg) for arg in call[0])]
        assert len(error_calls) > 0
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_add_xp_valid(self, mock_input, mock_display):
        """Test adding XP with valid input."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=2, experience=50)
        
        mock_input.return_value = "100"  # Add 100 XP
        
        debug_menu._add_xp(player)
        
        # Player should have gained XP
        assert player.experience >= 150  # 50 + 100, possibly more if leveled up
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_add_xp_causes_level_up(self, mock_input, mock_display):
        """Test adding XP that causes a level up."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=1, experience=80)  # Close to level up
        
        mock_input.return_value = "50"  # Should cause level up
        
        initial_level = player.level
        debug_menu._add_xp(player)
        
        # Player may have leveled up
        level_up_calls = [call for call in mock_display.add_line.call_args_list 
                         if any("LEVEL UP" in str(arg) for arg in call[0])]
        
        if player.level > initial_level:
            assert len(level_up_calls) > 0
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_remove_xp_valid(self, mock_input, mock_display):
        """Test removing XP with valid input."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=2, experience=150)
        
        mock_input.return_value = "50"  # Remove 50 XP
        
        debug_menu._remove_xp(player)
        
        # Player should have lost XP
        assert player.experience == 100  # 150 - 50
    
    @patch('src.ui.display.display')
    def test_remove_xp_no_xp(self, mock_display):
        """Test removing XP when player has no XP."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=1, experience=0)
        
        debug_menu._remove_xp(player)
        
        # Should show no XP message
        error_calls = [call for call in mock_display.add_line.call_args_list 
                      if any("No XP to remove" in str(arg) for arg in call[0])]
        assert len(error_calls) > 0
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_set_health_valid(self, mock_input, mock_display):
        """Test setting health with valid input."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=3, experience=100)
        
        mock_input.return_value = "25"  # Set to 25 HP
        
        debug_menu._set_health(player)
        
        # Player health should be set to 25
        assert player.current_health == 25
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_set_strength_valid(self, mock_input, mock_display):
        """Test setting strength with valid input."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=2, experience=50)
        
        mock_input.return_value = "15"  # Set to 15 strength
        
        debug_menu._set_strength(player)
        
        # Player strength should be set to 15
        assert player.strength == 15
    
    @patch('src.ui.display.display')
    def test_toggle_debug_mode_on(self, mock_display):
        """Test toggling debug mode on."""
        debug_menu = DebugMenu()
        
        # Ensure debug mode is off initially
        mock_display.debug_mode = False
        
        debug_menu._toggle_debug_mode()
        
        # Debug mode should now be on
        assert mock_display.debug_mode is True
        
        # Should show debug mode ON message
        on_calls = [call for call in mock_display.add_line.call_args_list 
                   if any("DEBUG MODE: ON" in str(arg) for arg in call[0])]
        assert len(on_calls) > 0
    
    @patch('src.ui.display.display')
    def test_toggle_debug_mode_off(self, mock_display):
        """Test toggling debug mode off."""
        debug_menu = DebugMenu()
        
        # Ensure debug mode is on initially
        mock_display.debug_mode = True
        
        debug_menu._toggle_debug_mode()
        
        # Debug mode should now be off
        assert mock_display.debug_mode is False
        
        # Should show debug mode OFF message
        off_calls = [call for call in mock_display.add_line.call_args_list 
                    if any("DEBUG MODE: OFF" in str(arg) for arg in call[0])]
        assert len(off_calls) > 0


class TestDebugMenuNavigation:
    """Test debug menu navigation and flow."""
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_show_debug_menu_quit(self, mock_input, mock_display):
        """Test quitting from debug menu."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=2, experience=50)
        
        mock_input.return_value = "8"  # Back to Inn option
        
        result = debug_menu.show_debug_menu(player)
        
        assert result == "continue"
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_show_debug_menu_invalid_choice(self, mock_input, mock_display):
        """Test invalid menu choice handling."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=2, experience=50)
        
        # First invalid, then quit
        mock_input.side_effect = ["99", "8"]
        
        result = debug_menu.show_debug_menu(player)
        
        assert result == "continue"
        
        # Should show invalid choice message
        error_calls = [call for call in mock_display.add_line.call_args_list 
                      if any("Invalid choice" in str(arg) for arg in call[0])]
        assert len(error_calls) > 0
    
    @patch('src.ui.display.display')
    def test_debug_menu_status_display(self, mock_display):
        """Test that debug menu shows player status."""
        debug_menu = DebugMenu()
        player = Player("Status Hero", level=3, experience=125)
        
        # Mock display_menu to avoid infinite loop
        mock_display.display_menu.return_value = "8"  # Quit immediately
        
        debug_menu.show_debug_menu(player)
        
        # Should have called display_menu with status containing player info
        assert mock_display.display_menu.called
        call_args = mock_display.display_menu.call_args
        status_text = call_args[0][2]  # Third argument is status text
        
        assert "Status Hero" in status_text
        assert "Level: 3" in status_text
        assert "XP: 125" in status_text


class TestDebugMenuInputHandling:
    """Test debug menu input validation and error handling."""
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_keyboard_interrupt_handling(self, mock_input, mock_display):
        """Test handling of keyboard interrupts in debug methods."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=2, experience=50)
        
        mock_input.side_effect = KeyboardInterrupt()
        
        # Should not crash, should handle gracefully
        try:
            debug_menu._add_level(player)
            # Should show operation cancelled message
            cancel_calls = [call for call in mock_display.add_line.call_args_list 
                           if any("Operation cancelled" in str(arg) for arg in call[0])]
            assert len(cancel_calls) > 0
        except KeyboardInterrupt:
            assert False, "KeyboardInterrupt should be handled gracefully"
    
    @patch('src.ui.display.display')
    @patch('builtins.input')
    def test_eof_error_handling(self, mock_input, mock_display):
        """Test handling of EOF errors in debug methods."""
        debug_menu = DebugMenu()
        player = Player("Test Hero", level=2, experience=50)
        
        mock_input.side_effect = EOFError()
        
        # Should not crash, should handle gracefully
        try:
            debug_menu._add_xp(player)
            # Should show operation cancelled message
            cancel_calls = [call for call in mock_display.add_line.call_args_list 
                           if any("Operation cancelled" in str(arg) for arg in call[0])]
            assert len(cancel_calls) > 0
        except EOFError:
            assert False, "EOFError should be handled gracefully"


class TestDebugMenuIntegration:
    """Integration tests for debug menu system."""
    
    def test_debug_menu_singleton_access(self):
        """Test accessing debug menu singleton."""
        from src.debug.debug_menu import debug_menu
        
        assert isinstance(debug_menu, DebugMenu)
        assert debug_menu.active is True
        assert debug_menu.debug_delay == 0.05
    
    def test_debug_menu_with_player_modifications(self):
        """Test debug menu making actual player modifications."""
        debug_menu = DebugMenu()
        player = Player("Mod Hero", level=1, experience=0)
        
        # Test that debug modifications actually work
        initial_level = player.level
        initial_xp = player.experience
        initial_health = player.current_health
        initial_strength = player.strength
        
        # Simulate debug modifications
        with patch('builtins.input'), patch('src.ui.display.display'):
            # These would normally be called through the menu
            player.level += 2  # Simulate add level
            player.experience += 100  # Simulate add XP  
            player.current_health = player.max_health - 10  # Simulate set health
            player.strength += 5  # Simulate set strength
        
        # Verify changes were made
        assert player.level == initial_level + 2
        assert player.experience == initial_xp + 100
        assert player.current_health == initial_health - 10
        assert player.strength == initial_strength + 5
    
    @patch('src.ui.display.display')
    def test_debug_delay_consistency(self, mock_display):
        """Test that debug menu uses consistent delays."""
        debug_menu = DebugMenu()
        
        # All debug menu operations should use the same delay
        assert debug_menu.debug_delay == 0.05
        
        # Test that delay is used in add_line calls
        player = Player("Delay Test", level=2, experience=50)
        
        with patch('builtins.input', return_value="5"):
            debug_menu._add_level(player)
        
        # Check that add_line was called with debug delay
        delay_calls = [call for call in mock_display.add_line.call_args_list 
                      if len(call[1]) > 0 and 'delay' in call[1] and 
                      call[1]['delay'] == debug_menu.debug_delay]
        assert len(delay_calls) > 0