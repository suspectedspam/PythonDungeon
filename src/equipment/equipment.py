#!/usr/bin/env python3
"""
Equipment classes for PythonDungeon
Defines base equipment and specific equipment types (weapons, armor, accessories).
"""

from enum import Enum

class EquipmentSlot(Enum):
    """Defines all available equipment slots."""
    MAIN_HAND = "main_hand"
    OFF_HAND = "off_hand"
    HEAD = "head"
    BODY = "body"
    LEGS = "legs"
    HANDS = "hands"
    FEET = "feet"
    NECKLACE = "necklace"
    RING_1 = "ring_1"
    RING_2 = "ring_2"

class Equipment:
    """Base equipment class that all items inherit from."""
    
    def __init__(self, name, description="", level_requirement=1, value=0, rarity="Common", 
                 strength_bonus=0, health_bonus=0, defense_bonus=0):
        """
        Initialize base equipment.
        
        Args:
            name (str): Equipment name
            description (str): Equipment description
            level_requirement (int): Minimum level to equip
            value (int): Gold value of the item
            rarity (str): Rarity tier (Common, Uncommon, Rare, Epic, Legendary)
            strength_bonus (int): Strength stat bonus
            health_bonus (int): Health stat bonus
            defense_bonus (int): Defense stat bonus
        """
        self.name = name
        self.description = description
        self.level_requirement = level_requirement
        self.value = value
        self.rarity = rarity
        
        # Stats bonuses (can be negative for cursed items)
        self.strength_bonus = strength_bonus
        self.health_bonus = health_bonus
        self.defense_bonus = defense_bonus
        
    def get_stat_summary(self):
        """Get a formatted string of all stat bonuses."""
        bonuses = []
        if self.strength_bonus != 0:
            bonuses.append(f"STR: {self.strength_bonus:+d}")
        if self.health_bonus != 0:
            bonuses.append(f"HP: {self.health_bonus:+d}")
        if self.defense_bonus != 0:
            bonuses.append(f"DEF: {self.defense_bonus:+d}")
        
        return " | ".join(bonuses) if bonuses else "No stat bonuses"
    
    def can_equip(self, player_level):
        """Check if player can equip this item."""
        return player_level >= self.level_requirement
    
    def __str__(self):
        """String representation of the equipment."""
        stats = self.get_stat_summary()
        return f"{self.name} ({self.rarity}) - {stats}"

class Weapon(Equipment):
    """Weapon equipment that can be equipped in main hand or off hand."""
    
    def __init__(self, name, damage, weapon_type="Sword", **kwargs):
        """
        Initialize weapon.
        
        Args:
            name (str): Weapon name
            damage (int): Base damage bonus
            weapon_type (str): Type of weapon (Sword, Axe, Bow, etc.)
            **kwargs: Additional Equipment parameters
        """
        super().__init__(name, **kwargs)
        self.damage = damage
        self.weapon_type = weapon_type
        self.slot = EquipmentSlot.MAIN_HAND  # Default slot
    
    def get_slot(self):
        """Get the equipment slot this weapon uses."""
        return self.slot
    
    def set_slot(self, slot):
        """Set which slot this weapon should use (main_hand or off_hand)."""
        if slot in [EquipmentSlot.MAIN_HAND, EquipmentSlot.OFF_HAND]:
            self.slot = slot
        else:
            raise ValueError("Weapons can only be equipped in main_hand or off_hand")
    
    def get_stat_summary(self):
        """Get weapon-specific stat summary."""
        base_stats = super().get_stat_summary()
        weapon_stats = f"DMG: +{self.damage}"
        
        if base_stats != "No stat bonuses":
            return f"{weapon_stats} | {base_stats}"
        return weapon_stats

class Armor(Equipment):
    """Armor equipment for various body slots."""
    
    def __init__(self, name, armor_type, slot, **kwargs):
        """
        Initialize armor.
        
        Args:
            name (str): Armor name
            armor_type (str): Type of armor (Leather, Chain, Plate, etc.)
            slot (EquipmentSlot): Which slot this armor fits
            **kwargs: Additional Equipment parameters
        """
        super().__init__(name, **kwargs)
        self.armor_type = armor_type
        self.slot = slot
        
        # Validate slot is appropriate for armor
        valid_armor_slots = [
            EquipmentSlot.HEAD, EquipmentSlot.BODY, EquipmentSlot.LEGS, 
            EquipmentSlot.HANDS, EquipmentSlot.FEET
        ]
        if slot not in valid_armor_slots:
            raise ValueError(f"Invalid armor slot: {slot}")
    
    def get_slot(self):
        """Get the equipment slot this armor uses."""
        return self.slot

class Accessory(Equipment):
    """Accessories like necklaces and rings."""
    
    def __init__(self, name, accessory_type, slot, **kwargs):
        """
        Initialize accessory.
        
        Args:
            name (str): Accessory name
            accessory_type (str): Type (Necklace, Ring, Amulet, etc.)
            slot (EquipmentSlot): Which slot this accessory fits
            **kwargs: Additional Equipment parameters
        """
        super().__init__(name, **kwargs)
        self.accessory_type = accessory_type
        self.slot = slot
        
        # Validate slot is appropriate for accessories
        valid_accessory_slots = [
            EquipmentSlot.NECKLACE, EquipmentSlot.RING_1, EquipmentSlot.RING_2
        ]
        if slot not in valid_accessory_slots:
            raise ValueError(f"Invalid accessory slot: {slot}")
    
    def get_slot(self):
        """Get the equipment slot this accessory uses."""
        return self.slot

# Example equipment factory functions
def create_basic_sword():
    """Create a basic starting sword."""
    return Weapon(
        name="Iron Sword",
        damage=5,
        weapon_type="Sword",
        description="A sturdy iron blade, perfect for beginners.",
        level_requirement=1,
        value=25,
        rarity="Common"
    )

def create_basic_armor():
    """Create basic starting armor set."""
    return {
        'head': Armor("Leather Cap", "Leather", EquipmentSlot.HEAD, 
                     defense_bonus=1, value=10, description="Simple leather headwear."),
        'body': Armor("Leather Tunic", "Leather", EquipmentSlot.BODY, 
                     defense_bonus=3, value=20, description="Basic leather protection."),
        'legs': Armor("Leather Pants", "Leather", EquipmentSlot.LEGS, 
                     defense_bonus=2, value=15, description="Flexible leather legwear.")
    }

def create_basic_ring():
    """Create a basic ring."""
    return Accessory(
        name="Simple Band",
        accessory_type="Ring",
        slot=EquipmentSlot.RING_1,  # Can be changed when equipped
        description="A plain metal ring.",
        value=5,
        rarity="Common"
    )