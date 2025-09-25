#!/usr/bin/env python3
"""
Forest adventure system for PythonDungeon
Handles forest encounters, monsters, and exploration
"""

import random
from combat import Combat
from display import display

class Forest:
    """Manages forest adventures and encounters."""
    
    def __init__(self):
        """Initialize the forest system."""
        self.combat = Combat()
    
    def create_forest_monster(self, player_level=1):
        """
        Create a monster appropriate for forest encounters using the database.
        
        Args:
            player_level (int): Player's current level for scaling
            
        Returns:
            Monster: A forest-appropriate monster from the database
        """
        from monster import Monster
        
        # Use database-driven monster creation
        return Monster.create_random_for_level(player_level)
    
    def start_adventure(self, player):
        """
        Handle a forest adventure with potential for multiple encounters.
        
        Args:
            player: The player object
            
        Returns:
            str: Result of the adventure ("victory", "defeat", "fled", "peaceful", "returned")
        """
        forest_intro = """You venture into the dense woodland...
Sunlight filters through the canopy above.
The forest is alive with rustling sounds.

Adventure awaits in the mysterious depths ahead!"""
        
        # Enable HP display for forest adventure
        display.set_header("Forest Adventure")
        display.set_player_for_header(player)
        display.display_text(forest_intro, exposition=True, title="Forest Adventure")
        
        # Continue adventuring until player decides to return
        while True:
            # Random encounter chance
            encounter_chance = random.random()
            
            if encounter_chance < 0.8:  # 80% chance of monster encounter
                result = self.monster_encounter(player)
                
                # If player died, fled, or was defeated, end the adventure
                if result in ["defeat", "fled"]:
                    return result
                elif result == "victory":
                    # After victory, give choice to continue or return
                    continue_choice = self.ask_continue_adventure(player)
                    if continue_choice == "return":
                        return "returned"
                    # If continue, loop again for another encounter
                    
            else:  # 20% chance of peaceful exploration
                result = self.peaceful_exploration(player)
                
                # After peaceful exploration, give choice to continue or return  
                continue_choice = self.ask_continue_adventure(player)
                if continue_choice == "return":
                    return "returned"
                # If continue, loop again for another encounter
    
    def ask_continue_adventure(self, player):
        """
        Ask player if they want to continue adventuring or return to inn.
        
        Args:
            player: The player object
            
        Returns:
            str: "continue" or "return"
        """
        options = [
            "🌲 Continue exploring the forest",
            "🏠 Return to the inn"
        ]
        
        status_text = f"Current Status: {player.emoji} {player.name} (Lvl {player.level}): {player.current_health}/{player.max_health} HP"
        
        # Show continue choice (HP already in header)
        choice = display.display_menu("Adventure Choice", options, status_text)
        
        if choice == "1":
            # Variety of continue messages
            continue_messages = [
                """🌿 You decide to venture deeper into the forest...
The trees grow thicker and the shadows longer.""",
                """🍃 Curiosity drives you to explore further...
New paths wind deeper into the woodland.""",
                """🌱 The forest calls to you with mysteries yet unsolved...
You press onward through the undergrowth.""",
                """🌳 Adventure awaits in the heart of the forest...
You continue your journey with renewed determination."""
            ]
            
            continue_text = random.choice(continue_messages)
            # Show continue message (HP already in header)
            display.display_text(continue_text, title="Deeper into the Forest")
            return "continue"
        elif choice == "2" or choice == "quit":
            return_text = """🏠 You decide it's time to head back to the safety of the inn.
You carefully make your way back through the forest paths."""
            # Show return message and clear HP from header
            display.display_text(return_text, title="Returning to Inn")
            display.clear_hp_header()
            return "return"
        else:
            # Default to return if something goes wrong
            return "return"
    
    def monster_encounter(self, player):
        """
        Handle a monster encounter in the forest.
        
        Args:
            player: The player object
            
        Returns:
            str: Result of the encounter
        """
        monster = self.create_forest_monster(player.level)
        
        encounter_text = f"""🐉 A wild {monster.name} appears!
It looks hostile and ready to fight!

🐉 {monster.name} (Lvl {monster.level})"""
        
        # Show encounter info (HP already in header from forest adventure)
        display.display_text(encounter_text, title="Monster Encounter")
        
        # Start combat (which will update header to include enemy HP)
        return self.combat.run_combat(player, monster)
    
    def peaceful_exploration(self, player):
        """
        Handle peaceful forest exploration (no combat).
        
        Args:
            player: The player object
            
        Returns:
            str: Result of exploration ("peaceful")
        """
        events = [
            "🍄 You discover some healing mushrooms and feel refreshed!",
            "🌸 You find a beautiful clearing with flowers that restore your spirits.",
            "🦋 Butterflies guide you to a peaceful grove where you rest briefly.",
            "🌿 You discover medicinal herbs growing wild in the forest.",
            "🏞️ You enjoy the peaceful sounds of a babbling brook."
        ]
        
        event = random.choice(events)
        
        # Small healing bonus for peaceful exploration
        heal_text = ""
        if player.current_health < player.max_health:
            heal_amount = random.randint(3, 8)
            actual_healed = player.heal(heal_amount)
            if actual_healed > 0:
                heal_text = f"\n💚 You restored {actual_healed} HP from your peaceful journey!"
        
        peaceful_text = f"""{event}{heal_text}

The forest continues to beckon with more secrets to discover..."""
        
        # Show peaceful exploration (HP already in header)
        display.display_text(peaceful_text, title="Peaceful Discovery")
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