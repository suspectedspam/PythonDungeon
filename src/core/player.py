#!/usr/bin/env python3
"""
Player class for PythonDungeon
"""

from datetime import datetime
from src.core.gamedata import game_db
from src.ui.display import display

def display_status(self):
        
        """
        Calculate XP needed for next level.
        Uses formula: level * 100 (level 1->2 needs 100 XP, 2->3 needs 200 XP, etc.)
        
        Returns:
            int: Total XP needed to reach next level
        """
        return self.level * 100
    
def get_current_level_xp(self):
    """
    Calculate XP threshold for current level.
    
    Returns:
        int: Total XP needed to reach current level
    """
    return max(0, (self.level - 1) * 100)
    print(f"🏃 {self.name} (Lvl {self.level}): {self.current_health}/{self.max_health} HP | Strength: {self.strength} | {self.get_xp_display()}")
    
    def display_stats(self):
        """Display the player's full stats."""
        print(f"📊 {self.name} Stats:")
        creation_text = f"""
Greetings, {self.name}!
You are now ready to begin your adventure!

📊 {player.emoji} {player_name} Stats:
   Level: {player.level}
   Health: {player.current_health}/{player.max_health}
   Strength: {player.strength}
   {player.get_xp_display()}
   Status: {player.get_health_status()}

{player.emoji} {player.name} arrives at the inn, ready for adventure")
        print(f"   Health: {self.current_health}/{self.max_health}")
        print(f"   Strength: {self.strength}")
        print(f"   {self.get_xp_display()}")
        print(f"   Status: {self.get_health_status()}")
"""

