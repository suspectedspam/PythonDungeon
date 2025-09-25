#!/usr/bin/env python3
"""
Combat system for PythonDungeon with scrolling display
Handles turn-based combat with visual feedback
"""

import random
import time
from display import display

class Combat:
    """Manages combat encounters with scrolling text display."""
    
    def __init__(self):
        """Initialize the combat system."""
        pass
    
    def calculate_damage(self, base_damage):
        """
        Calculate actual damage with some randomness.
        
        Args:
            base_damage (int): Base damage amount
            
        Returns:
            int: Calculated damage (80-120% of base)
        """
        # Add some randomness: 80% to 120% of base damage
        min_damage = max(1, int(base_damage * 0.8))
        max_damage = int(base_damage * 1.2)
        return random.randint(min_damage, max_damage)
    
    def take_damage(self, current_health, damage):
        """
        Apply damage to a character's health.
        
        Args:
            current_health (int): Current health points
            damage (int): Damage to apply
            
        Returns:
            tuple: (new_health, is_alive)
        """
        new_health = max(0, current_health - damage)
        is_alive = new_health > 0
        return new_health, is_alive
    
    def attempt_flee(self, success_chance=0.7):
        """
        Attempt to flee from combat.
        
        Args:
            success_chance (float): Probability of successful escape (0.0-1.0)
            
        Returns:
            str: "fled" if successful, "failed" if unsuccessful
        """
        if random.random() < success_chance:
            return "fled"
        return "failed"
    
    def calculate_critical_hit(self, base_damage, crit_chance=0.1, crit_multiplier=1.5):
        """
        Calculate damage with critical hit chance.
        
        Args:
            base_damage (int): Base damage amount
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
    
    def check_health_threshold(self, monster, crossed_thresholds):
        """
        Check if monster has crossed health thresholds and display appropriate message.
        
        Args:
            monster: The monster object
            crossed_thresholds: Set of thresholds already crossed
            
        Returns:
            str: Threshold message to display, or None if no new threshold crossed
        """
        health_percent = (monster.current_health / monster.max_health) * 100
        
        # Define thresholds and messages (from high to low)
        thresholds = [
            (75, "🩸 The monster staggers slightly!"),
            (50, f"💔 The {monster.name} looks wounded!"),
            (25, f"⚠️ The {monster.name} appears badly injured!"),
            (10, f"💀 The {monster.name} is near death!")
        ]
        
        for threshold, message in thresholds:
            if health_percent <= threshold and threshold not in crossed_thresholds:
                crossed_thresholds.add(threshold)
                return message
        
        return None

    def check_player_health_threshold(self, player, crossed_thresholds):
        """
        Check if player has crossed health thresholds and display appropriate message.
        
        Args:
            player: The player object
            crossed_thresholds: Set of thresholds already crossed
            
        Returns:
            str: Threshold message to display, or None if no new threshold crossed
        """
        health_percent = (player.current_health / player.max_health) * 100
        
        # Define thresholds and messages (from high to low)
        thresholds = [
            (50, f"💔 {player.emoji} You're feeling the strain of battle!"),
            (25, f"⚠️ {player.emoji} You're badly hurt and struggling to continue!")
        ]
        
        for threshold, message in thresholds:
            if health_percent <= threshold and threshold not in crossed_thresholds:
                crossed_thresholds.add(threshold)
                return message
        
        return None

    def run_combat(self, player, monster):
        """
        Handle full combat between player and monster with scrolling display.
        
        Args:
            player: The player object
            monster: The monster object
            
        Returns:
            str: Result of combat ("victory", "defeat", or "fled")
        """
        # Track which health thresholds have been crossed
        monster_crossed_thresholds = set()
        player_crossed_thresholds = set()
        
        # Initialize combat display by appending to scroll
        display.set_header("COMBAT INITIATED")
        
        display.add_line("", delay=0.3)
        display.add_line("⚔️  COMBAT BEGINS! ⚔️", delay=0.8)
        display.add_line("Get ready for battle!", delay=0.8)
        display.add_line("The clash of steel and magic is about to commence!", delay=0.6)
        display.add_line("", delay=0)
        
        while player.is_alive and monster.is_alive:
            # Show combat status in scrolling window
            display.display_combat_round(player, monster)
            
            # Player's turn - show options in footer and get choice
            choice = display.display_combat_options()
            
            if choice == "quit":
                return "fled"
            
            # Handle player action and add to scroll
            if choice == "1":  # Attack
                player_damage, is_crit = self.calculate_critical_hit(player.strength)
                new_health, monster_alive = self.take_damage(monster.current_health, player_damage)
                monster.update_health(new_health)
                
                # Add attack result with delays between each line
                display.add_line("", delay=0.3)
                
                if is_crit:
                    display.add_line(f"💥 CRITICAL HIT! {player.emoji} {player.name} deals {player_damage} damage!", delay=0.8)
                else:
                    display.add_line(f"⚔️ {player.emoji} {player.name} deals {player_damage} damage to {monster.name}.", delay=0.8)
                
                # Check for health threshold messages
                if monster.is_alive:  # Only check thresholds if monster is still alive
                    threshold_message = self.check_health_threshold(monster, monster_crossed_thresholds)
                    if threshold_message:
                        display.add_line(threshold_message, delay=0.6)
                
                if not monster.is_alive:
                    display.add_line("", delay=0.4)
                    display.add_line(f"🎉 Victory! You defeated the {monster.name}!", delay=0.6)
                    display.add_line("💰 You gain experience from this battle!", delay=0)
                    display.set_footer("Press Enter to continue...")
                    display.refresh_display()
                    try:
                        input()
                    except (EOFError, KeyboardInterrupt):
                        pass
                    # Clear enemy from header after battle
                    display.set_monster_for_header(None)
                    return "victory"
                    
            elif choice == "2":  # Heal
                if player.current_health == player.max_health:
                    display.add_line("", delay=0.3)
                    display.add_line(f"💚 {player.emoji} {player.name} is already at full health!", delay=0)
                else:
                    heal_amount = random.randint(10, 15)
                    actual_healed = player.heal(heal_amount)
                    display.add_line("", delay=0.3)
                    display.add_line(f"💚 {player.emoji} {player.name} heals for {actual_healed} HP!", delay=0.8)
                    
            elif choice == "3":  # Flee
                flee_result = self.attempt_flee()
                display.add_line("", delay=0.3)
                if flee_result == "fled":
                    display.add_line("🏃 You successfully escape from combat!", delay=0.8)
                    display.add_line("🌲 You make it back to the inn safely.", delay=0)
                    display.set_footer("Press Enter to continue...")
                    display.refresh_display()
                    try:
                        input()
                    except (EOFError, KeyboardInterrupt):
                        pass
                    # Clear enemy from header after fleeing
                    display.set_monster_for_header(None)
                    return "fled"
                else:
                    display.add_line("❌ You couldn't escape! You must fight!", delay=0)
            
            # Check if monster is still alive before counter-attack
            if not monster.is_alive:
                continue
                
            # Monster counter-attacks
            monster_damage, is_crit = self.calculate_critical_hit(monster.strength)
            new_health, player_alive = self.take_damage(player.current_health, monster_damage)
            player.update_health(new_health)
            
            display.add_line("", delay=0.3)
            display.add_line(f"🐉 {monster.name} attacks!", delay=0.8)
            
            if is_crit:
                display.add_line(f"💥 CRITICAL HIT! {monster.name} deals {monster_damage} damage!", delay=0.8)
            else:
                display.add_line(f"⚔️ {monster.name} deals {monster_damage} damage to {player.name}.", delay=0.8)
            
            # Check for player health threshold messages
            if player.is_alive:  # Only check thresholds if player is still alive
                player_threshold_message = self.check_player_health_threshold(player, player_crossed_thresholds)
                if player_threshold_message:
                    display.add_line(player_threshold_message, delay=0.6)
            
            if not player.is_alive:
                display.add_line("", delay=0.4)
                display.add_line(f"💀 Defeat! The {monster.name} has bested you!", delay=0.6)
                display.add_line("🏠 You awaken back at the inn, wounded but alive...", delay=0)
                
                player.current_health = 1  # Player survives but barely
                player.is_alive = True
                
                display.set_footer("Press Enter to continue...")
                display.refresh_display()
                try:
                    input()
                except (EOFError, KeyboardInterrupt):
                    pass
                # Clear enemy from header after defeat
                display.set_monster_for_header(None)
                return "defeat"
            
            # Small pause between turns to let player read
            time.sleep(1)
        
        # Clear enemy from header after combat loop ends
        display.set_monster_for_header(None)
        return "victory" if not monster.is_alive else "defeat"

# Global combat instance
combat_system = Combat()