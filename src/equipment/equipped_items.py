#!/usr/bin/env python3
"""
Equipment management system for PythonDungeon
Handles what equipment is currently equipped by the player.
"""

from .equipment import EquipmentSlot

class EquippedItems:
    """Manages all currently equipped items for a player."""
    
    def __init__(self):
        """Initialize empty equipment slots."""
        # Dictionary mapping slots to equipped items (None if empty)
        self.slots = {
            EquipmentSlot.MAIN_HAND: None,
            EquipmentSlot.OFF_HAND: None,
            EquipmentSlot.HEAD: None,
            EquipmentSlot.BODY: None,
            EquipmentSlot.LEGS: None,
            EquipmentSlot.HANDS: None,
            EquipmentSlot.FEET: None,
            EquipmentSlot.NECKLACE: None,
            EquipmentSlot.RING_1: None,
            EquipmentSlot.RING_2: None,
        }
    
    def equip_item(self, item, preferred_slot=None):
        """
        Equip an item to the appropriate slot.
        
        Args:
            item: Equipment item to equip
            preferred_slot: Preferred slot (useful for rings and weapons)
            
        Returns:
            tuple: (success: bool, message: str, unequipped_item: Equipment or None)
        """
        # Determine which slot to use
        if hasattr(item, 'get_slot'):
            target_slot = item.get_slot()
        else:
            return False, "Invalid equipment item", None
        
        # Handle special cases for items that can go in multiple slots
        if preferred_slot:
            if self._is_valid_slot_for_item(item, preferred_slot):
                target_slot = preferred_slot
                # Update item's slot if it's a weapon or ring
                if hasattr(item, 'set_slot'):
                    item.set_slot(preferred_slot)
        
        # Handle rings - find available ring slot
        if target_slot in [EquipmentSlot.RING_1, EquipmentSlot.RING_2]:
            target_slot = self._find_available_ring_slot(preferred_slot)
            if not target_slot:
                return False, "No available ring slots", None
        
        # Store what was previously equipped
        previously_equipped = self.slots[target_slot]
        
        # Equip the new item
        self.slots[target_slot] = item
        
        slot_name = target_slot.value.replace('_', ' ').title()
        return True, f"Equipped {item.name} to {slot_name}", previously_equipped
    
    def unequip_slot(self, slot):
        """
        Unequip item from a specific slot.
        
        Args:
            slot (EquipmentSlot): Slot to unequip
            
        Returns:
            Equipment or None: The unequipped item, if any
        """
        unequipped_item = self.slots[slot]
        self.slots[slot] = None
        return unequipped_item
    
    def get_equipped_item(self, slot):
        """Get the item equipped in a specific slot."""
        return self.slots[slot]
    
    def get_all_equipped(self):
        """Get dictionary of all equipped items (excluding empty slots)."""
        return {slot: item for slot, item in self.slots.items() if item is not None}
    
    def is_slot_empty(self, slot):
        """Check if a slot is empty."""
        return self.slots[slot] is None
    
    def get_total_stat_bonuses(self):
        """
        Calculate total stat bonuses from all equipped items.
        
        Returns:
            dict: Dictionary with 'strength', 'health', 'defense', 'damage' totals
        """
        totals = {
            'strength': 0,
            'health': 0,
            'defense': 0,
            'damage': 0
        }
        
        for item in self.slots.values():
            if item is not None:
                totals['strength'] += getattr(item, 'strength_bonus', 0)
                totals['health'] += getattr(item, 'health_bonus', 0)
                totals['defense'] += getattr(item, 'defense_bonus', 0)
                totals['damage'] += getattr(item, 'damage', 0)
        
        return totals
    
    def _is_valid_slot_for_item(self, item, slot):
        """Check if an item can be equipped in a specific slot."""
        # Weapons can go in main_hand or off_hand
        if hasattr(item, 'damage') and slot in [EquipmentSlot.MAIN_HAND, EquipmentSlot.OFF_HAND]:
            return True
        
        # Rings can go in either ring slot
        if hasattr(item, 'accessory_type') and item.accessory_type == "Ring":
            return slot in [EquipmentSlot.RING_1, EquipmentSlot.RING_2]
        
        # Other items must match their designated slot
        return hasattr(item, 'get_slot') and item.get_slot() == slot
    
    def _find_available_ring_slot(self, preferred_slot=None):
        """Find an available ring slot, preferring the specified one."""
        if preferred_slot in [EquipmentSlot.RING_1, EquipmentSlot.RING_2]:
            if self.is_slot_empty(preferred_slot):
                return preferred_slot
        
        # Try ring slots in order
        for slot in [EquipmentSlot.RING_1, EquipmentSlot.RING_2]:
            if self.is_slot_empty(slot):
                return slot
        
        return None  # No available ring slots
    
    def get_equipment_display(self):
        """
        Get a formatted display of all equipment slots.
        
        Returns:
            str: Formatted equipment display
        """
        display_lines = []
        display_lines.append("=== EQUIPPED ITEMS ===")
        
        # Define display order and names
        slot_display = [
            (EquipmentSlot.MAIN_HAND, "Main Hand"),
            (EquipmentSlot.OFF_HAND, "Off Hand"),
            (EquipmentSlot.HEAD, "Head"),
            (EquipmentSlot.BODY, "Body"),
            (EquipmentSlot.LEGS, "Legs"),
            (EquipmentSlot.HANDS, "Hands"),
            (EquipmentSlot.FEET, "Feet"),
            (EquipmentSlot.NECKLACE, "Necklace"),
            (EquipmentSlot.RING_1, "Ring 1"),
            (EquipmentSlot.RING_2, "Ring 2"),
        ]
        
        for slot, display_name in slot_display:
            item = self.slots[slot]
            if item:
                display_lines.append(f"{display_name:10}: {item.name}")
            else:
                display_lines.append(f"{display_name:10}: (empty)")
        
        # Add stat summary
        stats = self.get_total_stat_bonuses()
        display_lines.append("")
        display_lines.append("=== TOTAL BONUSES ===")
        display_lines.append(f"Damage:   +{stats['damage']}")
        display_lines.append(f"Strength: +{stats['strength']}")
        display_lines.append(f"Health:   +{stats['health']}")
        display_lines.append(f"Defense:  +{stats['defense']}")
        
        return "\n".join(display_lines)