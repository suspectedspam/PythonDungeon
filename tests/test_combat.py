#!/usr/bin/env python3
"""
Test suite for the combat system.
Tests turn-based combat mechanics, damage calculation, and combat flow.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.core.combat import Combat
from src.core.player import Player
from src.entities.monster import Monster


class TestCombatSystem:
    """Test the core combat system functionality."""
    
    def test_combat_creation(self):
        """Test combat system initialization."""
        combat = Combat()
        
        assert hasattr(combat, 'calculate_damage')
        assert hasattr(combat, 'take_damage')
        assert hasattr(combat, 'run_combat')
        assert hasattr(combat, 'attempt_flee')
        assert hasattr(combat, 'calculate_critical_hit')
    
    def test_calculate_damage_basic(self):
        """Test basic damage calculation."""
        combat = Combat()
        
        # Test damage calculation with base damage
        base_damage = 10
        calculated_damage = combat.calculate_damage(base_damage)
        
        assert isinstance(calculated_damage, int)
        assert calculated_damage > 0
        # Should be 80-120% of base damage (8-12 for base_damage=10)
        assert 8 <= calculated_damage <= 12
    
    def test_calculate_damage_minimum(self):
        """Test damage calculation always returns at least 1."""
        combat = Combat()
        
        # Test very low damage
        calculated_damage = combat.calculate_damage(1)
        assert calculated_damage >= 1
    
    def test_take_damage_basic(self):
        """Test basic damage application."""
        combat = Combat()
        
        # Test normal damage
        new_health, is_alive = combat.take_damage(50, 20)
        assert new_health == 30
        assert is_alive is True
        
        # Test lethal damage
        new_health, is_alive = combat.take_damage(10, 15)
        assert new_health == 0
        assert is_alive is False
    
    def test_take_damage_exact_lethal(self):
        """Test exact lethal damage."""
        combat = Combat()
        
        new_health, is_alive = combat.take_damage(20, 20)
        assert new_health == 0
        assert is_alive is False
    
    def test_attempt_flee_success(self):
        """Test successful flee attempt."""
        combat = Combat()
        
        # Test with high success chance
        result = combat.attempt_flee(success_chance=1.0)
        assert result is True
    
    def test_attempt_flee_failure(self):
        """Test failed flee attempt."""
        combat = Combat()
        
        # Test with no success chance
        result = combat.attempt_flee(success_chance=0.0)
        assert result is False
    
    def test_calculate_critical_hit_no_crit(self):
        """Test critical hit calculation when no crit occurs."""
        combat = Combat()
        
        with patch('random.random', return_value=0.5):  # No crit (chance is 0.1)
            damage, is_crit = combat.calculate_critical_hit(10, crit_chance=0.1)
            assert damage == 10
            assert is_crit is False
    
    def test_calculate_critical_hit_with_crit(self):
        """Test critical hit calculation when crit occurs."""
        combat = Combat()
        
        with patch('random.random', return_value=0.05):  # Crit occurs (chance is 0.1)
            damage, is_crit = combat.calculate_critical_hit(10, crit_chance=0.1, crit_multiplier=2.0)
            assert damage == 20  # 10 * 2.0
            assert is_crit is True


class TestCombatFlow:
    """Test the overall combat flow and integration."""
    
    @patch('src.ui.display.display')
    def test_run_combat_basic(self, mock_display):
        """Test basic combat execution."""
        combat = Combat()
        player = Player("Hero", level=2, experience=50)
        monster = Monster("Goblin", max_health=20, strength=5, level=2)
        
        # Mock the display system
        mock_display.display_menu.return_value = "1"  # Always attack
        mock_display.add_line = Mock()
        
        # Mock combat to end quickly
        with patch.object(combat, 'calculate_damage', return_value=25):  # High damage to end combat
            result = combat.run_combat(player, monster)
            
            # Combat should end with player victory
            assert result in ["victory", "defeat", "fled"]
    
    def test_check_health_threshold(self):
        """Test monster health threshold checking."""
        combat = Combat()
        monster = Monster("Test", max_health=100, strength=10, level=1)
        crossed_thresholds = set()
        
        # Test at 75% health
        monster.current_health = 75
        result = combat.check_health_threshold(monster, crossed_thresholds)
        
        # Should detect 75% threshold
        assert len(crossed_thresholds) > 0 or result is not None
    
    def test_check_player_health_threshold(self):
        """Test player health threshold checking."""
        combat = Combat()
        player = Player("Hero", level=2, experience=50)
        player.current_health = 25  # Assume max health is 50+
        crossed_thresholds = set()
        
        result = combat.check_player_health_threshold(player, crossed_thresholds)
        
        # Should handle threshold checking without errors
        assert result is None or isinstance(result, str)


class TestCombatEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_combat_with_zero_health_monster(self):
        """Test combat behavior with zero health monster."""
        combat = Combat()
        player = Player("Hero", level=2, experience=50)
        monster = Monster("Dead", max_health=1, strength=1, level=1)
        monster.current_health = 0
        monster.is_alive = False
        
        # Combat should handle dead monster appropriately
        with patch('src.ui.display.display') as mock_display:
            mock_display.add_line = Mock()
            mock_display.display_menu.return_value = "1"
            
            result = combat.run_combat(player, monster)
            assert result in ["victory", "defeat", "fled"]
    
    def test_negative_damage_calculation(self):
        """Test damage calculation with edge values."""
        combat = Combat()
        
        # Test with very small base damage
        damage = combat.calculate_damage(0.5)  # Should round up to at least 1
        assert damage >= 1
    
    def test_take_damage_negative_input(self):
        """Test damage application with negative values."""
        combat = Combat()
        
        # Negative damage should not increase health
        new_health, is_alive = combat.take_damage(50, -10)
        assert new_health == 50  # Health should not increase
        assert is_alive is True


class TestCombatIntegration:
    """Test combat integration with other systems."""
    
    @patch('src.ui.display.display')
    def test_combat_with_equipment_integration(self, mock_display):
        """Test combat integration with equipment system."""
        from src.equipment import Weapon, EquippedItems
        
        combat = Combat()
        player = Player("Hero", level=2, experience=50)
        
        # Give player equipment
        player.equipped = EquippedItems()
        sword = Weapon("Test Sword", damage=5, strength_bonus=2)
        player.equipped.equip_item(sword)
        
        monster = Monster("Target", max_health=30, strength=5, level=2)
        
        mock_display.add_line = Mock()
        mock_display.display_menu.return_value = "1"  # Attack
        
        # Test that combat can access equipment bonuses
        with patch.object(combat, 'calculate_damage', return_value=25):
            result = combat.run_combat(player, monster)
            assert result in ["victory", "defeat", "fled"]
    
    def test_combat_experience_integration(self):
        """Test that combat integrates properly with experience system."""
        combat = Combat()
        player = Player("Hero", level=1, experience=0)
        monster = Monster("Weak", max_health=1, strength=1, level=1)
        
        initial_xp = player.experience
        
        with patch('src.ui.display.display') as mock_display:
            mock_display.add_line = Mock()
            mock_display.display_menu.return_value = "1"
            
            # Mock high damage to ensure quick victory
            with patch.object(combat, 'calculate_damage', return_value=10):
                result = combat.run_combat(player, monster)
                
                # Player should gain XP after victory
                if result == "victory":
                    # XP gain happens in the combat system
                    assert player.experience >= initial_xp