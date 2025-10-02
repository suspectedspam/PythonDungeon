#!/usr/bin/env python3
"""
Debug Menu System for PythonDungeon
Provides developer tools for testing and debugging gameplay mechanics.
This file can be easily removed for production builds.
"""

from src.ui.display import display

class DebugMenu:
    """Debug menu system for developer testing and gameplay manipulation."""
    
    def __init__(self):
        """Initialize the debug menu system."""
        self.active = True
        self.debug_delay = 0.05  # Fast delay for all debug menu interactions
    
    def show_debug_menu(self, player):
        """
        Display the main debug menu and handle user choices.
        
        Args:
            player: The player object to debug/modify
            
        Returns:
            str: Result of debug menu interaction ("continue", "quit")
        """
        while True:
            debug_options = [
                "⬆️ Add Level",
                "⬇️ Remove Level", 
                "✨ Add XP",
                "💔 Remove XP",
                "❤️ Set Health",
                "💪 Set Strength",
                "🎮 Toggle Debug Mode",
                "🔙 Back to Inn"
            ]
            
            # Show current player stats for reference
            status_text = f"""🐛 DEBUG MENU - Developer Tools
            
Current Player Stats:
👤 {player.emoji} {player.name}
📊 Level: {player.level}
✨ XP: {player.experience} / {player.get_xp_needed_for_level_up()}
❤️  Health: {player.current_health} / {player.max_health}
💪 Strength: {player.strength}
🐛 Debug Mode: {'ON' if display.debug_mode else 'OFF'}

⚠️  Warning: These tools modify game state for testing purposes."""
            
            choice = display.display_menu("🐛 Debug Console", debug_options, status_text, exposition_intro=False)
            
            if choice == "quit" or choice == "8":
                return "continue"  # Return to inn
                
            elif choice == "1":  # Add Level
                self._add_level(player)
                
            elif choice == "2":  # Remove Level
                self._remove_level(player)
                
            elif choice == "3":  # Add XP
                self._add_xp(player)
                
            elif choice == "4":  # Remove XP
                self._remove_xp(player)
                
            elif choice == "5":  # Set Health
                self._set_health(player)
                
            elif choice == "6":  # Set Strength
                self._set_strength(player)
                
            elif choice == "7":  # Toggle Debug Mode
                self._toggle_debug_mode()
                
            else:
                display.add_line("❌ Invalid choice. Please select 1-8.", delay=self.debug_delay)
    
    def _add_level(self, player):
        """Add levels to the player."""
        display.add_line("", delay=self.debug_delay)
        display.add_line("⬆️ ADD LEVEL", delay=self.debug_delay)
        display.add_line("How many levels to add? (1-10):", delay=self.debug_delay)
        display.set_footer("Enter number of levels: ")
        display.refresh_display()
        
        try:
            levels = input().strip()
            levels_to_add = int(levels)
            
            if 1 <= levels_to_add <= 10:
                old_level = player.level
                for _ in range(levels_to_add):
                    player.level_up()
                
                display.add_line(f"✅ Added {levels_to_add} level(s)!", delay=self.debug_delay)
                display.add_line(f"📊 {old_level} → {player.level}", delay=self.debug_delay)
                display.add_line(f"💪 Strength: {player.strength}", delay=self.debug_delay)
                display.add_line(f"❤️  Health: {player.current_health}/{player.max_health}", delay=self.debug_delay)
            else:
                display.add_line("❌ Please enter a number between 1 and 10.", delay=self.debug_delay)
                
        except ValueError:
            display.add_line("❌ Invalid input. Please enter a number.", delay=self.debug_delay)
        except (EOFError, KeyboardInterrupt):
            display.add_line("🚫 Operation cancelled.", delay=self.debug_delay)
        
        display.set_footer("")
    
    def _remove_level(self, player):
        """Remove levels from the player."""
        if player.level <= 1:
            display.add_line("❌ Cannot go below level 1!", delay=self.debug_delay)
            return
            
        display.add_line("", delay=self.debug_delay)
        display.add_line("⬇️ REMOVE LEVEL", delay=self.debug_delay)
        max_removable = player.level - 1
        display.add_line(f"How many levels to remove? (1-{max_removable}):", delay=self.debug_delay)
        display.set_footer("Enter number of levels: ")
        display.refresh_display()
        
        try:
            levels = input().strip()
            levels_to_remove = int(levels)
            
            if 1 <= levels_to_remove <= max_removable:
                old_level = player.level
                # Decrease level and stats
                player.level -= levels_to_remove
                # Recalculate stats based on new level
                player.max_health = 50 + (player.level - 1) * 10  # Base + level increases
                player.strength = 6 + (player.level - 1) * 2     # Base + level increases
                player.current_health = min(player.current_health, player.max_health)
                
                display.add_line(f"✅ Removed {levels_to_remove} level(s)!", delay=self.debug_delay)
                display.add_line(f"📊 {old_level} → {player.level}", delay=self.debug_delay)
                display.add_line(f"💪 Strength: {player.strength}", delay=self.debug_delay)
                display.add_line(f"❤️  Health: {player.current_health}/{player.max_health}", delay=self.debug_delay)
            else:
                display.add_line(f"❌ Please enter a number between 1 and {max_removable}.", delay=self.debug_delay)
                
        except ValueError:
            display.add_line("❌ Invalid input. Please enter a number.", delay=self.debug_delay)
        except (EOFError, KeyboardInterrupt):
            display.add_line("🚫 Operation cancelled.", delay=self.debug_delay)
        
        display.set_footer("")
    
    def _add_xp(self, player):
        """Add experience points to the player."""
        display.add_line("", delay=self.debug_delay)
        display.add_line("✨ ADD EXPERIENCE", delay=self.debug_delay)
        xp_needed = player.get_xp_needed_for_level_up() - player.experience
        display.add_line(f"Current XP: {player.experience}/{player.get_xp_needed_for_level_up()}", delay=self.debug_delay)
        display.add_line(f"XP needed for next level: {xp_needed}", delay=self.debug_delay)
        display.add_line("How much XP to add? (1-1000):", delay=self.debug_delay)
        display.set_footer("Enter XP amount: ")
        display.refresh_display()
        
        try:
            xp_input = input().strip()
            xp_to_add = int(xp_input)
            
            if 1 <= xp_to_add <= 1000:
                old_xp = player.experience
                old_level = player.level
                
                # Add XP and check for level ups
                leveled_up = player.add_experience(xp_to_add)
                
                display.add_line(f"✅ Added {xp_to_add} XP!", delay=self.debug_delay)
                display.add_line(f"✨ {old_xp} → {player.experience} XP", delay=self.debug_delay)
                
                if leveled_up:
                    display.add_line(f"🎉 LEVEL UP! {old_level} → {player.level}", delay=self.debug_delay)
                    display.add_line(f"💪 Strength: {player.strength}", delay=self.debug_delay)
                    display.add_line(f"❤️  Health: {player.current_health}/{player.max_health}", delay=self.debug_delay)
                else:
                    xp_needed = player.get_xp_needed_for_level_up() - player.experience
                    display.add_line(f"📊 Need {xp_needed} more XP for level {player.level + 1}", delay=self.debug_delay)
            else:
                display.add_line("❌ Please enter a number between 1 and 1000.", delay=self.debug_delay)
                
        except ValueError:
            display.add_line("❌ Invalid input. Please enter a number.", delay=self.debug_delay)
        except (EOFError, KeyboardInterrupt):
            display.add_line("🚫 Operation cancelled.", delay=self.debug_delay)
        
        display.set_footer("")
    
    def _remove_xp(self, player):
        """Remove experience points from the player."""
        if player.experience <= 0:
            display.add_line("❌ No XP to remove!", delay=self.debug_delay)
            return
            
        display.add_line("", delay=self.debug_delay)
        display.add_line("💔 REMOVE EXPERIENCE", delay=self.debug_delay)
        display.add_line(f"Current XP: {player.experience}", delay=self.debug_delay)
        max_removable = player.experience
        display.add_line(f"How much XP to remove? (1-{max_removable}):", delay=self.debug_delay)
        display.set_footer("Enter XP amount: ")
        display.refresh_display()
        
        try:
            xp_input = input().strip()
            xp_to_remove = int(xp_input)
            
            if 1 <= xp_to_remove <= max_removable:
                old_xp = player.experience
                player.experience = max(0, player.experience - xp_to_remove)
                
                display.add_line(f"✅ Removed {xp_to_remove} XP!", delay=self.debug_delay)
                display.add_line(f"💔 {old_xp} → {player.experience} XP", delay=self.debug_delay)
                
                xp_needed = player.get_xp_needed_for_level_up() - player.experience
                display.add_line(f"📊 Need {xp_needed} more XP for level {player.level + 1}", delay=self.debug_delay)
            else:
                display.add_line(f"❌ Please enter a number between 1 and {max_removable}.", delay=self.debug_delay)
                
        except ValueError:
            display.add_line("❌ Invalid input. Please enter a number.", delay=self.debug_delay)
        except (EOFError, KeyboardInterrupt):
            display.add_line("🚫 Operation cancelled.", delay=self.debug_delay)
        
        display.set_footer("")
    
    def _set_health(self, player):
        """Set player health directly."""
        display.add_line("", delay=self.debug_delay)
        display.add_line("❤️ SET HEALTH", delay=self.debug_delay)
        display.add_line(f"Current Health: {player.current_health}/{player.max_health}", delay=self.debug_delay)
        display.add_line(f"Set health to? (1-{player.max_health}):", delay=self.debug_delay)
        display.set_footer("Enter health amount: ")
        display.refresh_display()
        
        try:
            health_input = input().strip()
            new_health = int(health_input)
            
            if 1 <= new_health <= player.max_health:
                old_health = player.current_health
                player.current_health = new_health
                player.is_alive = new_health > 0
                
                display.add_line(f"✅ Health set!", delay=self.debug_delay)
                display.add_line(f"❤️  {old_health} → {player.current_health}", delay=self.debug_delay)
            else:
                display.add_line(f"❌ Please enter a number between 1 and {player.max_health}.", delay=self.debug_delay)
                
        except ValueError:
            display.add_line("❌ Invalid input. Please enter a number.", delay=self.debug_delay)
        except (EOFError, KeyboardInterrupt):
            display.add_line("🚫 Operation cancelled.", delay=self.debug_delay)
        
        display.set_footer("")
    
    def _set_strength(self, player):
        """Set player strength directly."""
        display.add_line("", delay=self.debug_delay)
        display.add_line("💪 SET STRENGTH", delay=self.debug_delay)
        display.add_line(f"Current Strength: {player.strength}", delay=self.debug_delay)
        display.add_line("Set strength to? (1-50):", delay=self.debug_delay)
        display.set_footer("Enter strength amount: ")
        display.refresh_display()
        
        try:
            strength_input = input().strip()
            new_strength = int(strength_input)
            
            if 1 <= new_strength <= 50:
                old_strength = player.strength
                player.strength = new_strength
                
                display.add_line(f"✅ Strength set!", delay=self.debug_delay)
                display.add_line(f"💪 {old_strength} → {player.strength}", delay=self.debug_delay)
            else:
                display.add_line("❌ Please enter a number between 1 and 50.", delay=self.debug_delay)
                
        except ValueError:
            display.add_line("❌ Invalid input. Please enter a number.", delay=self.debug_delay)
        except (EOFError, KeyboardInterrupt):
            display.add_line("🚫 Operation cancelled.", delay=self.debug_delay)
        
        display.set_footer("")
    
    def _toggle_debug_mode(self):
        """Toggle debug mode on/off."""
        display.debug_mode = not display.debug_mode
        
        display.add_line("", delay=self.debug_delay)
        if display.debug_mode:
            display.add_line("🐛 DEBUG MODE: ON", delay=self.debug_delay)
            display.add_line("⚡ Ultra-fast text scrolling enabled (0.05s delays)", delay=self.debug_delay)
            display.add_line("🎯 Perfect for testing XP, combat, and story content", delay=self.debug_delay)
        else:
            display.add_line("🐛 DEBUG MODE: OFF", delay=self.debug_delay)
            display.add_line("📖 Normal text scrolling restored (0.3s delays)", delay=self.debug_delay)
            display.add_line("🎮 Regular gameplay experience", delay=self.debug_delay)

# Global debug menu instance
debug_menu = DebugMenu()
