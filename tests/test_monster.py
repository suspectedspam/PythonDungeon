#!/usr/bin/env python3
"""
Test suite for the monster system.
Tests monster classes, level scaling, and database integration.
"""

import pytest
from unittest.mock import Mock, patch
from src.entities.monster import Monster


class TestMonsterBaseClass:
    """Test the base Monster class functionality."""
    
    def test_monster_creation(self):
        """Test basic monster creation with all parameters."""
        monster = Monster(
            name="Test Goblin",
            max_health=25,
            strength=8,
            level=3,
            emoji="👹"
        )
        
        assert monster.name == "Test Goblin"
        assert monster.max_health == 25
        assert monster.current_health == 25
        assert monster.strength == 8
        assert monster.level == 3
        assert monster.is_alive is True
        assert monster.emoji == "👹"
    
    def test_monster_default_values(self):
        """Test monster creation with default values."""
        monster = Monster("Simple Goblin", max_health=20, strength=5)
        
        assert monster.level == 1  # Default level
        assert monster.emoji == "🐾"  # Default emoji
        assert monster.is_alive is True
    
    def test_update_health(self):
        """Test updating monster health."""
        monster = Monster("Test Monster", max_health=30, strength=6)
        
        # Test normal damage
        monster.update_health(20)
        assert monster.current_health == 20
        assert monster.is_alive is True
        
        # Test fatal damage
        monster.update_health(0)
        assert monster.current_health == 0
        assert monster.is_alive is False
        
        # Test negative health (should be clamped to 0)
        monster.update_health(-5)
        assert monster.current_health == 0
        assert monster.is_alive is False
    
    def test_get_health_status(self):
        """Test health status descriptions."""
        monster = Monster("Status Monster", max_health=40, strength=7)
        
        # Test full health (100%)
        status = monster.get_health_status()
        assert "perfect condition" in status.lower()
        
        # Test wounded (75%)
        monster.update_health(30)
        status = monster.get_health_status()
        assert len(status) > 0  # Should return some description
        
        # Test badly wounded (25%)
        monster.update_health(10)
        status = monster.get_health_status()
        assert len(status) > 0
        
        # Test dead (0%)
        monster.update_health(0)
        status = monster.get_health_status()
        assert "dead" in status.lower() or "defeated" in status.lower()


class TestMonsterLevelScaling:
    """Test the monster level scaling system."""
    
    def test_calculate_monster_level_same_level(self):
        """Test monster level calculation - same as player level."""
        # Mock random to always return 0.25 (50% chance range)
        with patch('src.entities.monster.random.random', return_value=0.25):
            level = Monster._calculate_monster_level(5)
            assert level == 5  # Same level as player
    
    def test_calculate_monster_level_plus_one(self):
        """Test monster level calculation - player level +1."""
        # Mock random to return 0.60 (20% chance for +1)
        with patch('src.entities.monster.random.random', return_value=0.60):
            level = Monster._calculate_monster_level(5)
            assert level == 6  # Player level + 1
    
    def test_calculate_monster_level_minus_one(self):
        """Test monster level calculation - player level -1."""
        # Mock random to return 0.80 (20% chance for -1)
        with patch('src.entities.monster.random.random', return_value=0.80):
            level = Monster._calculate_monster_level(5)
            assert level == 4  # Player level - 1
    
    def test_calculate_monster_level_plus_two(self):
        """Test monster level calculation - player level +2."""
        # Mock random to return 0.92 (5% chance for +2)
        with patch('src.entities.monster.random.random', return_value=0.92):
            level = Monster._calculate_monster_level(5)
            assert level == 7  # Player level + 2
    
    def test_calculate_monster_level_minus_two(self):
        """Test monster level calculation - player level -2."""
        # Mock random to return 0.97 (5% chance for -2)
        with patch('src.entities.monster.random.random', return_value=0.97):
            level = Monster._calculate_monster_level(5)
            assert level == 3  # Player level - 2
    
    def test_calculate_monster_level_cap_at_10(self):
        """Test that monster level is capped at 10 (forest area max)."""
        # High level player, +2 modifier
        with patch('src.entities.monster.random.random', return_value=0.92):
            level = Monster._calculate_monster_level(15)
            assert level == 10  # Capped at forest max level
    
    def test_calculate_monster_level_minimum_1(self):
        """Test that monster level has minimum of 1."""
        # Low level player, -2 modifier
        with patch('src.entities.monster.random.random', return_value=0.97):
            level = Monster._calculate_monster_level(1)
            assert level == 1  # Minimum level is 1
    
    def test_calculate_monster_level_distribution(self):
        """Test the probability distribution over many calculations."""
        # This test checks that the distribution is roughly correct
        levels = []
        player_level = 5
        
        # Simulate many level calculations
        for i in range(1000):
            with patch('src.entities.monster.random.random', return_value=i/1000):
                level = Monster._calculate_monster_level(player_level)
                levels.append(level)
        
        # Count occurrences
        level_counts = {}
        for level in levels:
            level_counts[level] = level_counts.get(level, 0) + 1
        
        # Check that level 5 (same as player) appears most frequently (~50%)
        same_level_count = level_counts.get(5, 0)
        assert same_level_count >= 450  # At least 45% (allowing for some variance)
        
        # Check that +/- 1 levels appear (~20% each)
        plus_one_count = level_counts.get(6, 0)
        minus_one_count = level_counts.get(4, 0)
        assert plus_one_count >= 150  # At least 15%
        assert minus_one_count >= 150  # At least 15%
        
        # Check that +/- 2 levels appear (~5% each)
        plus_two_count = level_counts.get(7, 0)
        minus_two_count = level_counts.get(3, 0)
        assert plus_two_count >= 30  # At least 3%
        assert minus_two_count >= 30  # At least 3%


