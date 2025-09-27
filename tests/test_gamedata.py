"""
Unit tests for GameDatabase class
"""

import pytest
import os
import tempfile
import sqlite3
from unittest.mock import patch, Mock
from src.core.gamedata import GameDatabase


@pytest.mark.database
class TestGameDatabaseInit:
    """Test GameDatabase initialization."""
    
    def test_database_creation(self, temp_db):
        """Test database is created successfully."""
        assert os.path.exists(temp_db.db_path)
    
    def test_database_tables_exist(self, temp_db):
        """Test all required tables are created."""
        conn = sqlite3.connect(temp_db.db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        required_tables = ['players', 'player_stats', 'player_settings', 'monster_templates']
        for table in required_tables:
            assert table in tables, f"Table {table} not found in database"
    
    def test_players_table_structure(self, temp_db):
        """Test players table has correct structure."""
        conn = sqlite3.connect(temp_db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(players)")
        columns = [column[1] for column in cursor.fetchall()]
        
        conn.close()
        
        required_columns = [
            'name', 'level', 'current_health', 'max_health', 
            'strength', 'emoji', 'created_at', 'last_played', 'unlocked_areas'
        ]
        
        for column in required_columns:
            assert column in columns, f"Column {column} not found in players table"


@pytest.mark.database
class TestPlayerOperations:
    """Test database operations for players."""
    
    def test_save_new_player(self, temp_db, test_player):
        """Test saving a new player."""
        temp_db.save_player(test_player)
        
        # Verify player was saved
        conn = sqlite3.connect(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM players WHERE name = ?", (test_player.name,))
        row = cursor.fetchone()
        conn.close()
        
        assert row is not None
        assert row[0] == test_player.name
        assert row[1] == test_player.level
    
    def test_load_existing_player(self, temp_db, test_player):
        """Test loading an existing player."""
        # Save first
        temp_db.save_player(test_player)
        
        # Load
        loaded_player = temp_db.load_player(test_player.name)
        
        assert loaded_player is not None
        assert loaded_player.name == test_player.name
        assert loaded_player.level == test_player.level
    
    def test_load_nonexistent_player(self, temp_db):
        """Test loading a player that doesn't exist."""
        loaded_data = temp_db.load_player("NonexistentPlayer")
        assert loaded_data is None
    
    def test_get_all_players(self, temp_db, test_player):
        """Test getting all players."""
        # Save test player
        temp_db.save_player(test_player)
        
        # Create and save another player
        player2 = test_player.__class__("TestHero2", "🧙‍♀️")
        temp_db.save_player(player2)
        
        # Get all players
        all_players = temp_db.get_all_players()
        
        assert len(all_players) == 2
        player_names = [player[0] for player in all_players]
        assert "TestHero" in player_names
        assert "TestHero2" in player_names
    
    def test_delete_player(self, temp_db, test_player):
        """Test deleting a player."""
        # Save first
        temp_db.save_player(test_player)
        
        # Verify exists
        loaded = temp_db.load_player(test_player.name)
        assert loaded is not None
        
        # Delete
        temp_db.delete_player(test_player.name)
        
        # Verify deleted
        loaded_after_delete = temp_db.load_player(test_player.name)
        assert loaded_after_delete is None


@pytest.mark.database
class TestUnlockedAreas:
    """Test unlocked areas functionality."""
    
    def test_get_default_unlocked_areas(self, temp_db, test_player):
        """Test new player gets forest unlocked by default."""
        temp_db.save_player(test_player)
        
        unlocked = temp_db.get_player_unlocked_areas(test_player.name)
        
        assert 'forest' in unlocked
        assert len(unlocked) == 1
    
    def test_unlock_new_area(self, temp_db, test_player):
        """Test unlocking a new area."""
        temp_db.save_player(test_player)
        
        # Unlock cave
        result = temp_db.unlock_area_for_player(test_player.name, 'cave')
        
        assert 'forest' in result
        assert 'cave' in result
        assert len(result) == 2
    
    def test_unlock_duplicate_area(self, temp_db, test_player):
        """Test unlocking an area that's already unlocked."""
        temp_db.save_player(test_player)
        
        # Try to unlock forest again
        result = temp_db.unlock_area_for_player(test_player.name, 'forest')
        
        assert 'forest' in result
        assert len(result) == 1  # Should not duplicate


@pytest.mark.database
class TestPlayerStats:
    """Test player statistics functionality."""
    
    def test_get_default_stats(self, temp_db, test_player):
        """Test getting default stats for new player."""
        temp_db.save_player(test_player)
        
        stats = temp_db.get_player_stats(test_player.name)
        
        assert isinstance(stats, dict)
        assert stats['total_monsters_defeated'] == 0
        assert stats['total_damage_dealt'] == 0
        assert stats['times_rested'] == 0
    
    def test_update_player_stat(self, temp_db, test_player):
        """Test updating a player statistic."""
        temp_db.save_player(test_player)
        
        # Update monsters defeated
        temp_db.update_player_stat(test_player.name, 'total_monsters_defeated', 5)
        
        stats = temp_db.get_player_stats(test_player.name)
        assert stats['total_monsters_defeated'] == 5
    
    def test_update_stat_multiple_times(self, temp_db, test_player):
        """Test updating same stat multiple times accumulates."""
        temp_db.save_player(test_player)
        
        # Update damage dealt multiple times
        temp_db.update_player_stat(test_player.name, 'total_damage_dealt', 10)
        temp_db.update_player_stat(test_player.name, 'total_damage_dealt', 15)
        
        stats = temp_db.get_player_stats(test_player.name)
        assert stats['total_damage_dealt'] == 25


@pytest.mark.database 
class TestPlayerSettings:
    """Test player settings functionality."""
    
    def test_get_default_settings(self, temp_db, test_player):
        """Test getting default settings."""
        temp_db.save_player(test_player)
        
        settings = temp_db.get_player_settings(test_player.name)
        
        assert isinstance(settings, dict)
        assert settings['auto_save_after_rest'] == True
        assert settings['auto_save_after_combat'] == True
        assert settings['auto_save_on_inn_visit'] == False
    
    def test_update_settings(self, temp_db, test_player):
        """Test updating player settings."""
        temp_db.save_player(test_player)
        
        new_settings = {
            'auto_save_after_rest': False,
            'auto_save_after_combat': True,
            'auto_save_on_inn_visit': True
        }
        
        temp_db.update_player_settings(test_player.name, new_settings)
        
        updated_settings = temp_db.get_player_settings(test_player.name)
        assert updated_settings['auto_save_after_rest'] == False
        assert updated_settings['auto_save_on_inn_visit'] == True


@pytest.mark.database
class TestMonsterOperations:
    """Test monster-related database operations."""
    
    def test_monsters_table_populated(self, temp_db):
        """Test that monster templates are populated on init."""
        conn = sqlite3.connect(temp_db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM monster_templates")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        assert count > 0, "Monster templates should be populated"
    
    def test_get_random_monster(self, temp_db):
        """Test getting a random monster."""
        monster = temp_db.get_random_monster(player_level=1)
        
        assert monster is not None
        assert len(monster) >= 8  # Should have all monster fields
    
    def test_get_random_monster_level_appropriate(self, temp_db):
        """Test that random monster is appropriate for player level."""
        monster = temp_db.get_random_monster(player_level=1)
        
        if monster:
            min_level = monster[2]  # min_level column
            max_level = monster[3]  # max_level column
            
            assert min_level <= 1 <= max_level


@pytest.mark.database
class TestDatabaseMigration:
    """Test database migration functionality."""
    
    def test_migration_adds_unlocked_areas_column(self):
        """Test that migration adds unlocked_areas column to existing database."""
        # Create a temporary database without the unlocked_areas column
        temp_fd, temp_path = tempfile.mkstemp(suffix='.db')
        os.close(temp_fd)
        
        try:
            # Create database with old schema (without unlocked_areas)
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE players (
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
            conn.commit()
            conn.close()
            
            # Now create GameDatabase instance - should trigger migration
            db = GameDatabase(temp_path)
            
            # Manually run migration to ensure it works
            db.migrate_database()
            
            # Check that unlocked_areas column exists
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(players)")
            columns = [column[1] for column in cursor.fetchall()]
            conn.close()
            
            assert 'unlocked_areas' in columns
        
        finally:
            # Cleanup
            try:
                os.unlink(temp_path)
            except OSError:
                pass


if __name__ == "__main__":
    pytest.main([__file__])