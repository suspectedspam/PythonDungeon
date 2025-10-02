#!/usr/bin/env python3
"""
Inventory management system for PythonDungeon
Handles storage and management of unequipped items.
"""

class Inventory:
    """Manages player's inventory of unequipped items."""
    
    def __init__(self, max_capacity=50):
        """
        Initialize inventory.
        
        Args:
            max_capacity (int): Maximum number of items that can be stored
        """
        self.items = []
        self.max_capacity = max_capacity
    
    def add_item(self, item):
        """
        Add an item to the inventory.
        
        Args:
            item: Equipment item to add
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if len(self.items) >= self.max_capacity:
            return False, f"Inventory full! (Max {self.max_capacity} items)"
        
        self.items.append(item)
        return True, f"Added {item.name} to inventory"
    
    def remove_item(self, item):
        """
        Remove a specific item from inventory.
        
        Args:
            item: Equipment item to remove
            
        Returns:
            bool: True if item was found and removed
        """
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def remove_item_by_name(self, name):
        """
        Remove the first item with matching name.
        
        Args:
            name (str): Name of item to remove
            
        Returns:
            Equipment or None: The removed item, if found
        """
        for item in self.items:
            if item.name.lower() == name.lower():
                self.items.remove(item)
                return item
        return None
    
    def get_item_by_name(self, name):
        """
        Get the first item with matching name (without removing).
        
        Args:
            name (str): Name of item to find
            
        Returns:
            Equipment or None: The found item
        """
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None
    
    def get_items_by_type(self, equipment_type):
        """
        Get all items of a specific type.
        
        Args:
            equipment_type: Equipment class type (Weapon, Armor, Accessory)
            
        Returns:
            list: List of matching items
        """
        return [item for item in self.items if isinstance(item, equipment_type)]
    
    def is_full(self):
        """Check if inventory is at capacity."""
        return len(self.items) >= self.max_capacity
    
    def is_empty(self):
        """Check if inventory is empty."""
        return len(self.items) == 0
    
    def get_count(self):
        """Get current number of items in inventory."""
        return len(self.items)
    
    def get_capacity_string(self):
        """Get formatted capacity string."""
        return f"{self.get_count()}/{self.max_capacity}"
    
    def sort_items(self, sort_by="name"):
        """
        Sort inventory items.
        
        Args:
            sort_by (str): Sort criteria ("name", "value", "level", "rarity")
        """
        if sort_by == "name":
            self.items.sort(key=lambda x: x.name.lower())
        elif sort_by == "value":
            self.items.sort(key=lambda x: x.value, reverse=True)
        elif sort_by == "level":
            self.items.sort(key=lambda x: x.level_requirement, reverse=True)
        elif sort_by == "rarity":
            rarity_order = {"Common": 1, "Uncommon": 2, "Rare": 3, "Epic": 4, "Legendary": 5}
            self.items.sort(key=lambda x: rarity_order.get(x.rarity, 0), reverse=True)
    
    def get_total_value(self):
        """Calculate total gold value of all items in inventory."""
        return sum(item.value for item in self.items)
    
    def get_inventory_display(self, show_stats=True):
        """
        Get formatted inventory display.
        
        Args:
            show_stats (bool): Whether to include item stats
            
        Returns:
            str: Formatted inventory display
        """
        if self.is_empty():
            return "Inventory is empty."
        
        display_lines = []
        display_lines.append(f"=== INVENTORY ({self.get_capacity_string()}) ===")
        
        for i, item in enumerate(self.items, 1):
            if show_stats:
                stats = item.get_stat_summary()
                display_lines.append(f"{i:2}. {item.name} ({item.rarity}) - {stats}")
            else:
                display_lines.append(f"{i:2}. {item.name} ({item.rarity})")
        
        display_lines.append("")
        display_lines.append(f"Total Value: {self.get_total_value()} gold")
        
        return "\n".join(display_lines)
    
    def get_item_by_index(self, index):
        """
        Get item by its position in inventory (1-based indexing).
        
        Args:
            index (int): Position in inventory (1-based)
            
        Returns:
            Equipment or None: The item at that position
        """
        if 1 <= index <= len(self.items):
            return self.items[index - 1]
        return None