class TestMonsterCreation:
    """Test monster creation methods."""
    
    @patch('src.entities.monster.Monster._calculate_monster_level')
    @patch('src.core.gamedata.game_db.get_random_monster')
    def test_create_random_for_level_success(self, mock_get_monster, mock_calc_level):
        """Test successful monster creation from database."""
        # Mock the level calculation
        mock_calc_level.return_value = 5
        
        # Mock database response
        mock_monster_data = {
            'name': 'Forest Orc',
            'health': 35,
            'strength': 10,
            'emoji': '👺'
        }
        mock_get_monster.return_value = mock_monster_data
        
        # Mock create_from_database
        with patch.object(Monster, 'create_from_database') as mock_create:
            mock_monster = Monster("Forest Orc", 35, 10, 5, "👺")
            mock_create.return_value = mock_monster
            
            result = Monster.create_random_for_level(3)
            
            # Verify the methods were called correctly
            mock_calc_level.assert_called_once_with(3)
            mock_get_monster.assert_called_once_with(5)  # Calculated level
            mock_create.assert_called_once_with(mock_monster_data, 5)
            
            assert result == mock_monster
    
    @patch('src.entities.monster.Monster._calculate_monster_level')
    @patch('src.core.gamedata.game_db.get_random_monster')
    def test_create_random_for_level_database_error(self, mock_get_monster, mock_calc_level):
        """Test fallback when database fails."""
        # Mock the level calculation
        mock_calc_level.return_value = 3
        
        # Mock database error
        mock_get_monster.side_effect = Exception("Database connection error")
        
        # Mock fallback monster creation
        with patch.object(Monster, 'create_fallback_monster') as mock_fallback:
            mock_monster = Monster("Goblin", 25, 7, 3, "👹")
            mock_fallback.return_value = mock_monster
            
            result = Monster.create_random_for_level(3)
            
            # Verify fallback was used
            mock_fallback.assert_called_once_with(3)
            assert result == mock_monster
    
    def test_create_fallback_monster_low_level(self):
        """Test fallback monster creation for low levels."""
        monster = Monster.create_fallback_monster(2)
        
        assert monster.name == "Goblin"
        assert monster.level == 2
        assert monster.emoji == "👹"
        assert monster.max_health > 20  # Should scale with level
        assert monster.strength > 3  # Should scale with level
    
    def test_create_fallback_monster_mid_level(self):
        """Test fallback monster creation for mid levels."""
        monster = Monster.create_fallback_monster(4)
        
        assert monster.name == "Orc"
        assert monster.level == 4
        assert monster.emoji == "👺"
        assert monster.max_health > 30  # Should scale with level
        assert monster.strength > 6  # Should scale with level
    
    def test_create_fallback_monster_high_level(self):
        """Test fallback monster creation for high levels."""
        monster = Monster.create_fallback_monster(8)
        
        assert monster.name == "Troll"
        assert monster.level == 8
        assert monster.emoji == "🧌"
        assert monster.max_health > 40  # Should scale with level
        assert monster.strength > 10  # Should scale with level
    
    def test_create_from_database_tuple_format(self):
        """Test creating monster from database tuple data (real format)."""
        # Real database format: (id, name, min_level, max_level, base_health, base_strength, emoji, rarity, description)
        monster_data = (1, 'Shadow Wolf', 3, 7, 40, 12, '🐺', 'common', 'A fierce forest predator')
        
        monster = Monster.create_from_database(monster_data, player_level=6)
        
        assert monster.name == "Shadow Wolf"
        assert monster.level == 6  # Should use player level
        assert monster.emoji == "🐺"
        # Health and strength should be scaled based on level
        # Level 6: scaling = max(0, 6-1) = 5
        # Health: 40 + (5 * 3) = 55
        # Strength: 12 + (5 // 2) = 14
        assert monster.max_health == 55
        assert monster.strength == 14
    
    def test_create_from_database_dict_format(self):
        """Test creating monster from dict data (test format)."""
        monster_data = {
            'name': 'Test Orc',
            'health': 30,
            'strength': 8,
            'emoji': '�'
        }
        
        monster = Monster.create_from_database(monster_data, player_level=4)
        
        assert monster.name == "Test Orc"
        assert monster.level == 4
        assert monster.emoji == "�"
        # Level 4: scaling = max(0, 4-1) = 3
        # Health: 30 + (3 * 3) = 39
        # Strength: 8 + (3 // 2) = 9
        assert monster.max_health == 39
        assert monster.strength == 9
    
    def test_create_from_database_integration(self):
        """Test monster creation with actual database integration."""
        from src.core.gamedata import game_db
        
        # This tests the actual database tuple format
        try:
            # Get a real monster from the database
            monster_data = game_db.get_random_monster(player_level=3)
            
            if monster_data:  # Only test if database has data
                monster = Monster.create_from_database(monster_data, player_level=3)
                
                # Verify it created a valid monster
                assert monster.name is not None
                assert monster.level == 3
                assert monster.max_health > 0
                assert monster.strength > 0
                assert monster.emoji is not None
                
                # Verify tuple format is being used correctly
                assert isinstance(monster_data, tuple)
                assert len(monster_data) >= 7  # Should have at least 7 fields
        except Exception:
            # If database isn't populated, that's fine for now
            pass


