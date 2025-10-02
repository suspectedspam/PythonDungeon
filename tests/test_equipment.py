#!/usr/bin/env python3
"""
Test suite for the equipment system.
Tests equipment classes, inventory management, and equipped items functionality.
"""

import pytest
from src.equipment import Equipment, Weapon, Armor, Accessory, Inventory, EquippedItems
from src.equipment.equipment import EquipmentSlot, create_basic_sword, create_basic_armor, create_basic_ring


class TestEquipmentBaseClass:
    """Test the base Equipment class functionality."""
    
    def test_equipment_creation(self):
        """Test basic equipment creation with all parameters."""
        equipment = Equipment(
            name="Test Item",
            description="A test item",
            level_requirement=5,
            value=100,
            rarity="Rare",
            strength_bonus=2,
            health_bonus=10,
            defense_bonus=3
        )
        
        assert equipment.name == "Test Item"
        assert equipment.description == "A test item"
        assert equipment.level_requirement == 5
        assert equipment.value == 100
        assert equipment.rarity == "Rare"
        assert equipment.strength_bonus == 2
        assert equipment.health_bonus == 10
        assert equipment.defense_bonus == 3
    
    def test_equipment_defaults(self):
        """Test equipment creation with default values."""
        equipment = Equipment("Simple Item")
        
        assert equipment.name == "Simple Item"
        assert equipment.description == ""
        assert equipment.level_requirement == 1
        assert equipment.value == 0
        assert equipment.rarity == "Common"
        assert equipment.strength_bonus == 0
        assert equipment.health_bonus == 0
        assert equipment.defense_bonus == 0
    
    def test_stat_summary_with_bonuses(self):
        """Test stat summary with various bonuses."""
        equipment = Equipment("Stat Item", strength_bonus=5, health_bonus=10, defense_bonus=2)
        summary = equipment.get_stat_summary()
        
        assert "STR: +5" in summary
        assert "HP: +10" in summary
        assert "DEF: +2" in summary
    
    def test_stat_summary_no_bonuses(self):
        """Test stat summary with no bonuses."""
        equipment = Equipment("Plain Item")
        summary = equipment.get_stat_summary()
        
        assert summary == "No stat bonuses"
    
    def test_stat_summary_negative_bonuses(self):
        """Test stat summary with negative bonuses (cursed items)."""
        equipment = Equipment("Cursed Item", strength_bonus=-2, health_bonus=-5)
        summary = equipment.get_stat_summary()
        
        assert "STR: -2" in summary
        assert "HP: -5" in summary
    
    def test_can_equip_level_requirement(self):
        """Test level requirement checking."""
        equipment = Equipment("High Level Item", level_requirement=10)
        
        assert equipment.can_equip(10) is True
        assert equipment.can_equip(15) is True
        assert equipment.can_equip(5) is False
        assert equipment.can_equip(1) is False
    
    def test_string_representation(self):
        """Test equipment string representation."""
        equipment = Equipment("Test Gear", rarity="Epic", strength_bonus=3)
        string_repr = str(equipment)
        
        assert "Test Gear" in string_repr
        assert "Epic" in string_repr
        assert "STR: +3" in string_repr


