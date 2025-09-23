#!/usr/bin/env python3
"""
Combat system for PythonDungeon
Handles damage calculation and combat mechanics
"""

import random

class Combat:
    """Simple combat class for handling damage and basic combat mechanics."""
    
    def __init__(self):
        """Initialize combat system."""
        pass
    
    def calculate_damage(self, base_damage, min_damage=1, max_damage=None):
        """
        Calculate damage with some randomization.
        
        Args:
            base_damage (int): Base damage value
            min_damage (int): Minimum damage possible (default: 1)
            max_damage (int): Maximum damage possible (default: base_damage + 2)
            
        Returns:
            int: Calculated damage amount
        """
        if max_damage is None:
            max_damage = base_damage + 2
            
        # Add some randomness to damage
        damage = random.randint(min_damage, max(min_damage, base_damage))
        damage = min(damage, max_damage)
        
        return damage
    
    def take_damage(self, current_health, damage_amount):
        """
        Apply damage to current health.
        
        Args:
            current_health (int): Current health points
            damage_amount (int): Amount of damage to take
            
        Returns:
            tuple: (new_health, is_alive)
        """
        new_health = max(0, current_health - damage_amount)
        is_alive = new_health > 0
        
        return new_health, is_alive
    
    def calculate_critical_hit(self, base_damage, crit_chance=0.1, crit_multiplier=1.5):
        """
        Calculate if attack is a critical hit and return damage.
        
        Args:
            base_damage (int): Base damage before crit calculation
            crit_chance (float): Chance for critical hit (0.0-1.0, default: 0.1)
            crit_multiplier (float): Damage multiplier for crits (default: 1.5)
            
        Returns:
            tuple: (damage_amount, is_critical)
        """
        is_critical = random.random() < crit_chance
        
        if is_critical:
            damage = int(base_damage * crit_multiplier)
            return damage, True
        else:
            damage = self.calculate_damage(base_damage)
            return damage, False
    
    def display_damage_message(self, attacker, target, damage, is_critical=False):
        """
        Display damage message to console.
        
        Args:
            attacker (str): Name of the attacker
            target (str): Name of the target
            damage (int): Damage dealt
            is_critical (bool): Whether it was a critical hit
        """
        if is_critical:
            print(f"💥 CRITICAL HIT! {attacker} deals {damage} damage to {target}!")
        else:
            print(f"⚔️  {attacker} deals {damage} damage to {target}.")

# Example usage and testing
if __name__ == "__main__":
    combat = Combat()
    
    print("=== Combat System Test ===")
    print()
    
    # Test damage calculation
    base_dmg = 10
    calculated_dmg = combat.calculate_damage(base_dmg)
    print(f"Base damage: {base_dmg}, Calculated damage: {calculated_dmg}")
    
    # Test taking damage
    health = 50
    damage = 15
    new_health, alive = combat.take_damage(health, damage)
    print(f"Health: {health} -> {new_health}, Alive: {alive}")
    
    # Test critical hit
    crit_dmg, is_crit = combat.calculate_critical_hit(base_dmg)
    print(f"Attack damage: {crit_dmg}, Critical: {is_crit}")
    
    # Test damage message
    combat.display_damage_message("Player", "Goblin", crit_dmg, is_crit)