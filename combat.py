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
    
    def run_combat(self, player, monster):
        """
        Handle full combat between player and monster.
        
        Args:
            player: The player object
            monster: The monster object
            
        Returns:
            str: Result of combat ("victory" or "defeat")
        """
        print("\n⚔️  COMBAT BEGINS! ⚔️")
        print("-" * 30)
        
        while player.is_alive and monster.is_alive:
            # Player attacks first
            player_damage, is_crit = self.calculate_critical_hit(player.strength)
            new_health, monster_alive = self.take_damage(monster.current_health, player_damage)
            monster.update_health(new_health)
            
            self.display_damage_message(player.name, monster.name, player_damage, is_crit)
            monster.display_status()
            
            if not monster.is_alive:
                print(f"\n🎉 Victory! You defeated the {monster.name}!")
                print(f"💰 You gain experience from this battle!")
                return "victory"
            
            print()
            
            # Monster counter-attacks
            monster_damage, is_crit = self.calculate_critical_hit(monster.strength)
            new_health, player_alive = self.take_damage(player.current_health, monster_damage)
            player.update_health(new_health)
            
            self.display_damage_message(monster.name, player.name, monster_damage, is_crit)
            player.display_status()
            
            if not player.is_alive:
                print(f"\n💀 Defeat! The {monster.name} has bested you!")
                print("🏠 You awaken back at the inn, wounded but alive...")
                player.current_health = 1  # Player survives but barely
                player.is_alive = True
                return "defeat"
            
            print("\n" + "-" * 20)
            input("Press Enter to continue the battle...")
        
        return "victory" if not monster.is_alive else "defeat"

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