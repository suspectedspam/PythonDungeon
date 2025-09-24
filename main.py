#!/usr/bin/env python3
"""
PythonDungeon - A Text-Based Dungeon Crawler Game
"""

from player import create_player
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

def create_character():
    """Create a new player character using the display system."""
    # Use the display system for character creation
    display.set_header("CHARACTER CREATION")
    display.add_line("")
    display.add_line("🎭 CHARACTER CREATION")
    display.add_line("-" * 20)
    display.add_line("")
    display.add_line("What is your name, brave adventurer?")
    
    # Set footer with input prompt and refresh display
    display.set_footer("Enter your name: ")
    display.refresh_display()
    
    # Get player's name
    while True:
        try:
            player_name = input().strip()
            if player_name:
                break
            display.add_line("Please enter a valid name.")
            display.set_footer("Enter your name: ")
            display.refresh_display()
        except (EOFError, KeyboardInterrupt):
            print("\nGame interrupted.")
            return None
    
    # Clear footer after getting input
    display.set_footer("")
    
    # Create player with default stats
    player = create_player(player_name)
    
    creation_text = f"""
Greetings, {player_name}!
You are now ready to begin your adventure!

📊 {player_name} Stats:
   Level: {player.level}
   Health: {player.current_health}/{player.max_health}
   Strength: {player.strength}
   Status: {player.get_health_status()}

{player.name} arrives at the inn, ready for adventure!"""
    
    # Regular text - line by line, appends to scroll
    display.display_text(creation_text, title="Character Created")
    
    return player
    
    return player

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
            "🚪 Quit game"
        ]
        
        status_text = f"The warm fireplace crackles as adventurers share\ntales of their journeys. The innkeeper nods\nwelcomingly as you approach the bar.\n\n{player.name} (Lvl {player.level}): {player.current_health}/{player.max_health} HP ({player.get_health_status()}) | Strength: {player.strength}"
        
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
            
            # Regular text - line by line
            display.display_text(rest_text, title="Resting at the Inn")
            
        elif choice == "2":  # Forest adventure
            print("\n🌲 You head towards the forest...")
            
            result = forest.start_adventure(player)
            
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
            
        elif choice == "4":  # Quit
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
    
    # Create character
    player = create_character()
    
    # Initialize game systems
    inn = Inn()
    forest = Forest()
    
    # Start main game loop
    game_loop(player, inn, forest)

if __name__ == "__main__":
    main()