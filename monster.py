#!/usr/bin/env python3
"""
Monster classes for PythonDungeon
Contains monster definitions and basic monster functionality
"""

import random

class Monster:
    """Basic monster class with name, health, strength, and level attributes."""
    
    def __init__(self, name, max_health, strength, level=1):
        """
        Initialize a monster.
        
        Args:
            name (str): Name of the monster
            max_health (int): Maximum health points
            strength (int): Strength attribute used for damage calculation
            level (int): Monster level (default: 1)
        """
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.strength = strength
        self.level = level
        self.is_alive = True
    
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

# Predefined monster types
def create_goblin(level=1):
    """Create a goblin monster with optional level scaling."""
    base_health = 25
    base_strength = 4
    return Monster("Goblin", base_health + (level - 1) * 5, base_strength + (level - 1), level)

def create_orc(level=2):
    """Create an orc monster with optional level scaling."""
    base_health = 40
    base_strength = 6
    return Monster("Orc", base_health + (level - 2) * 8, base_strength + (level - 2), level)

def create_skeleton(level=1):
    """Create a skeleton monster with optional level scaling."""
    base_health = 20
    base_strength = 5
    return Monster("Skeleton", base_health + (level - 1) * 4, base_strength + (level - 1), level)

def create_troll(level=3):
    """Create a troll monster with optional level scaling."""
    base_health = 60
    base_strength = 8
    return Monster("Troll", base_health + (level - 3) * 12, base_strength + (level - 3) * 2, level)

def create_human(level=2):
    """Create a human monster with optional level scaling."""
    base_health = 35
    base_strength = 5
    return Monster("Human Bandit", base_health + (level - 2) * 7, base_strength + (level - 2), level)

def create_elf(level=2):
    """Create an elf monster with optional level scaling."""
    base_health = 28
    base_strength = 6
    return Monster("Elf Fighter", base_health + (level - 2) * 5, base_strength + (level - 2), level)

def create_carnivorous_plant(level=1):
    """Create a carnivorous plant monster with optional level scaling."""
    base_health = 30
    base_strength = 4
    return Monster("Carnivorous Plant", base_health + (level - 1) * 8, base_strength + (level - 1), level)

def create_dire_bat(level=2):
    """Create a dire bat monster with optional level scaling."""
    base_health = 22
    base_strength = 7
    return Monster("Dire Bat", base_health + (level - 2) * 4, base_strength + (level - 2), level)

def create_dire_rat(level=1):
    """Create a dire rat monster with optional level scaling."""
    base_health = 18
    base_strength = 3
    return Monster("Dire Rat", base_health + (level - 1) * 3, base_strength + (level - 1), level)

def create_owlbear(level=4):
    """Create an owlbear monster with optional level scaling."""
    base_health = 75
    base_strength = 10
    return Monster("Owlbear", base_health + (level - 4) * 15, base_strength + (level - 4) * 2, level)

def create_dwarf(level=2):
    """Create a dwarf monster with optional level scaling."""
    base_health = 45
    base_strength = 7
    return Monster("Dwarf Warrior", base_health + (level - 2) * 10, base_strength + (level - 2), level)

def create_random_monster(max_level=3):
    """
    Create a random monster with appropriate level.
    
    Args:
        max_level (int): Maximum level for the monster
        
    Returns:
        Monster: A random monster with random level up to max_level
    """
    level = random.randint(1, max_level)
    monster_types = ["goblin", "orc", "skeleton", "troll", "human", "elf", 
                     "carnivorous_plant", "dire_bat", "dire_rat", "owlbear", "dwarf"]
    monster_type = random.choice(monster_types)
    
    monster_creators = {
        "goblin": create_goblin,
        "orc": create_orc,
        "skeleton": create_skeleton,
        "troll": create_troll,
        "human": create_human,
        "elf": create_elf,
        "carnivorous_plant": create_carnivorous_plant,
        "dire_bat": create_dire_bat,
        "dire_rat": create_dire_rat,
        "owlbear": create_owlbear,
        "dwarf": create_dwarf
    }
    
    return monster_creators[monster_type](level)

def create_monster_for_area(area_level):
    """
    Create a monster appropriate for a specific area level.
    
    Args:
        area_level (int): The level/difficulty of the current area
        
    Returns:
        Monster: A monster with level appropriate for the area
    """
    # Create monsters with levels around the area level (±1)
    monster_level = random.randint(max(1, area_level - 1), area_level + 1)
    
    monster_creators = {
        "goblin": create_goblin,
        "orc": create_orc,
        "skeleton": create_skeleton,
        "troll": create_troll,
        "human": create_human,
        "elf": create_elf,
        "carnivorous_plant": create_carnivorous_plant,
        "dire_bat": create_dire_bat,
        "dire_rat": create_dire_rat,
        "owlbear": create_owlbear,
        "dwarf": create_dwarf
    }
    
    if area_level <= 1:
        # Very low level areas: weak creatures
        monster_type = random.choice(["dire_rat", "goblin", "carnivorous_plant"])
    elif area_level <= 2:
        # Low level areas: basic monsters
        monster_type = random.choice(["goblin", "skeleton", "dire_rat", "dire_bat", "human"])
    elif area_level <= 3:
        # Mid level areas: more variety
        monster_type = random.choice(["goblin", "skeleton", "orc", "human", "elf", "dire_bat", "carnivorous_plant"])
    elif area_level <= 4:
        # Higher level areas: stronger creatures
        monster_type = random.choice(["orc", "human", "elf", "dwarf", "troll", "dire_bat"])
    else:
        # High level areas: dangerous monsters
        monster_type = random.choice(["troll", "owlbear", "dwarf", "elf", "orc"])
    
    return monster_creators[monster_type](monster_level)

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