class TestWeaponClass:
    """Test the Weapon class functionality."""
    
    def test_weapon_creation(self):
        """Test weapon creation with all parameters."""
        weapon = Weapon(
            name="Steel Sword",
            damage=10,
            weapon_type="Sword",
            description="A sharp blade",
            value=50,
            strength_bonus=2
        )
        
        assert weapon.name == "Steel Sword"
        assert weapon.damage == 10
        assert weapon.weapon_type == "Sword"
        assert weapon.description == "A sharp blade"
        assert weapon.value == 50
        assert weapon.strength_bonus == 2
        assert weapon.slot == EquipmentSlot.MAIN_HAND  # Default slot
    
    def test_weapon_slot_management(self):
        """Test weapon slot setting and getting."""
        weapon = Weapon("Dagger", damage=5)
        
        # Test default slot
        assert weapon.get_slot() == EquipmentSlot.MAIN_HAND
        
        # Test setting to off hand
        weapon.set_slot(EquipmentSlot.OFF_HAND)
        assert weapon.get_slot() == EquipmentSlot.OFF_HAND
        
        # Test setting back to main hand
        weapon.set_slot(EquipmentSlot.MAIN_HAND)
        assert weapon.get_slot() == EquipmentSlot.MAIN_HAND
    
    def test_weapon_invalid_slot(self):
        """Test that weapons can't be set to invalid slots."""
        weapon = Weapon("Sword", damage=8)
        
        with pytest.raises(ValueError):
            weapon.set_slot(EquipmentSlot.HEAD)
        
        with pytest.raises(ValueError):
            weapon.set_slot(EquipmentSlot.NECKLACE)
    
    def test_weapon_stat_summary(self):
        """Test weapon-specific stat summary including damage."""
        weapon = Weapon("Magic Sword", damage=12, strength_bonus=3, health_bonus=5)
        summary = weapon.get_stat_summary()
        
        assert "DMG: +12" in summary
        assert "STR: +3" in summary
        assert "HP: +5" in summary
    
    def test_weapon_damage_only(self):
        """Test weapon with only damage bonus."""
        weapon = Weapon("Simple Blade", damage=7)
        summary = weapon.get_stat_summary()
        
        assert summary == "DMG: +7"


class TestArmorClass:
    """Test the Armor class functionality."""
    
    def test_armor_creation(self):
        """Test armor creation for different slots."""
        helmet = Armor("Iron Helmet", "Iron", EquipmentSlot.HEAD, defense_bonus=5, value=30)
        
        assert helmet.name == "Iron Helmet"
        assert helmet.armor_type == "Iron"
        assert helmet.slot == EquipmentSlot.HEAD
        assert helmet.defense_bonus == 5
        assert helmet.value == 30
    
    def test_armor_valid_slots(self):
        """Test armor creation for all valid armor slots."""
        valid_slots = [
            EquipmentSlot.HEAD,
            EquipmentSlot.BODY, 
            EquipmentSlot.LEGS,
            EquipmentSlot.HANDS,
            EquipmentSlot.FEET
        ]
        
        for slot in valid_slots:
            armor = Armor(f"Test {slot.value}", "Leather", slot)
            assert armor.get_slot() == slot
    
    def test_armor_invalid_slots(self):
        """Test that armor can't be created for invalid slots."""
        invalid_slots = [
            EquipmentSlot.MAIN_HAND,
            EquipmentSlot.OFF_HAND,
            EquipmentSlot.NECKLACE,
            EquipmentSlot.RING_1,
            EquipmentSlot.RING_2
        ]
        
        for slot in invalid_slots:
            with pytest.raises(ValueError):
                Armor("Invalid Armor", "Leather", slot)


class TestAccessoryClass:
    """Test the Accessory class functionality."""
    
    def test_accessory_creation(self):
        """Test accessory creation for different types."""
        necklace = Accessory("Gold Amulet", "Amulet", EquipmentSlot.NECKLACE, 
                           strength_bonus=2, value=75, rarity="Uncommon")
        
        assert necklace.name == "Gold Amulet"
        assert necklace.accessory_type == "Amulet"
        assert necklace.slot == EquipmentSlot.NECKLACE
        assert necklace.strength_bonus == 2
        assert necklace.value == 75
        assert necklace.rarity == "Uncommon"
    
    def test_accessory_valid_slots(self):
        """Test accessory creation for all valid accessory slots."""
        valid_slots = [
            EquipmentSlot.NECKLACE,
            EquipmentSlot.RING_1,
            EquipmentSlot.RING_2
        ]
        
        for slot in valid_slots:
            accessory = Accessory(f"Test {slot.value}", "Ring", slot)
            assert accessory.get_slot() == slot
    
    def test_accessory_invalid_slots(self):
        """Test that accessories can't be created for invalid slots."""
        invalid_slots = [
            EquipmentSlot.MAIN_HAND,
            EquipmentSlot.HEAD,
            EquipmentSlot.BODY,
            EquipmentSlot.LEGS,
            EquipmentSlot.HANDS,
            EquipmentSlot.FEET
        ]
        
        for slot in invalid_slots:
            with pytest.raises(ValueError):
                Accessory("Invalid Accessory", "Ring", slot)


