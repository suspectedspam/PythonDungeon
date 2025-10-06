#!/usr/bin/env python3
"""
Game settings management for PythonDungeon
Handles auto-save preferences and other game configuration options
"""

import time
import os
import json
from src.ui.display import display

class GameSettings:
    """Manages game settings and preferences interface."""
    
    def __init__(self):
        """Initialize the game settings manager."""
        self.debug_mode = False  # Debug mode for fast testing
        self.auto_save = True    # Automatic save functionality
        self.text_speed = 0.3    # Text scrolling speed (0.1 - 1.0)
        
        # Load settings from file if it exists
        self.load_settings()
    
    def show_settings_menu(self, player):
        """
        Show and handle the settings menu.
        
        Args:
            player: The player object with settings methods
        """
        settings = player.get_settings()
        
        while True:
            # Show current settings
            display.set_header("GAME SETTINGS")
            display.add_line("", delay=0.3)
            display.add_line("⚙️ GAME SETTINGS", delay=0.6)
            display.add_line("-" * 20, delay=0.4)
            display.add_line("", delay=0.3)
            
            display.add_line("Current Auto-Save Settings:", delay=0.4)
            display.add_line(f"1. After Resting: {'✅ Enabled' if settings['auto_save_after_rest'] else '❌ Disabled'}", delay=0.2)
            display.add_line(f"2. After Combat: {'✅ Enabled' if settings['auto_save_after_combat'] else '❌ Disabled'}", delay=0.2)
            display.add_line(f"3. On Inn Visit: {'✅ Enabled' if settings['auto_save_on_inn_visit'] else '❌ Disabled'}", delay=0.2)
            display.add_line("", delay=0.3)
            display.add_line("4. 🔙 Back to Inn", delay=0.2)
            
            display.set_footer("Choose setting to toggle (1-4): ")
            display.refresh_display()
            
            try:
                choice = input().strip()
                
                if choice == "1":
                    settings['auto_save_after_rest'] = not settings['auto_save_after_rest']
                    player.update_settings(settings)
                    display.add_line(f"✅ Auto-save after rest: {'Enabled' if settings['auto_save_after_rest'] else 'Disabled'}", delay=0.4)
                    
                elif choice == "2":
                    settings['auto_save_after_combat'] = not settings['auto_save_after_combat']
                    player.update_settings(settings)
                    display.add_line(f"⚔️ Auto-save after combat: {'Enabled' if settings['auto_save_after_combat'] else 'Disabled'}", delay=0.4)
                    
                elif choice == "3":
                    settings['auto_save_on_inn_visit'] = not settings['auto_save_on_inn_visit']
                    player.update_settings(settings)
                    display.add_line(f"🏠 Auto-save on inn visit: {'Enabled' if settings['auto_save_on_inn_visit'] else 'Disabled'}", delay=0.4)
                    
                elif choice == "4":
                    # Clear footer when leaving
                    display.set_footer("")
                    return
                
                else:
                    display.add_line("❌ Invalid choice. Please choose 1-4.", delay=0.3)
                    
            except (EOFError, KeyboardInterrupt):
                # Clear footer when interrupted
                display.set_footer("")
                return
                
            # Brief pause before next menu display
            time.sleep(0.5)
    
    def export_settings(self, player):
        """
        Export player settings to a dictionary for backup.
        
        Args:
            player: The player object with settings methods
            
        Returns:
            dict: Player settings
        """
        return player.get_settings()
    
    def import_settings(self, player, settings_dict):
        """
        Import settings from a dictionary.
        
        Args:
            player: The player object to import settings to
            settings_dict (dict): Settings to import
        """
        # Validate settings before importing
        valid_keys = {'auto_save_after_rest', 'auto_save_after_combat', 'auto_save_on_inn_visit'}
        
        if all(key in valid_keys for key in settings_dict.keys()):
            player.update_settings(settings_dict)
            display.add_line("⚙️ Settings imported successfully!", delay=0.4)
        else:
            display.add_line("❌ Invalid settings format!", delay=0.4)
    
    def toggle_debug_mode(self):
        """Toggle debug mode on/off."""
        self.debug_mode = not self.debug_mode
        
        # Update the display system with new delay settings
        if self.debug_mode:
            display.set_debug_mode(True)
            display.add_line("🐛 DEBUG MODE: ON - Fast text scrolling enabled", delay=0)
        else:
            display.set_debug_mode(False)
            display.add_line("🐛 DEBUG MODE: OFF - Normal text scrolling restored", delay=0.3)
    
    def is_debug_mode(self):
        """Check if debug mode is enabled."""
        return self.debug_mode
    
    def save_settings(self):
        """Save current settings to file."""
        try:
            # Ensure config directory exists
            config_dir = "config"
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            # Save settings as JSON
            settings_data = {
                "debug_mode": self.debug_mode,
                "auto_save": self.auto_save,
                "text_speed": self.text_speed
            }
            
            with open(os.path.join(config_dir, "settings.json"), 'w') as f:
                json.dump(settings_data, f, indent=2)
                
        except (OSError, IOError, PermissionError):
            # Handle file system errors gracefully
            pass
    
    def load_settings(self):
        """Load settings from file."""
        try:
            settings_file = os.path.join("config", "settings.json")
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings_data = json.load(f)
                
                # Apply loaded settings with validation
                if isinstance(settings_data, dict):
                    self.debug_mode = settings_data.get("debug_mode", False)
                    self.auto_save = settings_data.get("auto_save", True)
                    text_speed = settings_data.get("text_speed", 0.3)
                    
                    # Validate text_speed bounds
                    self.text_speed = max(0.1, min(1.0, text_speed))
                    
        except (OSError, IOError, json.JSONDecodeError, PermissionError):
            # Handle file system and JSON errors gracefully
            # Keep default values if loading fails
            pass

# Global game settings instance
game_settings = GameSettings()