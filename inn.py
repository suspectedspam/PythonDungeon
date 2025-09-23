#!/usr/bin/env python3
"""
Inn system for PythonDungeon
Handles the inn location and player rest mechanics
"""

import random

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
        print()
        
        print("What would you like to do?")
        print("1. 🛏️  Rest (Restore full health)")
        print("2. 🌲 Go on an adventure in the Forest")
        print("3. 📊 View your stats")
        print("4. 🚪 Quit game")
        print()
    
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
        print(f"💚 You restored {restored} HP and feel refreshed!")
        print("🏠 Ready for your next adventure!")
        return True
    
# Example usage and testing
if __name__ == "__main__":
    from player import create_player
    
    print("=== Inn System Test ===")
    print()
    
    # Create test player
    player = create_player("TestHero")
    inn = Inn()
    
    # Test inn display
    inn.show_inn(player)
    
    # Test resting
    # Damage player first to test rest
    player.update_health(25)
    print("Player takes some damage for testing...")
    player.display_status()
    
    result = inn.rest_at_inn(player)
    print(f"Rest result: {result}")
    player.display_status()