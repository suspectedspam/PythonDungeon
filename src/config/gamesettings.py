#!/usr/bin/env python3
"""
Game settings management for PythonDungeon
Handles auto-save preferences and other game configuration options
"""

from src.ui.display import display

class GameSettings:
    """Manages game settings and preferences interface."""
    
    def __init__(self):
        """Initialize the game settings manager."""
        pass
    
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
                    status = "enabled" if settings['auto_save_after_rest'] else "disabled"
                    display.add_line(f"✅ Auto-save after resting {status}!", delay=0.4)
                    player.update_settings(settings)
                
                elif choice == "2":
                    settings['auto_save_after_combat'] = not settings['auto_save_after_combat']
                    status = "enabled" if settings['auto_save_after_combat'] else "disabled"
                    display.add_line(f"✅ Auto-save after combat {status}!", delay=0.4)
                    player.update_settings(settings)
                
                elif choice == "3":
                    settings['auto_save_on_inn_visit'] = not settings['auto_save_on_inn_visit']
                    status = "enabled" if settings['auto_save_on_inn_visit'] else "disabled"
                    display.add_line(f"✅ Auto-save on inn visit {status}!", delay=0.4)
                    player.update_settings(settings)
                
                elif choice == "4":
                    display.add_line("🏠 Returning to inn...", delay=0.4)
                    break
                
                else:
                    display.add_line("Please choose a valid option (1-4).")
            
            except (EOFError, KeyboardInterrupt):
                break
    
    def get_setting_description(self, setting_name):
        """
        Get a user-friendly description of a setting.
        
        Args:
            setting_name (str): Internal setting name
            
        Returns:
            str: Human-readable description
        """
        descriptions = {
            'auto_save_after_rest': 'Automatically save when resting at the inn',
            'auto_save_after_combat': 'Automatically save after forest adventures and battles',
            'auto_save_on_inn_visit': 'Automatically save every time you return to the inn'
        }
        return descriptions.get(setting_name, setting_name)
    
    def reset_settings_to_default(self, player):
        """
        Reset all settings to their default values.
        
        Args:
            player: The player object to reset settings for
        """
        default_settings = {
            'auto_save_after_rest': True,
            'auto_save_after_combat': True,
            'auto_save_on_inn_visit': False
        }
        
        player.update_settings(default_settings)
        display.add_line("⚙️ Settings reset to defaults!", delay=0.4)
    
    def export_settings(self, player):
        """
        Export player settings for backup or sharing.
        
        Args:
            player: The player object to export settings from
            
        Returns:
            dict: Dictionary of current settings
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

# Create global settings manager instance
game_settings = GameSettings()