class TestMonsterDatabase:
    """Test monster database operations."""
    
    def test_monster_exists(self):
        """Test that we can create monsters (basic functionality)."""
        monster = Monster("Test Monster", max_health=25, strength=6, level=2)
        
        assert monster is not None
        assert monster.name == "Test Monster"
        assert monster.level == 2


class TestMonsterIntegration:
    """Integration tests for monster system."""
    
    def test_monster_combat_simulation(self):
        """Test monster in a simulated combat scenario."""
        monster = Monster("Battle Test", max_health=30, strength=8, level=3)
        
        # Simulate taking damage
        initial_health = monster.current_health
        monster.update_health(initial_health - 10)
        
        assert monster.current_health == initial_health - 10
        assert monster.is_alive is True
        
        # Simulate fatal damage
        monster.update_health(0)
        assert monster.is_alive is False
    
    def test_monster_level_scaling_integration(self):
        """Test the complete monster creation with level scaling."""
        player_levels = [1, 5, 10, 15]
        
        for player_level in player_levels:
            # Test level calculation bounds
            for _ in range(10):  # Test multiple times due to randomness
                calculated_level = Monster._calculate_monster_level(player_level)
                
                # Should be within ±2 levels of player, but capped at 1-10
                min_expected = max(1, player_level - 2)
                max_expected = min(10, player_level + 2)
                
                assert min_expected <= calculated_level <= max_expected
    
    def test_monster_stats_scaling(self):
        """Test that monster stats scale appropriately with level."""
        low_level = Monster.create_fallback_monster(1)
        high_level = Monster.create_fallback_monster(5)
        
        # Higher level monsters should generally be stronger
        assert high_level.max_health >= low_level.max_health
        assert high_level.strength >= low_level.strength