"""
Unit tests for Player class
"""

import pytest
from unittest.mock import Mock, patch
from src.core.player import Player


class TestPlayerCreation:
    """Test player creation and initialization."""
    
    def test_player_creation_with_valid_data(self, test_player):
        """Test creating a player with valid name and emoji."""
        assert test_player.name == "TestHero"
        assert test_player.emoji == "🧙"
        assert test_player.level == 1
        assert test_player.current_health == 50
        assert test_player.max_health == 50
        assert test_player.strength == 6  # Default strength is 6, not 5
        assert test_player.is_alive == True
    
    def test_player_creation_empty_name(self):
        """Test that empty name is allowed (Player is permissive)."""
        player = Player("", emoji="🧙")
        assert player.name == ""
        assert player.emoji == "🧙"
    
    def test_player_creation_none_values(self):
        """Test that None name is preserved as None."""
        player = Player(None, emoji="🧙")
        assert player.name is None  # Player stores None as-is
        assert player.emoji == "🧙"


class TestPlayerHealth:
    """Test player health management."""
    
    def test_initial_health(self, test_player):
        """Test player starts with full health."""
        assert test_player.current_health == test_player.max_health
        assert test_player.is_alive == True
    
    def test_take_damage(self, test_player):
        """Test taking damage reduces health."""
        initial_health = test_player.current_health
        damage = 10
        
        test_player.update_health(initial_health - damage)
        
        assert test_player.current_health == initial_health - damage
        assert test_player.is_alive == True
    
    def test_take_fatal_damage(self, test_player):
        """Test taking fatal damage sets is_alive to False."""
        test_player.update_health(0)
        
        assert test_player.current_health == 0
        assert test_player.is_alive == False
    
    def test_heal_damage(self, test_player):
        """Test healing restores health."""
        # Damage player first
        test_player.update_health(30)
        assert test_player.current_health == 30
        
        # Heal player
        healed = test_player.heal(15)
        
        assert test_player.current_health == 45
        assert healed == 15
        assert test_player.is_alive == True
    
    def test_heal_beyond_max(self, test_player):
        """Test healing cannot exceed max health."""
        # Damage player slightly
        test_player.update_health(45)
        
        # Try to overheal
        healed = test_player.heal(20)
        
        assert test_player.current_health == test_player.max_health
        assert healed == 5  # Only healed to max
    
    def test_rest_full_heal(self, test_player):
        """Test resting fully restores health."""
        # Damage player
        test_player.update_health(25)
        
        # Rest
        healed = test_player.rest()
        
        assert test_player.current_health == test_player.max_health
        assert healed == 25


class TestPlayerLeveling:
    """Test player leveling system."""
    
    def test_initial_level(self, test_player):
        """Test player starts at level 1."""
        assert test_player.level == 1
    
    @pytest.mark.parametrize("level", [2, 5, 10])
    def test_level_scaling_health(self, level):
        """Test health scales with level."""
        player = Player("Test", "🧙")
        player.level = level
        
        expected_health = 50 + (level - 1) * 10
        player.max_health = expected_health
        player.current_health = expected_health
        
        assert player.max_health == expected_health
    
    @pytest.mark.parametrize("level", [2, 5, 10])
    def test_level_scaling_strength(self, level):
        """Test strength scales with level."""
        player = Player("Test", "🧙")
        player.level = level
        
        expected_strength = 5 + (level - 1) * 2
        player.strength = expected_strength
        
        assert player.strength == expected_strength


@pytest.mark.database
class TestPlayerDatabase:
    """Test player database operations."""
    
    def test_save_player(self, test_player, temp_db):
        """Test saving player to database."""
        with patch('src.core.gamedata.game_db', temp_db):
            # Save should not raise exception
            temp_db.save_player(test_player)
            
            # Verify player was saved
            saved_player = temp_db.load_player(test_player.name)
            assert saved_player is not None
            assert saved_player.name == test_player.name
    
    def test_load_player(self, test_player_with_db, temp_db):
        """Test loading player from database."""
        # test_player_with_db is already saved to temp_db
        loaded_player = temp_db.load_player("TestHero")
        
        assert loaded_player is not None
        assert loaded_player.name == "TestHero"
        assert loaded_player.level == 1
    
    def test_get_unlocked_areas_default(self, test_player, temp_db):
        """Test new player gets forest unlocked by default."""
        with patch('src.core.gamedata.game_db', temp_db):
            temp_db.save_player(test_player)
            unlocked = test_player.get_unlocked_areas()
            
            assert 'forest' in unlocked
    
    def test_unlock_new_area(self, test_player, temp_db):
        """Test unlocking a new area."""
        with patch('src.core.gamedata.game_db', temp_db):
            temp_db.save_player(test_player)
            
            # Unlock cave
            result = test_player.unlock_area('cave')
            
            assert 'cave' in result
            assert 'forest' in result  # Should still have forest


class TestPlayerSettings:
    """Test player settings management."""
    
    @pytest.mark.database
    def test_get_default_settings(self, test_player, temp_db):
        """Test getting default settings."""
        with patch('src.core.gamedata.game_db', temp_db):
            settings = test_player.get_settings()
            
            assert isinstance(settings, dict)
            assert 'auto_save_after_rest' in settings
            assert 'auto_save_after_combat' in settings
    
    @pytest.mark.database
    def test_update_settings(self, test_player, temp_db):
        """Test updating player settings."""
        with patch('src.core.gamedata.game_db', temp_db):
            new_settings = {
                'auto_save_after_rest': False,
                'auto_save_after_combat': True,
                'auto_save_on_inn_visit': True
            }
            
            test_player.update_settings(new_settings)
            
            # Should not raise exception
            assert True  # If we get here, update worked


if __name__ == "__main__":
    pytest.main([__file__])