class TestEquipmentFactories:
    """Test the equipment factory functions."""
    
    def test_create_basic_sword(self):
        """Test basic sword creation."""
        sword = create_basic_sword()
        
        assert isinstance(sword, Weapon)
        assert sword.name == "Iron Sword"
        assert sword.damage == 5
        assert sword.weapon_type == "Sword"
        assert sword.rarity == "Common"
    
    def test_create_basic_armor(self):
        """Test basic armor set creation."""
        armor_set = create_basic_armor()
        
        assert isinstance(armor_set, dict)
        assert 'head' in armor_set
        assert 'body' in armor_set
        assert 'legs' in armor_set
        
        # Test individual pieces
        helmet = armor_set['head']
        assert isinstance(helmet, Armor)
        assert helmet.slot == EquipmentSlot.HEAD
        assert helmet.armor_type == "Leather"
    
    def test_create_basic_ring(self):
        """Test basic ring creation."""
        ring = create_basic_ring()
        
        assert isinstance(ring, Accessory)
        assert ring.name == "Simple Band"
        assert ring.accessory_type == "Ring"
        assert ring.slot == EquipmentSlot.RING_1
        assert ring.rarity == "Common"


class TestInventoryClass:
    """Test the Inventory management system."""
    
    def test_inventory_creation(self):
        """Test inventory creation with custom capacity."""
        inventory = Inventory(max_capacity=10)
        
        assert inventory.max_capacity == 10
        assert inventory.get_count() == 0
        assert inventory.is_empty() is True
        assert inventory.is_full() is False
    
    def test_inventory_default_capacity(self):
        """Test inventory creation with default capacity."""
        inventory = Inventory()
        
        assert inventory.max_capacity == 50
    
    def test_add_item_success(self):
        """Test adding items to inventory."""
        inventory = Inventory(max_capacity=5)
        sword = create_basic_sword()
        
        success, message = inventory.add_item(sword)
        
        assert success is True
        assert "Added Iron Sword to inventory" in message
        assert inventory.get_count() == 1
        assert inventory.is_empty() is False
    
    def test_add_item_capacity_full(self):
        """Test adding items when inventory is full."""
        inventory = Inventory(max_capacity=1)
        sword1 = create_basic_sword()
        sword2 = Weapon("Second Sword", damage=3)
        
        # Add first item
        success1, _ = inventory.add_item(sword1)
        assert success1 is True
        assert inventory.is_full() is True
        
        # Try to add second item
        success2, message = inventory.add_item(sword2)
        assert success2 is False
        assert "Inventory full!" in message
    
    def test_remove_item(self):
        """Test removing specific items from inventory."""
        inventory = Inventory()
        sword = create_basic_sword()
        
        inventory.add_item(sword)
        assert inventory.get_count() == 1
        
        removed = inventory.remove_item(sword)
        assert removed is True
        assert inventory.get_count() == 0
        assert inventory.is_empty() is True
    
    def test_remove_item_not_found(self):
        """Test removing item that's not in inventory."""
        inventory = Inventory()
        sword = create_basic_sword()
        
        removed = inventory.remove_item(sword)
        assert removed is False
    
    def test_remove_item_by_name(self):
        """Test removing items by name."""
        inventory = Inventory()
        sword = create_basic_sword()
        inventory.add_item(sword)
        
        removed_item = inventory.remove_item_by_name("Iron Sword")
        assert removed_item == sword
        assert inventory.get_count() == 0
    
    def test_remove_item_by_name_not_found(self):
        """Test removing item by name when not found."""
        inventory = Inventory()
        
        removed_item = inventory.remove_item_by_name("Nonexistent Sword")
        assert removed_item is None
    
    def test_get_item_by_name(self):
        """Test getting items by name without removing."""
        inventory = Inventory()
        sword = create_basic_sword()
        inventory.add_item(sword)
        
        found_item = inventory.get_item_by_name("Iron Sword")
        assert found_item == sword
        assert inventory.get_count() == 1  # Item still in inventory
    
    def test_get_item_by_index(self):
        """Test getting items by index position."""
        inventory = Inventory()
        sword = create_basic_sword()
        ring = create_basic_ring()
        
        inventory.add_item(sword)
        inventory.add_item(ring)
        
        # Test 1-based indexing
        first_item = inventory.get_item_by_index(1)
        second_item = inventory.get_item_by_index(2)
        invalid_item = inventory.get_item_by_index(3)
        
        assert first_item == sword
        assert second_item == ring
        assert invalid_item is None
    
    def test_get_items_by_type(self):
        """Test filtering items by type."""
        inventory = Inventory()
        sword = create_basic_sword()
        ring = create_basic_ring()
        armor_set = create_basic_armor()
        
        inventory.add_item(sword)
        inventory.add_item(ring)
        inventory.add_item(armor_set['head'])
        
        weapons = inventory.get_items_by_type(Weapon)
        accessories = inventory.get_items_by_type(Accessory)
        armor_pieces = inventory.get_items_by_type(Armor)
        
        assert len(weapons) == 1
        assert sword in weapons
        assert len(accessories) == 1
        assert ring in accessories
        assert len(armor_pieces) == 1
    
    def test_sort_items(self):
        """Test inventory sorting by different criteria."""
        inventory = Inventory()
        
        # Add items with different values and names
        cheap_sword = Weapon("A-Sword", damage=1, value=10)
        expensive_sword = Weapon("Z-Sword", damage=5, value=100)
        
        inventory.add_item(expensive_sword)
        inventory.add_item(cheap_sword)
        
        # Test sort by name
        inventory.sort_items("name")
        assert inventory.items[0] == cheap_sword
        assert inventory.items[1] == expensive_sword
        
        # Test sort by value
        inventory.sort_items("value")
        assert inventory.items[0] == expensive_sword
        assert inventory.items[1] == cheap_sword
    
    def test_get_total_value(self):
        """Test calculating total inventory value."""
        inventory = Inventory()
        sword = Weapon("Sword", damage=5, value=50)
        ring = Accessory("Ring", "Ring", EquipmentSlot.RING_1, value=25)
        
        inventory.add_item(sword)
        inventory.add_item(ring)
        
        assert inventory.get_total_value() == 75
    
    def test_inventory_display(self):
        """Test inventory display formatting."""
        inventory = Inventory()
        
        # Test empty inventory
        display = inventory.get_inventory_display()
        assert "Inventory is empty" in display
        
        # Test with items
        sword = create_basic_sword()
        inventory.add_item(sword)
        
        display = inventory.get_inventory_display()
        assert "INVENTORY" in display
        assert "Iron Sword" in display
        assert "1/50" in display  # Capacity display


