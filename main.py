#!/usr/bin/env python3
"""
PythonDungeon - A Text-Based Dungeon Crawler Game
"""

def display_welcome():
    """Display the welcome message to the player."""
    print("=" * 50)
    print("    Welcome to PythonDungeon!")
    print("=" * 50)
    print()
    print("You find yourself standing at the entrance of a dark,")
    print("mysterious dungeon. Ancient stones line the walls,")
    print("and you can hear strange sounds echoing from within.")
    print()
    print("Your adventure begins now...")
    print()

def main():
    """Main game function."""
    display_welcome()
    
    # Get player's name
    player_name = input("What is your name, brave adventurer? ").strip()
    
    if not player_name:
        player_name = "Unknown Hero"
    
    print(f"\nGreetings, {player_name}!")
    print("Prepare yourself for the challenges that lie ahead.")
    print("\n" + "-" * 50)
    print("Your dungeon crawling adventure starts here!")
    print("(More features coming soon...)")
    print("-" * 50)

if __name__ == "__main__":
    main()