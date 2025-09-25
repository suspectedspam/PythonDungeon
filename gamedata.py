#!/usr/bin/env python3
"""
Game database management using SQLite
Handles player saves, statistics, and monster templates
"""

import sqlite3
import os
import random
from datetime import datetime

class GameDatabase:
    def __init__(self, db_path="pythondungeon.db"):
        """Initialize the game database."""
        self.db_path = db_path
        self.init_database()
        
        # Only populate monsters if table is empty (first run)
        if self.is_monsters_table_empty():
            self.populate_initial_monsters()
    
    def init_database(self):
        """Create all necessary tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Players table - save character data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                name TEXT PRIMARY KEY,
                level INTEGER NOT NULL,
                current_health INTEGER NOT NULL,
                max_health INTEGER NOT NULL,
                strength INTEGER NOT NULL,
                emoji TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_played TEXT NOT NULL
            )
        ''')
        
        # Game stats table - track player statistics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_stats (
                player_name TEXT PRIMARY KEY,
                battles_won INTEGER DEFAULT 0,
                battles_lost INTEGER DEFAULT 0,
                monsters_defeated INTEGER DEFAULT 0,
                total_damage_dealt INTEGER DEFAULT 0,
                times_fled INTEGER DEFAULT 0,
                FOREIGN KEY (player_name) REFERENCES players (name)
            )
        ''')
        
        # Player settings table - track player preferences
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_settings (
                player_name TEXT PRIMARY KEY,
                auto_save_after_rest BOOLEAN DEFAULT 1,
                auto_save_after_combat BOOLEAN DEFAULT 1,
                auto_save_on_inn_visit BOOLEAN DEFAULT 0,
                FOREIGN KEY (player_name) REFERENCES players (name)
            )
        ''')
        
        # Monster templates table - define monster types
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monster_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                min_level INTEGER NOT NULL,
                max_level INTEGER NOT NULL,
                base_health INTEGER NOT NULL,
                base_strength INTEGER NOT NULL,
                emoji TEXT NOT NULL,
                rarity TEXT DEFAULT 'common',
                description TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def is_monsters_table_empty(self):
        """Check if monster_templates table has any data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM monster_templates')
        count = cursor.fetchone()[0]
        conn.close()
        
        return count == 0
    
    def populate_initial_monsters(self):
        """Add initial monster set to database (only runs once)."""
        print("🐉 Setting up monster database...")
        
        initial_monsters = [
            ("Goblin", 1, 2, 20, 3, "👹", "common", "A small, green creature with sharp teeth and malicious eyes"),
            ("Forest Wolf", 1, 3, 25, 4, "🐺", "common", "A wild wolf that hunts in packs through the dark forest"),
            ("Orc Warrior", 2, 4, 35, 5, "👺", "common", "A brutal warrior with crude weapons and fierce determination"),
            ("Giant Spider", 2, 3, 22, 4, "🕷️", "common", "A massive arachnid that lurks in shadowy corners"),
            ("Skeleton Warrior", 3, 5, 30, 6, "💀", "uncommon", "An undead soldier from ancient battles, still wielding rusty weapons"),
            ("Cave Troll", 4, 6, 60, 8, "🧌", "uncommon", "A massive creature with regenerative powers and stone-like skin"),
            ("Dark Mage", 3, 6, 28, 7, "🧙‍♂️", "uncommon", "A corrupted wizard wielding forbidden magic"),
            ("Fire Drake", 5, 8, 80, 10, "🐲", "rare", "A young dragon with fiery breath and scales like molten metal"),
            ("Shadow Beast", 6, 8, 70, 12, "👤", "rare", "A creature born from pure darkness and nightmares"),
            ("Ancient Dragon", 8, 10, 150, 18, "🐉", "legendary", "A legendary beast of immense power and ancient wisdom"),
            ("Lich King", 9, 10, 120, 16, "👑", "legendary", "An undead sorcerer of unimaginable magical power")
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.executemany('''
            INSERT INTO monster_templates 
            (name, min_level, max_level, base_health, base_strength, emoji, rarity, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', initial_monsters)
        
        conn.commit()
        conn.close()
        print("✅ Monster database ready with {} creatures!".format(len(initial_monsters)))
    
    # Player save/load methods
    def save_player(self, player):
        """Save player to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT OR REPLACE INTO players 
            (name, level, current_health, max_health, strength, emoji, created_at, last_played)
            VALUES (?, ?, ?, ?, ?, ?, 
                    COALESCE((SELECT created_at FROM players WHERE name = ?), ?), 
                    ?)
        ''', (player.name, player.level, player.current_health, player.max_health, 
              player.strength, player.emoji, player.name, now, now))
        
        # Initialize stats if new player
        cursor.execute('''
            INSERT OR IGNORE INTO player_stats (player_name) VALUES (?)
        ''', (player.name,))
        
        # Initialize settings if new player
        cursor.execute('''
            INSERT OR IGNORE INTO player_settings (player_name) VALUES (?)
        ''', (player.name,))
        
        conn.commit()
        conn.close()
    
    def load_player(self, name):
        """Load player from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM players WHERE name = ?', (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            from player import Player
            player = Player(
                name=row[0],
                max_health=row[3],
                strength=row[4], 
                level=row[1],
                emoji=row[5]
            )
            player.current_health = row[2]
            return player
        return None
    
    def get_all_saves(self):
        """Get list of all saved characters."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, level, emoji, last_played 
            FROM players 
            ORDER BY last_played DESC
        ''')
        saves = cursor.fetchall()
        conn.close()
        
        return saves
    
    # Monster database methods
    def get_monsters_for_level(self, player_level):
        """Get all monsters appropriate for player's level."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM monster_templates 
            WHERE min_level <= ? AND max_level >= ?
            ORDER BY rarity, name
        ''', (player_level, player_level))
        
        monsters = cursor.fetchall()
        conn.close()
        return monsters
    
    def get_random_monster(self, player_level):
        """Get a random monster appropriate for player's level."""
        monsters = self.get_monsters_for_level(player_level)
        if not monsters:
            return None
        
        # Weight by rarity (common monsters more likely)
        weights = []
        for monster in monsters:
            rarity = monster[6]  # rarity column
            if rarity == 'common':
                weights.append(50)
            elif rarity == 'uncommon':
                weights.append(20)
            elif rarity == 'rare':
                weights.append(8)
            elif rarity == 'legendary':
                weights.append(2)
            else:
                weights.append(25)
        
        return random.choices(monsters, weights=weights)[0]
    
    def add_monster_template(self, name, min_level, max_level, base_health, 
                           base_strength, emoji, rarity='common', description=''):
        """Add a new monster template to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO monster_templates 
            (name, min_level, max_level, base_health, base_strength, emoji, rarity, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, min_level, max_level, base_health, base_strength, emoji, rarity, description))
        
        conn.commit()
        conn.close()
    
    # Statistics methods
    def update_battle_stats(self, player_name, won=False, damage_dealt=0, fled=False):
        """Update battle statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if won:
            cursor.execute('''
                UPDATE player_stats 
                SET battles_won = battles_won + 1,
                    monsters_defeated = monsters_defeated + 1,
                    total_damage_dealt = total_damage_dealt + ?
                WHERE player_name = ?
            ''', (damage_dealt, player_name))
        elif fled:
            cursor.execute('''
                UPDATE player_stats 
                SET times_fled = times_fled + 1,
                    total_damage_dealt = total_damage_dealt + ?
                WHERE player_name = ?
            ''', (damage_dealt, player_name))
        else:  # lost
            cursor.execute('''
                UPDATE player_stats 
                SET battles_lost = battles_lost + 1,
                    total_damage_dealt = total_damage_dealt + ?
                WHERE player_name = ?
            ''', (damage_dealt, player_name))
        
        conn.commit()
        conn.close()
    
    def get_player_stats(self, player_name):
        """Get player statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM player_stats WHERE player_name = ?', (player_name,))
        row = cursor.fetchone()
        conn.close()
        
        return row
    
    # Settings methods
    def get_player_settings(self, player_name):
        """Get player settings."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM player_settings WHERE player_name = ?', (player_name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'auto_save_after_rest': bool(row[1]),
                'auto_save_after_combat': bool(row[2]),
                'auto_save_on_inn_visit': bool(row[3])
            }
        else:
            # Return defaults if no settings found
            return {
                'auto_save_after_rest': True,
                'auto_save_after_combat': True,
                'auto_save_on_inn_visit': False
            }
    
    def update_player_settings(self, player_name, settings):
        """Update player settings."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO player_settings 
            (player_name, auto_save_after_rest, auto_save_after_combat, auto_save_on_inn_visit)
            VALUES (?, ?, ?, ?)
        ''', (player_name, 
              int(settings['auto_save_after_rest']),
              int(settings['auto_save_after_combat']),
              int(settings['auto_save_on_inn_visit'])))
        
        conn.commit()
        conn.close()

# Global database instance
game_db = GameDatabase()