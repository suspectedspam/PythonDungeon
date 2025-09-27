#!/usr/bin/env python3

from time import time
from src.core.player import Player
from src.locations.inn import Inn
from src.ui.display import display

def display_welcome():
    """Display the welcome message to the player."""
    welcome_text = """Welcome to PythonDungeon!

You are a brave adventurer who has arrived at
the Cozy Dragon Inn, a safe haven for travelers
on the edge of a mysterious forest.

Your adventure begins now..."""
    
    # Exposition text - character by character
    display.display_text(welcome_text, exposition=True, pause=True, title="Welcome Adventurer")

def game_loop(player, inn):
    """Main game loop with display system."""
    
    while player.is_alive:
        result = inn.show_inn_menu(player)
        
        if result == "quit":
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
    
    # Start main game loop
    game_loop(player, inn)

if __name__ == "__main__":
    main()