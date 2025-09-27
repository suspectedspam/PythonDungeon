#!/usr/bin/env python3
"""
Advanced Display utilities for PythonDungeon
Handles scrolling text window with static header/footer
"""

import os
import sys
import time

class Display:
    """Manages scrolling text window with static elements."""
    
    def __init__(self, scroll_delay=0.03, line_delay=0.5, window_height=20):
        """
        Initialize display system.
        
        Args:
            scroll_delay (float): Not used anymore (kept for compatibility)
            line_delay (float): Delay between lines (seconds)
            window_height (int): Number of lines in the scrolling content area
        """
        self.scroll_delay = scroll_delay
        self.line_delay = 0.3  # Regular line delay
        self.exposition_line_delay = 0.6  # Slower for exposition text
        self.ui_width = 80
        self.window_height = window_height
        self.content_lines = [""] * window_height  # Initialize with empty lines
        self.header_text = "PythonDungeon"
        self.footer_text = ""
        
        # HP tracking for dynamic headers
        self.player = None
        self.monster = None
        self.show_hp_in_header = False
    
    def clear_screen(self):
        """Clear the terminal screen."""
        # Windows
        if os.name == 'nt':
            os.system('cls')
        # Unix/Linux/MacOS
        else:
            os.system('clear')
    
    def set_header(self, text):
        """Set the header text."""
        self.header_text = text
    
    def set_footer(self, text):
        """Set the footer text."""
        self.footer_text = text
    
    def set_player_for_header(self, player):
        """Set the player for HP display in header."""
        self.player = player
        self.show_hp_in_header = True
    
    def set_monster_for_header(self, monster):
        """Set the monster for HP display in header (combat mode)."""
        self.monster = monster
    
    def clear_hp_header(self):
        """Clear HP display from header."""
        self.player = None
        self.monster = None
        self.show_hp_in_header = False
    
    def get_dynamic_header(self):
        """Get header with dynamic HP information if enabled."""
        if not self.show_hp_in_header or not self.player:
            return self.header_text
        
        # Start with base header and player HP
        header_parts = []
        if self.header_text:
            header_parts.append(self.header_text)
        
        # Add player HP
        header_parts.append(f"{self.player.emoji} {self.player.name}: {self.player.current_health}/{self.player.max_health} HP")
        
        # Show monster name with health threshold icon if in combat
        if self.monster:
            health_icon = self.get_health_threshold_icon(self.monster)
            header_parts.append(f"🐉 {self.monster.name} {health_icon}")
        
        return " | ".join(header_parts)
    
    def get_health_threshold_icon(self, monster):
        """
        Get the appropriate health threshold icon based on monster's current health.
        
        Args:
            monster: The monster object
            
        Returns:
            str: Icon representing the monster's health status
        """
        if not monster:
            return ""
        
        health_percent = (monster.current_health / monster.max_health) * 100
        
        if health_percent <= 10:
            return "💀"  # Near death
        elif health_percent <= 25:
            return "⚠️"   # Badly injured
        elif health_percent <= 50:
            return "💔"  # Wounded
        elif health_percent <= 75:
            return "🩸"  # Slightly injured
        else:
            return "💚"  # Healthy
    
    def add_line(self, line, delay=None):
        """
        Add a line to the scrolling content area and refresh display.
        
        Args:
            line (str): Line to add to the scroll
            delay (float): Optional delay after adding the line. If None, uses self.line_delay
        """
        # Remove the first line and append the new line
        self.content_lines.pop(0)
        self.content_lines.append(line)
        self.refresh_display()
        
        # Add delay if specified
        if delay is not None and delay > 0:
            time.sleep(delay)
    
    def add_lines(self, lines, exposition=False):
        """
        Add multiple lines to the scrolling content area one by one with delays.
        
        Args:
            lines (list or str): Lines to add
            exposition (bool): Whether this is exposition text (slower display)
        """
        if isinstance(lines, str):
            lines = lines.split('\n')
        
        delay = self.exposition_line_delay if exposition else self.line_delay
        
        for line in lines:
            self.add_line(line)
            if delay > 0:
                time.sleep(delay)
    
    def print_header(self):
        """Print the static header bar with dynamic HP information."""
        print("=" * self.ui_width)
        dynamic_header = self.get_dynamic_header()
        centered_title = f"    {dynamic_header}    ".center(self.ui_width, "=")
        print(centered_title)
        print("=" * self.ui_width)
    
    def print_footer(self):
        """Print the static footer bar."""
        print("=" * self.ui_width)
        if self.footer_text:
            centered_message = self.footer_text.center(self.ui_width)
            print(centered_message)
        print("=" * self.ui_width)
    
    def refresh_display(self):
        """Refresh the entire display with current content."""
        self.clear_screen()
        
        # Print header
        self.print_header()
        
        # Print content area
        for line in self.content_lines:
            # Pad lines to fit width and add left margin
            padded_line = f"  {line}".ljust(self.ui_width - 2)
            print(padded_line)
        
        # Print footer
        self.print_footer()
    
    def clear_content(self):
        """Clear the scrolling content area."""
        self.content_lines = [""] * self.window_height
    
    def display_text(self, text, exposition=False, pause=False, title="PythonDungeon"):
        """
        Display text in the scrolling window by appending to existing content.
        
        Args:
            text (str or list): Text to display
            exposition (bool): Whether this is exposition text (slower line-by-line)
            pause (bool): Whether to pause for user input after
            title (str): Title for the header
        """
        self.set_header(title)
        self.set_footer("")  # Clear footer initially
        
        lines = text.split('\n') if isinstance(text, str) else text
        
        # Always append lines to the scrolling content
        self.add_lines(lines, exposition=exposition)
        
        # Only set footer and pause if requested
        if pause:
            self.set_footer("Press Enter to continue...")
            self.refresh_display()  # Update display to show footer
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                pass
    
    def display_menu(self, title, options, status="", exposition_intro=False):
        """
        Display a menu with options in the footer.
        
        Args:
            title (str): Menu title
            options (list): List of menu options
            status (str): Current status to show
            exposition_intro (bool): Whether to display intro text as exposition
        
        Returns:
            str: User's choice
        """
        # Set header and clear footer initially
        self.set_header(title)
        self.set_footer("")
        
        # Add a separator line before new content
        self.add_line("")
        self.add_line("-" * 60, delay=0.3)
        
        # Add status/intro content
        if status:
            status_lines = status.split('\n')
            self.add_lines(status_lines, exposition=exposition_intro)
        
        self.add_line("")
        
        # Create footer options text with shortened versions
        short_options = []
        for i, option in enumerate(options, 1):
            # Extract key words from option for shorter footer display
            if "Rest" in option:
                short_options.append(f"{i}) 🛏️ Rest")
            elif "adventure" in option.lower():
                short_options.append(f"{i}) 🗺️ Adventure")
            elif any(location in option for location in ["Forest", "Cave", "Desert", "Mountain", "Dungeon"]):
                # Extract the emoji and location name from the full option text
                # This handles dynamic location names without hardcoding
                if "🌲" in option:  # Forest
                    short_options.append(f"{i}) 🌲 Forest")
                elif "🕳️" in option:  # Cave
                    short_options.append(f"{i}) 🕳️ Cave")
                elif "🏜️" in option:  # Desert  
                    short_options.append(f"{i}) 🏜️ Desert")
                elif "⛰️" in option:  # Mountain
                    short_options.append(f"{i}) ⛰️ Mountain")
                elif "🏰" in option:  # Dungeon
                    short_options.append(f"{i}) 🏰 Dungeon")
                else:
                    # Fallback: try to extract emoji and first word after it
                    parts = option.split()
                    if len(parts) >= 2:
                        emoji = parts[0]
                        location = parts[1]
                        short_options.append(f"{i}) {emoji} {location}")
                    else:
                        short_options.append(f"{i}) {option}")
            elif "stats" in option:
                short_options.append(f"{i}) 📊 Stats")
            elif "Save game" in option:
                short_options.append(f"{i}) 💾 Save")
            elif "Settings" in option:
                short_options.append(f"{i}) ⚙️ Settings")
            elif "Quit" in option:
                short_options.append(f"{i}) 🚪 Quit")
            elif "Continue exploring" in option:
                short_options.append(f"{i}) 🌲 Continue")
            elif "Return to" in option:
                short_options.append(f"{i}) 🏠 Return")
            else:
                # Fallback to first few words
                words = option.split()[:3]
                short_options.append(f"{i}) {' '.join(words)}")
        
        options_text = " | ".join(short_options) + ": "
        
        # Get user choice using footer
        while True:
            try:
                self.set_footer(options_text)
                self.refresh_display()
                choice = input().strip()
                if choice.isdigit() and 1 <= int(choice) <= len(options):
                    self.set_footer("")  # Clear footer after successful choice
                    return choice
                self.add_line(f"Please choose a number between 1 and {len(options)}.")
            except (EOFError, KeyboardInterrupt):
                self.add_line("Game interrupted.")
                return "quit"
    
    def display_stats(self, character):
        """
        Display character stats by appending to the scrolling window.
        
        Args:
            character: Character object with stats to display
        """
        self.set_header(f"{character.name}'s Character Stats")
        self.set_footer("")  # Clear footer initially
        
        # Add separator and stats to scrolling content
        self.add_line("")
        self.add_line("-" * 40)
        self.add_line(f"📊 {character.name}'s Stats:")
        self.add_line("")
        
        stats_lines = [
            f"Name: {character.name}",
            f"Level: {character.level}",
            f"Health: {character.current_health}/{character.max_health}",
            f"Strength: {character.strength}",
            f"Status: {character.get_health_status()}",
        ]
        
        self.add_lines(stats_lines)
        
        # Set footer and refresh display for pause
        self.set_footer("Press Enter to continue...")
        self.refresh_display()
        
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            pass
    
    def display_combat_round(self, player, monster):
        """
        Display combat round information in scrolling window with player HP in header.
        
        Args:
            player: Player object
            monster: Monster object  
        """
        # Set up combat header with player HP and monster name
        self.set_header("COMBAT")
        self.set_player_for_header(player)
        self.set_monster_for_header(monster)
        self.set_footer("")
    
    def display_combat_options(self):
        """
        Display combat options in the footer and get user choice.
        
        Returns:
            str: User's choice (1-3)
        """
        options_text = "1) ⚔️ Attack  2) 💚 Heal  3) 🏃 Try to flee"
        
        while True:
            try:
                self.set_footer(options_text)
                self.refresh_display()
                choice = input().strip()
                if choice in ['1', '2', '3']:
                    # Clear footer after successful choice
                    self.set_footer("")
                    return choice
                self.add_line(f"Please choose 1, 2, or 3.")
            except (EOFError, KeyboardInterrupt):
                return "quit"

# Global display instance for easy access
display = Display()

# Example usage and testing
if __name__ == "__main__":
    # Test the scrolling display system
    display.display_text("Welcome to the Scrolling Display System!", exposition=True, pause=True, title="UI Test")
    
    # Test adding multiple lines
    display.clear_content()
    display.set_header("Testing Scroll")
    for i in range(20):
        display.add_line(f"This is line {i+1}")
        time.sleep(0.2)
    
    input("Press Enter to exit test...")