class TestEquippedItemsClass:
    """Test the EquippedItems management system."""
    
    def test_equipped_items_creation(self):
        """Test equipped items initialization."""
        equipped = EquippedItems()
        
        # Test all slots are empty initially
        for slot in EquipmentSlot:
            assert equipped.is_slot_empty(slot) is True
            assert equipped.get_equipped_item(slot) is None
    
    def test_equip_weapon_main_hand(self):
        """Test equipping a weapon to main hand."""
        equipped = EquippedItems()
        sword = create_basic_sword()
        
        success, message, old_item = equipped.equip_item(sword)
        
        assert success is True
        assert "Equipped Iron Sword to Main Hand" in message
        assert old_item is None
        assert equipped.get_equipped_item(EquipmentSlot.MAIN_HAND) == sword
    
    def test_equip_weapon_off_hand(self):
        """Test equipping a weapon to off hand."""
        equipped = EquippedItems()
        dagger = Weapon("Dagger", damage=3)
        dagger.set_slot(EquipmentSlot.OFF_HAND)
        
        success, message, old_item = equipped.equip_item(dagger)
        
        assert success is True
        assert "Off Hand" in message
        assert equipped.get_equipped_item(EquipmentSlot.OFF_HAND) == dagger
    
    def test_equip_armor_pieces(self):
        """Test equipping different armor pieces."""
        equipped = EquippedItems()
        armor_set = create_basic_armor()
        
        for armor_piece in armor_set.values():
            success, message, old_item = equipped.equip_item(armor_piece)
            assert success is True
            assert old_item is None
    
    def test_equip_rings(self):
        """Test equipping rings to different ring slots."""
        equipped = EquippedItems()
        
        ring1 = Accessory("Ring 1", "Ring", EquipmentSlot.RING_1, strength_bonus=1)
        ring2 = Accessory("Ring 2", "Ring", EquipmentSlot.RING_2, health_bonus=5)
        
        # Equip first ring
        success1, message1, _ = equipped.equip_item(ring1)
        assert success1 is True
        assert "Ring 1" in message1
        
        # Equip second ring
        success2, message2, _ = equipped.equip_item(ring2)
        assert success2 is True
        assert "Ring 2" in message2
        
        # Check both rings are equipped
        assert equipped.get_equipped_item(EquipmentSlot.RING_1) == ring1
        assert equipped.get_equipped_item(EquipmentSlot.RING_2) == ring2
    
    def test_equip_replace_existing(self):
        """Test replacing an already equipped item."""
        equipped = EquippedItems()
        
        sword1 = Weapon("Iron Sword", damage=5)
        sword2 = Weapon("Steel Sword", damage=8)
        
        # Equip first sword
        equipped.equip_item(sword1)
        
        # Equip second sword (should replace first)
        success, message, old_item = equipped.equip_item(sword2)
        
        assert success is True
        assert old_item == sword1
        assert equipped.get_equipped_item(EquipmentSlot.MAIN_HAND) == sword2
    
    def test_unequip_slot(self):
        """Test unequipping items from slots."""
        equipped = EquippedItems()
        sword = create_basic_sword()
        
        # Equip and then unequip
        equipped.equip_item(sword)
        unequipped_item = equipped.unequip_slot(EquipmentSlot.MAIN_HAND)
        
        assert unequipped_item == sword
        assert equipped.is_slot_empty(EquipmentSlot.MAIN_HAND) is True
    
    def test_get_all_equipped(self):
        """Test getting all equipped items."""
        equipped = EquippedItems()
        
        sword = create_basic_sword()
        helmet = Armor("Helmet", "Iron", EquipmentSlot.HEAD, defense_bonus=3)
        
        equipped.equip_item(sword)
        equipped.equip_item(helmet)
        
        all_equipped = equipped.get_all_equipped()
        
        assert len(all_equipped) == 2
        assert EquipmentSlot.MAIN_HAND in all_equipped
        assert EquipmentSlot.HEAD in all_equipped
        assert all_equipped[EquipmentSlot.MAIN_HAND] == sword
        assert all_equipped[EquipmentSlot.HEAD] == helmet
    
    def test_get_total_stat_bonuses(self):
        """Test calculating total stat bonuses from all equipment."""
        equipped = EquippedItems()
        
        sword = Weapon("Magic Sword", damage=10, strength_bonus=3)
        helmet = Armor("Magic Helmet", "Mithril", EquipmentSlot.HEAD, 
                      defense_bonus=5, health_bonus=10)
        ring = Accessory("Power Ring", "Ring", EquipmentSlot.RING_1, strength_bonus=2)
        
        equipped.equip_item(sword)
        equipped.equip_item(helmet)
        equipped.equip_item(ring)
        
        totals = equipped.get_total_stat_bonuses()
        
        assert totals['damage'] == 10
        assert totals['strength'] == 5  # 3 + 2
        assert totals['health'] == 10
        assert totals['defense'] == 5
    
    def test_equipment_display(self):
        """Test equipment display formatting."""
        equipped = EquippedItems()
        
        # Test empty display
        display = equipped.get_equipment_display()
        assert "EQUIPPED ITEMS" in display
        assert "(empty)" in display
        
        # Test with equipped items
        sword = create_basic_sword()
        equipped.equip_item(sword)
        
        display = equipped.get_equipment_display()
        assert "Iron Sword" in display
        assert "TOTAL BONUSES" in display