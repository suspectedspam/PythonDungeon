#!/usr/bin/env python3
"""
Monster classes for PythonDungeon
Contains monster definitions and basic monster functionality
"""

import random

class Monster:
    """Basic monster class with name, health, strength, and level attributes."""
    
    def __init__(self, name, max_health, strength, level=1, emoji="🐾"):
        """
        Initialize a monster.
        
        Args:
            name (str): Name of the monster
            max_health (int): Maximum health points
            strength (int): Strength attribute used for damage calculation
            level (int): Monster level (default: 1)
            emoji (str): Monster emoji representation (default: "🐾")
        """
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.strength = strength
        self.level = level
        self.is_alive = True
        self.emoji = emoji
    
    def update_health(self, new_health):
        """
        Update the monster's health (used by combat system).
        
        Args:
            new_health (int): New health value
        """
        self.current_health = max(0, new_health)
        self.is_alive = self.current_health > 0
    
    def get_health_status(self):
        """
        Get a description of the monster's current health status.
        
        Returns:
            str: Health status description
        """
        health_percent = (self.current_health / self.max_health) * 100
        
        if health_percent == 100:
            return "in perfect condition"
        elif health_percent >= 75:
            return "slightly wounded"
        elif health_percent >= 50:
            return "moderately wounded"
        elif health_percent >= 25:
            return "badly wounded"
        elif health_percent > 0:
            return "critically wounded"
        else:
            return "defeated"
    
    def display_status(self):
        """Display the monster's current status."""
        status = self.get_health_status()
        print(f"🐉 {self.name} (Lvl {self.level}): {self.current_health}/{self.max_health} HP ({status}) | Strength: {self.strength}")
    
    def display_stats(self):
        """Display the monster's full stats."""
        print(f"📊 {self.name} Stats:")
        print(f"   Level: {self.level}")
        print(f"   Health: {self.current_health}/{self.max_health}")
        print(f"   Strength: {self.strength}")
        print(f"   Status: {self.get_health_status()}")
    
    def __str__(self):
        """String representation of the monster."""
        return f"{self.name} Lvl {self.level} (HP: {self.current_health}/{self.max_health})"
    
    def __repr__(self):
        """Developer representation of the monster."""
        return f"Monster('{self.name}', {self.max_health}, {self.strength}, {self.level})"
    
    @classmethod
    def create_from_database(cls, monster_data, player_level):
        """
        Create a monster from database template data.
        
        Args:
            monster_data: Database row from monster_templates table
            player_level: Current player level for scaling
            
        Returns:
            Monster: A new monster instance
        """
        if not monster_data:
            # Fallback monster if database fails
            return cls("Wild Beast", 20, 3, 1, "🐾")
        
        # Extract data from database row
        # Row format: (id, name, min_level, max_level, base_health, base_strength, emoji, rarity, description)
        name = monster_data[1]
        base_health = monster_data[4]
        base_strength = monster_data[5]
        emoji = monster_data[6]
        
        # Scale stats based on player level
        level_scaling = max(0, player_level - 1)
        scaled_health = base_health + (level_scaling * 3)  # +3 HP per level above 1
        scaled_strength = base_strength + (level_scaling // 2)  # +1 strength every 2 levels
        
        return cls(name, scaled_health, scaled_strength, player_level, emoji)
    
    @classmethod 
    def create_random_for_level(cls, player_level):
        """
        Create a random monster appropriate for the player's level.
        
        Args:
            player_level: Current player level
            
        Returns:
            Monster: A random monster instance
        """
        from gamedata import game_db
        
        try:
            monster_data = game_db.get_random_monster(player_level)
            return cls.create_from_database(monster_data, player_level)
        except Exception as e:
            print(f"Database error: {e}")
            # Fallback to hardcoded monster
            return cls.create_fallback_monster(player_level)
    
    @classmethod
    def create_fallback_monster(cls, player_level):
        """Create a fallback monster if database fails."""
        if player_level <= 2:
            return cls("Goblin", 20 + (player_level * 5), 3 + player_level, player_level, "👹")
        elif player_level <= 4:
            return cls("Orc", 30 + (player_level * 6), 4 + player_level, player_level, "👺")
        else:
            return cls("Troll", 50 + (player_level * 8), 6 + player_level, player_level, "🧌")

# Database-driven monster creation is now handled by class methods above
# All monster data is stored in the SQLite database and loaded dynamically

# Example usage and testing
if __name__ == "__main__":
    # Import combat system for proper testing
    from combat import Combat
    
    print("=== Monster System Test ===")
    print()
    
    # Create combat system and a goblin
    combat = Combat()
    goblin = create_goblin()
    print(f"Created: {goblin}")
    goblin.display_status()
    print()
    
    # Test damage using combat system
    print("🗡️  Player attacks goblin!")
    damage_dealt = combat.calculate_damage(10)
    new_health, is_alive = combat.take_damage(goblin.current_health, damage_dealt)
    goblin.update_health(new_health)
    
    combat.display_damage_message("Player", goblin.name, damage_dealt)
    goblin.display_status()
    print()
    
    # Test goblin counter-attack using its strength
    if goblin.is_alive:
        print(f"🗡️  {goblin.name} counter-attacks!")
        monster_damage, is_critical = combat.calculate_critical_hit(goblin.strength)
        combat.display_damage_message(goblin.name, "Player", monster_damage, is_critical)
    print()
    
    # Test random monster creation with levels
    print("Creating random monsters:")
    for i in range(5):
        monster = create_random_monster(4)
        print(f"  {monster}")
    
    print()
    
    # Test area-based creation
    print("Monsters by area level:")
    area1_monster = create_monster_for_area(1)
    area3_monster = create_monster_for_area(3)
    area5_monster = create_monster_for_area(5)
    
    print(f"  Area 1: {area1_monster}")
    print(f"  Area 3: {area3_monster}")
    print(f"  Area 5: {area5_monster}")
    
    print()
    
    # Test new monster types
    print("New monster examples:")
    owlbear = create_owlbear(4)
    dire_rat = create_dire_rat(2)
    dark_elf = create_elf(3)
    plant = create_carnivorous_plant(2)
    
    owlbear.display_stats()
    print()
    dire_rat.display_stats()
    print()
    dark_elf.display_stats()
    print()
    plant.display_stats()