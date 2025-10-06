#!/usr/bin/env python3
"""
Adventure base class for PythonDungeon
Provides common functionality for all adventure locations
"""

import random
from abc import ABC, abstractmethod
from src.ui.display import display
from src.core.combat import Combat

class Adventure(ABC):
    """
    Abstract base class for all adventure locations.
    
    Provides common adventure functionality that all locations share:
    - Combat system
    - Monster encounters  
    - Peaceful exploration
    - Adventure flow management
    - Player status tracking
    """
    
    def __init__(self):
        """Initialize the adventure with common systems."""
        self.combat = Combat()
        self.encounter_rate = 0.8  # Default 80% chance of encounters
        self.peaceful_events = []  # Override in subclasses
    
    @abstractmethod
    def get_location_name(self):
        """Return the name of this adventure location."""
        pass
    
    @abstractmethod  
    def get_location_emoji(self):
        """Return the emoji representing this location."""
        pass
    
    @abstractmethod
    def create_location_monster(self, player_level):
        """Create a monster appropriate for this location and player level."""
        pass
    
    @abstractmethod
    def get_location_intro(self):
        """Return the intro text for entering this location."""
        pass
    
    @abstractmethod
    def get_peaceful_events(self):
        """Return list of peaceful events that can happen in this location."""
        pass
    
    def start_adventure(self, player):
        """
        Handle an adventure with potential for multiple encounters.
        
        Args:
            player: The player object
            
        Returns:
            str: Result of the adventure ("victory", "defeat", "fled", "peaceful", "returned")
        """
        intro_text = self.get_location_intro()
        
        # Enable HP display for adventure
        display.set_header(f"{self.get_location_name()} Adventure")
        display.set_player_for_header(player)
        display.display_text(intro_text, exposition=True, title=f"{self.get_location_name()} Adventure")
        
        # Continue adventuring until player decides to return
        while True:
            # Random encounter chance
            encounter_chance = random.random()
            
            if encounter_chance < self.encounter_rate:
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
            else:
                # Peaceful exploration
                result = self.peaceful_exploration(player)
                
                # After peaceful event, give choice to continue or return  
                continue_choice = self.ask_continue_adventure(player)
                if continue_choice == "return":
                    return "returned"
    
    def monster_encounter(self, player):
        """
        Handle a monster encounter in this location.
        
        Args:
            player: The player object
            
        Returns:
            str: Result of combat ("victory", "defeat", "fled")
        """
        monster = self.create_location_monster(player.level)
        
        encounter_text = f"""You encounter a dangerous creature!

                            {monster.emoji} {monster.name} (Lvl {monster.level})"""
        
        # Show encounter info (HP already in header from adventure)
        display.display_text(encounter_text, title="Monster Encounter")
        
        # Start combat (which will update header to include enemy HP)
        return self.combat.run_combat(player, monster)
    
    def peaceful_exploration(self, player):
        """
        Handle peaceful exploration (no combat).
        
        Args:
            player: The player object
            
        Returns:
            str: Result of exploration ("peaceful")
        """
        events = self.get_peaceful_events()
        
        if events:
            event = random.choice(events)
            display.display_text(event, title="Peaceful Exploration")
        else:
            # Default peaceful event if none defined
            default_event = f"🌟 You explore the {self.get_location_name().lower()} peacefully, enjoying the scenery."
            display.display_text(default_event, title="Peaceful Exploration")
        
        return "peaceful"
    
    def ask_continue_adventure(self, player):
        """
        Ask the player if they want to continue adventuring.
        
        Args:
            player: The player object
            
        Returns:
            str: "continue" or "return"
        """
        options = [
            f"{self.get_location_emoji()} Continue exploring the {self.get_location_name().lower()}",
            "🏠 Return to the inn"
        ]
        
        status_text = f"Current Status: {player.emoji} {player.name} (Lvl {player.level}): {player.current_health}/{player.max_health} HP"
        
        # Show continue choice (HP already in header)
        choice = display.display_menu("Adventure Choice", options, status_text)
        
        if choice == "1":
            return "continue"
        else:
            return "return"
    
    def set_encounter_rate(self, rate):
        """
        Set the encounter rate for this location.
        
        Args:
            rate (float): Encounter rate between 0.0 and 1.0
        """
        self.encounter_rate = max(0.0, min(1.0, rate))
    
    
    # Class-level adventure management methods
    @classmethod
    def _load_adventures(cls):
        """
        Load all available adventure classes (lazy loading).
        
        Returns:
            dict: Dictionary of {adventure_key: adventure_class}
        """
        adventure_classes = {}
        
        try:
            # Use dynamic import to avoid circular imports
            from src.locations.forest import Forest
            adventure_classes['forest'] = Forest
            
            # Test creating an instance to ensure it works
            test_forest = Forest()
            location_name = test_forest.get_location_name()
            
        except ImportError as e:
            # Forest module not available
            pass
        except Exception as e:
            # Forest class has issues, skip it
            pass
        return adventure_classes
    
    @classmethod
    def get_available_adventures(cls, player=None):
        """
        Get list of available adventure locations for a player.
        
        Args:
            player: Player object (optional, if None returns all adventures)
        
        Returns:
            list: List of tuples (key, name, emoji)
        """
        adventure_classes = cls._load_adventures()
        available_adventures = []
        
        # Get player's unlocked areas
        if player:
            unlocked_areas = player.get_unlocked_areas()
        else:
            unlocked_areas = list(adventure_classes.keys())  # All areas if no player
        
        for key, adventure_class in adventure_classes.items():
            # Only include if player has unlocked this area
            if key in unlocked_areas:
                # Create temporary instance to get location info
                temp_adventure = adventure_class()
                location_name = temp_adventure.get_location_name()
                location_emoji = temp_adventure.get_location_emoji()
                
                available_adventures.append((
                    key,
                    location_name,
                    location_emoji
                ))
        
        return available_adventures
    
    @classmethod
    def show_adventure_selection_menu(cls, player):
        """
        Show adventure location selection menu.
        
        Args:
            player: The player object
            
        Returns:
            str: Result of adventure or "cancelled" if player backs out
        """
        
        available_adventures = cls.get_available_adventures(player)
        
        if not available_adventures:
            display.add_line("❌ No adventures are currently available!")
            return "cancelled"
        
        # Build menu options
        adventure_options = []
        for key, name, emoji in available_adventures:
            option_text = f"{emoji} {name}"
            adventure_options.append(option_text)

        
        adventure_options.append("🏠 Return to Inn")
        
        status_text = f"Choose your adventure destination:\n\n{player.emoji} {player.name} (Lvl {player.level}): {player.current_health}/{player.max_health} HP"
        
        choice = display.display_menu("🗺️ Adventure Destinations", adventure_options, status_text)
        
        if choice == "quit" or int(choice) == len(adventure_options):
            display.add_line("🏠 You decide to stay at the inn for now.")
            return "cancelled"
        
        # Start chosen adventure
        choice_index = int(choice) - 1
        adventure_key = available_adventures[choice_index][0]
        
        return cls.start_adventure_by_key(adventure_key, player)
    
    @classmethod
    def start_adventure_by_key(cls, adventure_key, player):
        """
        Start an adventure by its key identifier.
        
        Args:
            adventure_key (str): Key of the adventure ('forest', 'cave', etc.)
            player: The player object
            
        Returns:
            str: Result of the adventure ("victory", "defeat", "fled", "returned")
        """
        adventure_classes = cls._load_adventures()
        
        if adventure_key not in adventure_classes:
            raise ValueError(f"Adventure '{adventure_key}' not found")
        
        adventure_class = adventure_classes[adventure_key]
        adventure = adventure_class()
        
        # Start the adventure
        return adventure.start_adventure(player)