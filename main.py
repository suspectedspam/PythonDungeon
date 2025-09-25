#!/usr/bin/env python3
"""
Pyt        inn_options = [
            "🛏️ Rest (Restore full        inn_options = [
            "🛏️ Rest (Restore full health)",
            "🌲 Go on an adventure in the Forest", 
            "📊 View your stats",
            "💾 Save game",
            "⚙️ Settings",
            "🚪 Quit game"
        ])",
            "🌲 Go on an adventure in the Forest", 
            "📊 View your stats",
            "💾 Save game",
            "⚙️ Settings",
            "🚪 Quit game"
        ]eon - A Text-Based Dungeon Crawler Game
"""

from player import Player
from inn import Inn
from forest import Forest
from display import display

def display_welcome():
    """Display the welcome message to the player."""
    welcome_text = """Welcome to PythonDungeon!

You are a brave adventurer who has arrived at
the Cozy Dragon Inn, a safe haven for travelers
on the edge of a mysterious forest.

Your adventure begins now..."""
    
    # Exposition text - character by character
    display.display_text(welcome_text, exposition=True, pause=True, title="Welcome Adventurer")


def show_settings_menu(player):
    """Show and handle the settings menu."""
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

def game_loop(player, inn, forest):
    """Main game loop with display system."""
    
    # Content should already be initialized from previous steps
    # No need to clear - let character creation content remain in scroll
    
    while player.is_alive:
        # Show inn menu using display system
        inn_options = [
            "🛏️ Rest (Restore full health)",
            "🌲 Go on an adventure in the Forest", 
            "📊 View your stats",
            "� Save game",
            "�🚪 Quit game"
        ]
        
        status_text = f"The warm fireplace crackles as adventurers share\ntales of their journeys. The innkeeper nods\nwelcomingly as you approach the bar.\n\n{player.emoji} {player.name} (Lvl {player.level}): {player.current_health}/{player.max_health} HP"
        
        # Always append to scrolling content
        choice = display.display_menu("Welcome to the Cozy Dragon Inn! 🏠", inn_options, status_text, exposition_intro=False)
        
        if choice == "quit":
            break
            
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
            
        elif choice == "2":  # Forest adventure
            print("\n🌲 You head towards the forest...")
            
            result = forest.start_adventure(player)
            
            # Auto-save after forest adventure (if enabled)
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
                result_text = "🏠 You return to the inn after your forest exploration."
            else:
                result_text = "🏠 You return to the inn."
            
            # Regular text - line by line
            display.display_text(result_text, title="Return to Inn")
            
        elif choice == "3":  # View stats
            display.display_stats(player)
            
        elif choice == "4":  # Save game
            player.manual_save()
            
        elif choice == "5":  # Settings
            show_settings_menu(player)
            
        elif choice == "6":  # Quit
            # Save before quitting
            player.auto_save()
            break
    
    # End game message - exposition
    if not player.is_alive:
        end_text = f"""💀 {player.name} has fallen in battle.
Your adventure ends here..."""
    else:
        end_text = f"""👋 Farewell, {player.name}!
Thanks for playing PythonDungeon!"""
    
    # Exposition text for dramatic ending
    display.display_text(end_text, exposition=True, pause=True, title="Game Over")

def main():
    """Main game function."""
    # Clear content at the very start of the game
    display.clear_content()
    
    display_welcome()
    
    # Load existing character or create new one
    player = Player.load_or_create_character()
    
    # Check if player creation/loading was cancelled
    if player is None:
        display.add_line("👋 Thanks for playing PythonDungeon!")
        return
    
    # Initialize game systems
    inn = Inn()
    forest = Forest()
    
    # Start main game loop
    game_loop(player, inn, forest)

if __name__ == "__main__":
    main()