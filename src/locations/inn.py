#!/usr/bin/env python3
import random
from src.locations.adventure import Adventure
from src.ui.display import display
from src.config.gamesettings import game_settings
from src.debug.debug_menu import debug_menu

class Inn:
    """Manages the inn location and rest functionality."""
    
    def __init__(self):
        """Initialize the inn system."""
        self.current_location = "inn"
    
    def show_inn(self, player):
        """
        Display the inn and available options.
        
        Args:
            player: The player object
        """
        print("\n" + "=" * 50)
        print("🏠 Welcome to the Cozy Dragon Inn!")
        print("=" * 50)
        print("The warm fireplace crackles as adventurers share")
        print("tales of their journeys. The innkeeper nods")
        print("welcomingly as you approach the bar.")
        print()
        
        player.display_status()
    
    def rest_at_inn(self, player):
        """
        Player rests at the inn to restore health.
        
        Args:
            player: The player object
            
        Returns:
            bool: True if player rested, False if already at full health
        """
        if player.current_health == player.max_health:
            print("\n💤 You're already feeling great! No need to rest.")
            return False
        
        restored = player.rest()
        print(f"\n💤 You rest peacefully at the inn...")
        print(f"💚 You feel fully rested and restored! (+{healed} HP)")
        return "rested"
    
    def show_inn_menu(self, player):
        """
        Show the inn menu and handle player choices.
        
        Args:
            player: The player object
            
        Returns:
            str: Result of the menu interaction ("continue", "quit")
        """
        inn_options = [
            "🛏️ Rest (Restore full health)",
            "🗺️ Go on an adventure", 
            "📊 View your stats",
            "💾 Save game",
            "⚙️ Settings",
            "🚪 Quit game"
        ]
        
        status_text = f"The warm fireplace crackles as adventurers share\ntales of their journeys. The innkeeper nods\nwelcomingly as you approach the bar.\n\n{player.emoji} {player.name} (Lvl {player.level}): {player.current_health}/{player.max_health} HP"
        
        # Always append to scrolling content
        choice = display.display_menu("Welcome to the Cozy Dragon Inn! 🏠", inn_options, status_text, exposition_intro=False)
        
        # Handle special debug command
        if choice == "debug":
            debug_menu.show_debug_menu(player)
            return "continue"
        
        if choice == "quit":
            return "quit"
            
        if choice == "1":  # Rest
            if player.current_health == player.max_health:
                rest_text = "💤 You're already feeling great! No need to rest."
            else:
                restored = player.rest()
                rest_text = f"""💤 You rest peacefully at the inn...
                                💚 You restored {restored} HP and feel refreshed!
                                🏠 Ready for your next adventure!"""
                # Auto-save after resting (if enabled)
                player.auto_save("rest")
            
            # Regular text - line by line
            display.display_text(rest_text, title="Resting at the Inn")
            
        elif choice == "2":  # Adventure selection
            
            result = Adventure.show_adventure_selection_menu(player)
            
            if result != "cancelled":
                # Auto-save after adventure (if enabled)
                player.auto_save("combat")
                
                # Clear HP header when returning from adventure
                display.clear_hp_header()
                
                # Handle adventure results
                if result == "victory":
                    result_text = "🎉 You return to the inn victorious after your adventure!"
                elif result == "defeat":
                    result_text = "💔 You limp back to the inn, defeated but alive..."
                elif result == "fled":
                    result_text = "🏃 You return to the inn safely after fleeing from danger."
                elif result == "returned":
                    result_text = "🏠 You return to the inn after your exploration."
                else:
                    result_text = "🏠 You return to the inn."
                
                # Regular text - line by line
                display.display_text(result_text, title="Return to Inn")
            
        elif choice == "3":  # View stats
            display.display_stats(player)
            
        elif choice == "4":  # Save game
            player.manual_save()
            
        elif choice == "5":  # Settings
            game_settings.show_settings_menu(player)
            
        elif choice == "6":  # Quit
            # Save before quitting
            player.auto_save()
            return "quit"
        
        return "continue"