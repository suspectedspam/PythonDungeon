#!/usr/bin/env python3
"""
Player class for PythonDungeon
Contains player character functionality and stats
"""

class Player:
    """Basic player class with name, health, strength, and level attributes."""
    
    def __init__(self, name, max_health=50, strength=6, level=1):
        """
        Initialize a player.
        
        Args:
            name (str): Name of the player
            max_health (int): Maximum health points (default: 50)
            strength (int): Strength attribute used for damage calculation (default: 6)
            level (int): Player level (default: 1)
        """
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.strength = strength
        self.level = level
        self.is_alive = True
    
    def update_health(self, new_health):
        """
        Update the player's health (used by combat system).
        
        Args:
            new_health (int): New health value
        """
        self.current_health = max(0, new_health)
        self.is_alive = self.current_health > 0
    
    def get_health_status(self):
        """
        Get a description of the player's current health status.
        
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
        """Display the player's current status."""
        status = self.get_health_status()
        print(f"🏃 {self.name} (Lvl {self.level}): {self.current_health}/{self.max_health} HP ({status}) | Strength: {self.strength}")
    
    def display_stats(self):
        """Display the player's full stats."""
        print(f"📊 {self.name} Stats:")
        print(f"   Level: {self.level}")
        print(f"   Health: {self.current_health}/{self.max_health}")
        print(f"   Strength: {self.strength}")
        print(f"   Status: {self.get_health_status()}")
    
    def heal(self, amount):
        """
        Heal the player by a specific amount.
        
        Args:
            amount (int): Amount of health to restore
            
        Returns:
            int: Actual amount healed
        """
        old_health = self.current_health
        self.current_health = min(self.max_health, self.current_health + amount)
        self.is_alive = self.current_health > 0
        actual_healed = self.current_health - old_health
        return actual_healed
    
    def rest(self):
        """Fully restore the player's health (like resting at an inn)."""
        old_health = self.current_health
        self.current_health = self.max_health
        self.is_alive = True
        return self.max_health - old_health
    
    def __str__(self):
        """String representation of the player."""
        return f"{self.name} Lvl {self.level} (HP: {self.current_health}/{self.max_health})"
    
    def __repr__(self):
        """Developer representation of the player."""
        return f"Player('{self.name}', {self.max_health}, {self.strength}, {self.level})"

# Helper function to create a new player
def create_player(name, character_class="Adventurer"):
    """
    Create a new player with default or class-based stats.
    
    Args:
        name (str): Player's name
        character_class (str): Character class (for future expansion)
        
    Returns:
        Player: A new player instance
    """
    # Basic adventurer stats for now
    # In the future, this could vary by character class
    return Player(name, max_health=50, strength=6, level=1)

# Example usage and testing
if __name__ == "__main__":
    print("=== Player System Test ===")
    print()
    
    # Create a player
    player = create_player("Hero")
    print(f"Created: {player}")
    player.display_stats()
    print()
    
    # Test taking damage using combat system
    from combat import Combat
    combat = Combat()
    
    print("🗡️  Player takes damage in combat!")
    damage_dealt = combat.calculate_damage(15)
    new_health, is_alive = combat.take_damage(player.current_health, damage_dealt)
    player.update_health(new_health)
    
    print(f"Player took {damage_dealt} damage!")
    player.display_status()
    print()
    
    # Test healing
    print("💚 Player uses a healing potion!")
    healed = player.heal(20)
    print(f"Player healed for {healed} HP!")
    player.display_status()
    print()
    
    # Test resting
    print("😴 Player rests to recover fully!")
    restored = player.rest()
    print(f"Player restored {restored} HP!")
    player.display_status()