#!/usr/bin/env python3
"""
Forest adventure system for PythonDungeon
Handles forest encounters, monsters, and exploration
"""

import random
from monster import (create_goblin, create_skeleton, create_carnivorous_plant, 
                    create_dire_bat, create_dire_rat, create_owlbear, create_elf)
from combat import Combat

class Forest:
    """Manages forest adventures and encounters."""
    
    def __init__(self):
        """Initialize the forest system."""
        self.combat = Combat()
    
    def create_forest_monster(self, player_level=1):
        """
        Create a monster appropriate for forest encounters.
        
        Args:
            player_level (int): Player's current level for scaling
            
        Returns:
            Monster: A forest-appropriate monster
        """
        # Forest creatures that make sense in a woodland setting
        forest_creatures = [
            ("goblin", 0.25),        # Common forest dwellers
            ("dire_rat", 0.20),      # Forest vermin
            ("carnivorous_plant", 0.15), # Dangerous forest plants
            ("dire_bat", 0.15),      # Cave/forest bats
            ("skeleton", 0.10),      # Ancient remains in the woods
            ("elf", 0.10),          # Forest guardians gone rogue
            ("owlbear", 0.05),      # Rare, dangerous forest predator
        ]
        
        # Choose creature based on weighted probability
        rand = random.random()
        cumulative = 0
        
        for creature_type, probability in forest_creatures:
            cumulative += probability
            if rand <= cumulative:
                # Scale monster level based on player level (±1)
                monster_level = random.randint(max(1, player_level - 1), player_level + 1)
                
                if creature_type == "goblin":
                    return create_goblin(monster_level)
                elif creature_type == "dire_rat":
                    return create_dire_rat(monster_level)
                elif creature_type == "carnivorous_plant":
                    return create_carnivorous_plant(monster_level)
                elif creature_type == "dire_bat":
                    return create_dire_bat(monster_level)
                elif creature_type == "skeleton":
                    return create_skeleton(monster_level)
                elif creature_type == "elf":
                    return create_elf(monster_level)
                elif creature_type == "owlbear":
                    return create_owlbear(monster_level)
        
        # Fallback to goblin if something goes wrong
        return create_goblin(player_level)
    
    def start_adventure(self, player):
        """
        Handle a forest adventure encounter.
        
        Args:
            player: The player object
            
        Returns:
            str: Result of the adventure ("victory", "defeat", "fled", "peaceful")
        """
        print("\n" + "🌲" * 25)
        print("      FOREST ADVENTURE")
        print("🌲" * 25)
        print()
        print("You venture into the dense woodland...")
        print("Sunlight filters through the canopy above.")
        print("The forest is alive with rustling sounds.")
        print()
        
        # Random encounter chance
        encounter_chance = random.random()
        
        if encounter_chance < 0.8:  # 80% chance of monster encounter
            return self.monster_encounter(player)
        else:  # 20% chance of peaceful exploration
            return self.peaceful_exploration(player)
    
    def monster_encounter(self, player):
        """
        Handle a monster encounter in the forest.
        
        Args:
            player: The player object
            
        Returns:
            str: Result of the encounter
        """
        monster = self.create_forest_monster(player.level)
        
        print(f"🐉 A wild {monster.name} appears!")
        print("It looks hostile and ready to fight!")
        print()
        monster.display_status()
        print()
        
        print("What do you do?")
        print("1. ⚔️  Attack")
        print("2. 🏃 Try to flee")
        print()
        
        while True:
            try:
                choice = input("Choose your action (1-2): ").strip()
                if choice == "1":
                    return self.combat.run_combat(player, monster)
                elif choice == "2":
                    flee_result = self.attempt_flee()
                    if flee_result == "failed_flee":
                        # If flee fails, force combat
                        return self.combat.run_combat(player, monster)
                    else:
                        return flee_result
                else:
                    print("Please choose 1 or 2.")
            except (EOFError, KeyboardInterrupt):
                print("\nGame interrupted.")
                return "fled"
    
    def attempt_flee(self):
        """
        Attempt to flee from combat.
        
        Returns:
            str: Result of flee attempt
        """
        flee_chance = random.random()
        
        if flee_chance < 0.7:  # 70% chance to successfully flee
            print("\n🏃 You successfully escape into the forest!")
            print("🌲 You make it back to the inn safely.")
            return "fled"
        else:
            print("\n❌ You couldn't escape!")
            print("The creature blocks your path - you must fight!")
            return "failed_flee"
    
    def peaceful_exploration(self, player):
        """
        Handle peaceful forest exploration (no combat).
        
        Args:
            player: The player object
            
        Returns:
            str: Result of exploration
        """
        events = [
            "🍄 You discover some healing mushrooms and feel refreshed!",
            "🌸 You find a beautiful clearing with flowers that restore your spirits.",
            "🦋 Butterflies guide you to a peaceful grove where you rest briefly.",
            "🌿 You discover medicinal herbs growing wild in the forest.",
            "🏞️ You enjoy the peaceful sounds of a babbling brook."
        ]
        
        event = random.choice(events)
        print(event)
        
        # Small healing bonus for peaceful exploration
        if player.current_health < player.max_health:
            heal_amount = random.randint(3, 8)
            actual_healed = player.heal(heal_amount)
            if actual_healed > 0:
                print(f"💚 You restored {actual_healed} HP from your peaceful journey!")
        
        print("\n🏠 You return to the inn feeling content.")
        return "peaceful"

# Example usage and testing
if __name__ == "__main__":
    from player import create_player
    
    print("=== Forest System Test ===")
    print()
    
    # Create test player and forest
    player = create_player("TestHero")
    forest = Forest()
    
    # Test forest adventure
    result = forest.start_adventure(player)
    print(f"\nAdventure result: {result}")
    
    player.display_status()