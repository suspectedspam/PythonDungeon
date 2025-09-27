"""
Unit tests for Adventure system
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.locations.adventure import Adventure
from src.locations.forest import Forest


class TestAdventureBaseClass:
    """Test the Adventure abstract base class."""
    
    def test_cannot_instantiate_adventure_directly(self):
        """Test that Adventure abstract class cannot be instantiated."""
        with pytest.raises(TypeError):
            Adventure()
    
    def test_forest_inherits_from_adventure(self, forest_adventure):
        """Test that Forest properly inherits from Adventure."""
        assert isinstance(forest_adventure, Adventure)
    
    def test_adventure_class_methods_exist(self):
        """Test that Adventure class has required class methods."""
        assert hasattr(Adventure, '_load_adventures')
        assert hasattr(Adventure, 'get_available_adventures')
        assert hasattr(Adventure, 'show_adventure_selection_menu')
        assert hasattr(Adventure, 'start_adventure_by_key')


class TestForestAdventure:
    """Test the Forest adventure implementation."""
    
    def test_forest_creation(self, forest_adventure):
        """Test Forest adventure can be created."""
        assert forest_adventure is not None
        assert hasattr(forest_adventure, 'combat')
        assert forest_adventure.encounter_rate == 0.8
    
    def test_forest_abstract_methods(self, forest_adventure):
        """Test Forest implements all required abstract methods."""
        assert forest_adventure.get_location_name() == "Forest"
        assert forest_adventure.get_location_emoji() == "🌲"
        assert isinstance(forest_adventure.get_location_intro(), str)
        assert isinstance(forest_adventure.get_peaceful_events(), list)
        assert len(forest_adventure.get_peaceful_events()) > 0
    
    def test_forest_encounter_rate(self, forest_adventure):
        """Test Forest encounter rate can be modified."""
        forest_adventure.set_encounter_rate(0.5)
        assert forest_adventure.encounter_rate == 0.5
        
        # Test bounds
        forest_adventure.set_encounter_rate(-0.1)
        assert forest_adventure.encounter_rate == 0.0
        
        forest_adventure.set_encounter_rate(1.5)
        assert forest_adventure.encounter_rate == 1.0
    
    def test_create_forest_monster(self, forest_adventure):
        """Test Forest can create monsters."""
        # Since Monster is imported inside the method, we need to patch the import
        with patch('src.entities.monster.Monster') as mock_monster_class:
            # Create a mock monster instance
            mock_monster = Mock()
            mock_monster.name = "Forest Wolf"
            mock_monster.level = 1
            mock_monster.emoji = "🐺"
            
            # Mock the class method that gets called
            mock_monster_class.create_random_for_level.return_value = mock_monster
            
            # Test monster creation
            monster = forest_adventure.create_location_monster(1)
            
            # Verify the monster was created correctly
            assert monster is not None
            assert monster == mock_monster
            
            # Verify the correct method was called with correct parameters
            mock_monster_class.create_random_for_level.assert_called_once_with(1)


class TestAdventureLoading:
    """Test adventure loading and management."""
    
    def test_load_adventures_includes_forest(self):
        """Test that _load_adventures includes Forest."""
        adventures = Adventure._load_adventures()
        
        assert 'forest' in adventures
        assert adventures['forest'] == Forest
    
    def test_get_available_adventures_without_player(self):
        """Test getting available adventures without player restrictions."""
        adventures = Adventure.get_available_adventures(player=None)
        
        assert isinstance(adventures, list)
        assert len(adventures) > 0
        
        # Should include forest
        forest_found = False
        for key, name, emoji in adventures:
            if key == 'forest':
                assert name == "Forest"
                assert emoji == "🌲"
                forest_found = True
        
        assert forest_found, "Forest should be in available adventures"
    
    @patch('src.locations.adventure.Adventure._load_adventures')
    def test_get_available_adventures_with_player(self, mock_load, test_player):
        """Test getting available adventures filtered by player unlocked areas."""
        # Mock the adventures loading
        mock_load.return_value = {'forest': Forest, 'cave': Mock}
        
        # Mock player unlocked areas
        with patch.object(test_player, 'get_unlocked_areas', return_value=['forest']):
            adventures = Adventure.get_available_adventures(test_player)
            
            # Should only include forest (player's unlocked area)
            assert len(adventures) == 1
            key, name, emoji = adventures[0]
            assert key == 'forest'
            assert name == "Forest"
            assert emoji == "🌲"


class TestAdventureSelectionMenu:
    """Test adventure selection menu functionality."""
    
    def test_show_adventure_selection_menu_no_adventures(self, test_player, mock_display):
        """Test menu when no adventures are available."""
        with patch.object(Adventure, 'get_available_adventures', return_value=[]):
            result = Adventure.show_adventure_selection_menu(test_player)
            
            assert result == "cancelled"
            mock_display.add_line.assert_called_with("❌ No adventures are currently available!")
    
    def test_show_adventure_selection_menu_with_adventures(self, test_player, mock_display):
        """Test menu with available adventures."""
        mock_adventures = [('forest', 'Forest', '🌲')]
        
        with patch.object(Adventure, 'get_available_adventures', return_value=mock_adventures):
            # Mock user selecting "Return to Inn" (option 2)
            mock_display.display_menu.return_value = "2"
            
            result = Adventure.show_adventure_selection_menu(test_player)
            
            assert result == "cancelled"
            mock_display.add_line.assert_called_with("🏠 You decide to stay at the inn for now.")
    
    def test_start_adventure_by_key_valid(self, test_player):
        """Test starting adventure with valid key."""
        with patch.object(Adventure, '_load_adventures', return_value={'forest': Forest}):
            with patch.object(Forest, 'start_adventure', return_value="returned") as mock_start:
                result = Adventure.start_adventure_by_key('forest', test_player)
                
                assert result == "returned"
                mock_start.assert_called_once_with(test_player)
    
    def test_start_adventure_by_key_invalid(self, test_player):
        """Test starting adventure with invalid key."""
        with patch.object(Adventure, '_load_adventures', return_value={'forest': Forest}):
            with pytest.raises(ValueError, match="Adventure 'invalid' not found"):
                Adventure.start_adventure_by_key('invalid', test_player)


@pytest.mark.integration
class TestAdventureIntegration:
    """Integration tests for the adventure system."""
    
    def test_full_adventure_flow(self, test_player, mock_display, mock_input):
        """Test complete adventure selection and execution flow."""
        # Mock the forest adventure to return quickly
        with patch.object(Forest, 'start_adventure', return_value="returned"):
            # Mock user selecting forest (option 1)
            mock_display.display_menu.return_value = "1"
            
            result = Adventure.show_adventure_selection_menu(test_player)
            
            assert result == "returned"
    
    @pytest.mark.slow
    def test_adventure_with_mock_combat(self, test_player, forest_adventure):
        """Test adventure with mocked combat system."""
        with patch.object(forest_adventure, 'monster_encounter', return_value="victory"):
            with patch.object(forest_adventure, 'ask_continue_adventure', return_value="return"):
                with patch('random.random', return_value=0.5):  # Force encounter
                    result = forest_adventure.start_adventure(test_player)
                    
                    assert result == "returned"


if __name__ == "__main__":
    pytest.main([__file__])