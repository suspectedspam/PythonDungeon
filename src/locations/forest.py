#!/usr/bin/env python3
"""
Forest adventure system for PythonDungeon
Handles forest encounters, monsters, and exploration
"""

import random
from src.locations.adventure import Adventure

class Forest(Adventure):
    """Manages forest adventures and encounters."""
    
    def __init__(self):
        """Initialize the forest adventure system."""
        super().__init__()
        self.set_encounter_rate(0.8)  # 80% encounter rate for forest
    
    # Abstract method implementations
    def get_location_name(self):
        """Return the name of this location."""
        return "Forest"
    
    def get_location_emoji(self):
        """Return the emoji for this location."""
        return "🌲"
    
    def get_location_intro(self):
        """Return the intro text for entering the forest."""
        return """You venture into the dense woodland...
Sunlight filters through the canopy above.
The forest is alive with rustling sounds.

Adventure awaits in the mysterious depths ahead!"""
    
    def get_peaceful_events(self):
        """Return peaceful events that can happen in the forest."""
        return [
            "🍄 You discover some healing mushrooms and feel refreshed!",
            "🌸 You find a beautiful clearing with flowers that restore your spirits.",
            "🐦 Colorful birds chirp melodiously in the trees above.",
            "🦋 Butterflies dance around you in a magical display.",
            "🌿 You find a peaceful stream and take a refreshing drink.",
            "🐿️ A friendly squirrel chatters at you from a nearby tree.",
            "☀️ Warm sunlight breaks through the canopy, lifting your mood.",
            "🌳 You discover an ancient tree that seems to whisper old secrets.",
            "🌺 You stumble upon a hidden grove filled with beautiful wildflowers.",
            "🦉 An owl hoots wisely from somewhere in the branches above."
        ]
    
    def create_location_monster(self, player_level):
        """Create a monster appropriate for the forest and player level."""
        return self.create_forest_monster(player_level)
    
    def create_forest_monster(self, player_level=1):
        """
        Create a monster appropriate for forest encounters using the database.
        
        Args:
            player_level (int): Player's current level for scaling
            
        Returns:
            Monster: A forest-appropriate monster from the database
        """
        from src.entities.monster import Monster
        
        # Use database-driven monster creation
        return Monster.create_random_for_level(player_level)
    

                # If continue, loop again for another encounter
    


# Example usage and testing
if __name__ == "__main__":
    from src.core.player import create_player
    
    print("=== Forest System Test ===")
    print()
    
    # Create test player and forest
    player = create_player("TestHero")
    forest = Forest()
    
    # Test forest adventure
    result = forest.start_adventure(player)
    print(f"\nAdventure result: {result}")
    
    player.display_status()