class Player:
    """Basic player class with name, health, strength, and level attributes."""
    
    def __init__(self, name, max_health=50, strength=6, level=1, emoji="👤", experience=0):
        """
        Initialize a player.
        
        Args:
            name (str): Name of the player
            max_health (int): Maximum health points (default: 50)
            strength (int): Strength attribute used for damage calculation (default: 6)
            level (int): Player level (default: 1)
            emoji (str): Character emoji representation (default: "👤")
            experience (int): Current experience points (default: 0)
        """
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.strength = strength
        self.level = level
        self.experience = experience
        self.is_alive = True
        self.emoji = emoji
    
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
        print(f"🏃 {self.name} (Lvl {self.level}): {self.current_health}/{self.max_health} HP | Strength: {self.strength}")
    
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
    
    # Experience and Leveling System
    def get_xp_needed_for_level_up(self):
        """
        Calculate XP needed for current level to advance to next level.
        Scaling formula: level * 100 (level 1->2 needs 100, 2->3 needs 200, etc.)
        This prevents farming low areas and encourages progression to harder content.
        
        Returns:
            int: XP needed to level up from current level
        """
        return self.level * 100
    
    def get_current_level_progress(self):
        """
        Get XP progress within current level.
        
        Returns:
            tuple: (current_xp_in_level, xp_needed_to_level_up, percentage)
        """
        xp_needed = self.get_xp_needed_for_level_up()
        current_xp_in_level = self.experience  # With scaling, this is progress within current level
        percentage = (current_xp_in_level / xp_needed) * 100
        
        return current_xp_in_level, xp_needed, percentage
    
    def add_experience(self, xp_amount):
        """
        Add experience points and handle leveling up.
        
        Args:
            xp_amount (int): XP to add
            
        Returns:
            bool: True if player leveled up, False otherwise
        """
        if xp_amount <= 0:
            return False
            
        self.experience += xp_amount
        leveled_up = False
        
        # Check for level up with scaling XP requirements
        while self.experience >= self.get_xp_needed_for_level_up():
            xp_needed = self.get_xp_needed_for_level_up()
            self.experience -= xp_needed  # Subtract XP used for level up
            self.level_up()
            leveled_up = True
            
        return leveled_up
    
    def level_up(self):
        """
        Level up the player, increasing stats.
        """
        old_level = self.level
        self.level += 1
        
        # Stat increases per level
        health_increase = 10  # +10 max HP per level
        strength_increase = 2  # +2 strength per level
        
        # Apply stat increases
        old_max_health = self.max_health
        self.max_health += health_increase
        self.strength += strength_increase
        
        # Heal to full on level up (classic RPG mechanic)
        self.current_health = self.max_health
        self.is_alive = True
        
        # Display level up message  
        level_up_text = f"""🎉 LEVEL UP! 🎉

🌟 {self.name} reached Level {self.level}!
💪 Strength: {self.strength - strength_increase} → {self.strength}
❤️  Max Health: {old_max_health} → {self.max_health}
✨ Full health restored!"""
        
        display.display_text(level_up_text, title="Level Up!")
        
        # Auto-save on level up
        self.auto_save("level_up")
    
    def get_xp_display(self):
        """
        Get formatted XP display string for current level progress.
        
        Returns:
            str: Formatted XP display (e.g., "XP: 45/100 (45%)")
        """
        current_xp, xp_needed, percentage = self.get_current_level_progress()
        return f"XP: {current_xp}/{xp_needed} ({percentage:.0f}%)"

    def __str__(self):
        """String representation of the player."""
        return f"{self.name} Lvl {self.level} (HP: {self.current_health}/{self.max_health})"
    
    def __repr__(self):
        """Developer representation of the player."""
        return f"Player('{self.name}', {self.max_health}, {self.strength}, {self.level}, experience={self.experience})"
    
    # Database Integration Methods
    def save_to_database(self):
        """Save this player to the database."""
        try:
            game_db.save_player(self)
            return True
        except Exception as e:
            print(f"❌ Error saving player: {e}")
            return False
    
    def auto_save(self, context="general"):
        """
        Auto-save after important events with user feedback.
        
        Args:
            context (str): Context for the auto-save ("rest", "combat", "inn_visit")
        """
        # Check if auto-save is enabled for this context
        if not self.should_auto_save(context):
            return
            
        if self.save_to_database():
            display.add_line("💾 Game saved automatically", delay=0.3)
    
    def should_auto_save(self, context):
        """Check if auto-save should happen in this context."""
        try:
            settings = game_db.get_player_settings(self.name)
            
            if context == "rest":
                return settings['auto_save_after_rest']
            elif context == "combat":
                return settings['auto_save_after_combat']
            elif context == "inn_visit":
                return settings['auto_save_on_inn_visit']
            else:
                return True  # Default to auto-save for other contexts
        except:
            return True  # Default to auto-save if settings can't be loaded
    
    def get_settings(self):
        """Get player's current settings."""
        return game_db.get_player_settings(self.name)
    
    def update_settings(self, settings):
        """Update player's settings."""
        game_db.update_player_settings(self.name, settings)
    
    def get_unlocked_areas(self):
        """Get list of areas unlocked for this player."""
        return game_db.get_player_unlocked_areas(self.name)
    
    def unlock_area(self, area_key):
        """Unlock a new area for this player."""
        unlocked_areas = game_db.unlock_area_for_player(self.name, area_key)
        
        # Show unlock message if it's a new area
        current_unlocked = self.get_unlocked_areas()
        if area_key in unlocked_areas and len(unlocked_areas) > len(current_unlocked):
            display.add_line(f"🗝️ New area unlocked: {area_key.title()}!", delay=0.5)
        
        return unlocked_areas
    
    def manual_save(self):
        """Manual save with user feedback."""
        if self.save_to_database():
            display.add_line("✅ Game saved successfully!", delay=0.4)
        else:
            display.add_line("❌ Failed to save game", delay=0.4)
    
    @classmethod
    def load_from_database(cls, name):
        """
        Load a player from the database.
        
        Args:
            name (str): Name of the player to load
            
        Returns:
            Player or None: Player object if found, None otherwise
        """
        try:
            return game_db.load_player(name)
        except Exception as e:
            print(f"❌ Error loading player: {e}")
            return None
    
    @classmethod
    def get_all_saved_characters(cls):
        """
        Get list of all saved characters.
        
        Returns:
            list: List of tuples (name, level, emoji, last_played)
        """
        try:
            return game_db.get_all_saves()
        except Exception as e:
            print(f"❌ Error loading character list: {e}")
            return []
    
    @classmethod
    def load_or_create_character(cls):
        """
        Show character selection menu - load existing or create new.
        
        Returns:
            Player or None: Selected/created player, or None if cancelled
        """
        
        # Check for existing saves
        saved_characters = cls.get_all_saved_characters()
        
        if saved_characters:
            # Show load/create menu
            display.set_header("CHARACTER SELECTION")
            display.add_line("", delay=0.3)
            display.add_line("🎮 CHOOSE YOUR ADVENTURE", delay=0.6)
            display.add_line("-" * 25, delay=0.4)
            display.add_line("", delay=0.3)
            
            # Show saved characters
            display.add_line("📁 Saved Characters:", delay=0.4)
            for i, (name, level, emoji, last_played) in enumerate(saved_characters, 1):
                # Format last played date
                try:
                    last_date = datetime.fromisoformat(last_played).strftime("%m/%d %H:%M")
                except:
                    last_date = "Unknown"
                display.add_line(f"  {i}. {emoji} {name} (Lvl {level}) - {last_date}", delay=0.2)
            
            display.add_line("", delay=0.3)
            display.add_line("Options:", delay=0.4)
            display.add_line(f"  {len(saved_characters) + 1}. 🎭 Create New Character", delay=0.2)
            display.add_line(f"  {len(saved_characters) + 2}. ❌ Quit Game", delay=0.2)
            
            display.set_footer(f"Choose (1-{len(saved_characters) + 2}): ")
            display.refresh_display()
            
            while True:
                try:
                    choice = input().strip()
                    choice_num = int(choice)
                    
                    if 1 <= choice_num <= len(saved_characters):
                        # Load existing character
                        character_name = saved_characters[choice_num - 1][0]
                        player = cls.load_from_database(character_name)
                        if player:
                            display.add_line("", delay=0.3)
                            display.add_line(f"✅ Loaded {player.emoji} {player.name}!", delay=0.6)
                            display.add_line(f"Welcome back, {player.name}!", delay=0.4)
                            return player
                        else:
                            display.add_line("❌ Failed to load character. Try again.")
                            display.set_footer(f"Choose (1-{len(saved_characters) + 2}): ")
                            display.refresh_display()
                    
                    elif choice_num == len(saved_characters) + 1:
                        # Create new character
                        return cls.create_character()
                    
                    elif choice_num == len(saved_characters) + 2:
                        # Quit
                        return None
                    
                    else:
                        display.add_line("Please choose a valid option.")
                        display.set_footer(f"Choose (1-{len(saved_characters) + 2}): ")
                        display.refresh_display()
                
                except ValueError:
                    display.add_line("Please enter a number.")
                    display.set_footer(f"Choose (1-{len(saved_characters) + 2}): ")
                    display.refresh_display()
                except (EOFError, KeyboardInterrupt):
                    return None
        else:
            # No saved characters, create new one
            display.add_line("🎮 No saved characters found. Let's create your first character!", delay=0.6)
            return cls.create_character()
    
    @classmethod
    def create_character(cls):
        """Create a new player character with full creation process."""
        
        # Name selection
        display.set_header("CHARACTER CREATION")
        display.add_line("", delay=0.3)
        display.add_line("🎭 CHARACTER CREATION", delay=0.6)
        display.add_line("-" * 20, delay=0.4)
        display.add_line("", delay=0.3)
        display.add_line("What is your name, brave adventurer?", delay=0.6)
        
        # Set footer with input prompt and refresh display
        display.set_footer("Enter your name: ")
        display.refresh_display()
        
        # Get player's name
        while True:
            try:
                player_name = input().strip()
                if player_name:
                    break
                display.add_line("Please enter a valid name.")
                display.set_footer("Enter your name: ")
                display.refresh_display()
            except (EOFError, KeyboardInterrupt):
                print("\nGame interrupted.")
                return None
        
        # Clear footer after getting input
        display.set_footer("")
        
        # Get player's emoji choice
        player_emoji = cls._choose_character_emoji()
        if player_emoji is None:
            return None
        
        # Create player with chosen name and emoji
        player = cls(player_name, emoji=player_emoji)
        
        creation_text = f"""
Greetings, {player_name}!
You are now ready to begin your adventure!

📊 {player.emoji} {player_name} Stats:
   Level: {player.level}
   Health: {player.current_health}/{player.max_health}
   Strength: {player.strength}
   Status: {player.get_health_status()}

{player.emoji} {player.name} arrives at the inn, ready for adventure!"""
        
        # Regular text - line by line, appends to scroll
        display.display_text(creation_text, title="Character Created")
        
        # Auto-save new character
        player.save_to_database()
        display.add_line("💾 Character saved to database!", delay=0.4)
        
        return player

    @classmethod
    def _choose_character_emoji(cls):
        """Let the player choose an emoji for their character."""
        
        # Define emoji categories (10 lines of 10 emojis each)
        emoji_lines = [
            ["🧙", "🧚", "🧛", "🧜", "🧞", "🧝", "🧟", "👸", "🤴", "👑"],  # Fantasy
            ["⚔️", "🗡️", "🏹", "🛡️", "🪓", "🔨", "🏺", "⚱️", "🧿", "💎"],  # Weapons/Items
            ["🐉", "🦄", "🐺", "🦅", "🐯", "🦁", "🐻", "🦊", "🐸", "🦉"],  # Creatures
            ["🌟", "⭐", "✨", "💫", "🔥", "❄️", "⚡", "🌙", "☀️", "🌈"],  # Elements
            ["👤", "👥", "👁️", "🦾", "🦿", "🧠", "❤️", "💚", "💙", "💜"],  # Abstract
            ["🎭", "🎪", "🎨", "🎵", "🎯", "🎲", "🃏", "🎰", "🎊", "🎉"],  # Arts/Games
            ["👮", "👷", "👩‍⚕️", "👩‍🚒", "�‍✈️", "👩‍🔬", "👩‍💼", "👩‍�", "👩‍�", "👩‍�"],  # Professions
            ["📿", "🔮", "�", "🎩", "🧢", "�️", "🥷", "�‍⚖️", "⚗️", "🏴‍☠️"],  # Accessories/Special
            ["🍄", "🌺", "🌸", "🌼", "🌻", "🌷", "🌹", "💐", "🌱", "☘️"],  # Nature
            ["😊", "😎", "🤩", "😇", "🤔", "😤", "😈", "🤠", "🤖", "👻"]   # Faces
        ]
        
        line_descriptions = [
            "Fantasy Characters", "Weapons & Items", "Creatures & Beasts", "Elements & Magic",
            "Abstract Symbols", "Arts & Games", "Places & Landmarks", "Accessories & Tools",
            "Nature & Plants", "Faces & Expressions"
        ]
        
        while True:
            # Show all emoji lines
            display.set_header("CHOOSE YOUR CHARACTER ICON")
            display.add_line("Please choose your character's icon:", delay=0.4)
            
            for i, line in enumerate(emoji_lines, 1):
                emoji_display = " ".join(line)
                display.add_line(f"{i:2d}. {emoji_display}", delay=0.2)
            
            # Get line choice
            display.set_footer("Choose a line (1-10) or 'q' to quit: ")
            display.refresh_display()
            
            try:
                choice = input().strip().lower()
                if choice == 'q':
                    return None
                
                line_num = int(choice)
                if 1 <= line_num <= 10:
                    selected_emoji = cls._choose_from_emoji_line(emoji_lines[line_num - 1])
                    if selected_emoji:
                        return selected_emoji
                    # If they chose to go back, continue the main loop
                else:
                    display.add_line("Please choose a number between 1 and 10.")
            except ValueError:
                display.add_line("Please enter a valid number or 'q' to quit.")
            except (EOFError, KeyboardInterrupt):
                return None

    @classmethod
    def _choose_from_emoji_line(cls, emoji_line):
        """Let the player choose a specific emoji from a line."""
        
        while True:
            display.set_header("CHOOSE YOUR EMOJI")
            display.add_line("Choose your emoji:", delay=0.4)
            
            for i, emoji in enumerate(emoji_line, 1):
                display.add_line(f"{i:2d}. {emoji}", delay=0.2)
            
            # Get emoji choice
            display.set_footer("Choose emoji (1-10) or 'b' to go back: ")
            display.refresh_display()
            
            try:
                choice = input().strip().lower()
                if choice == 'b':
                    return None  # Go back to main emoji selection
                
                emoji_num = int(choice)
                if 1 <= emoji_num <= 10:
                    chosen_emoji = emoji_line[emoji_num - 1]
                    
                    # Confirm choice
                    display.add_line("", delay=0.3)
                    display.add_line(f"You chose: {chosen_emoji}", delay=0.6)
                    display.set_footer("Confirm this emoji? (y/n): ")
                    display.refresh_display()
                    
                    confirm = input().strip().lower()
                    if confirm in ['y', 'yes']:
                        return chosen_emoji
                    # If not confirmed, continue the loop to choose again
                else:
                    display.add_line("Please choose a number between 1 and 10.")
            except ValueError:
                display.add_line("Please enter a valid number or 'b' to go back.")
            except (EOFError, KeyboardInterrupt):
                return None