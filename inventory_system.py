"""
PROJECT: VoxenCore Pro - Ultimate Voxel Engine
FILE: 7 / 50 (inventory_system.py)
DESCRIPTION: Core inventory logic. Handles item stacking, database IDs, 
             and slot management. This is the 'Data Layer'.
"""

class Item:
    def __init__(self, id, name, texture, stackable=True, max_stack=64):
        self.id = id
        self.name = name
        self.texture = texture
        self.stackable = stackable
        self.max_stack = max_stack

class InventorySystem:
    def __init__(self):
        # 1. ग्लोबल आइटम डेटाबेस (Item Database - हजारों आइटम्स यहाँ आ सकते हैं)
        self.item_db = {
            0: Item(0, 'Air', None),
            1: Item(1, 'Grass Block', 'grass_block'),
            2: Item(2, 'Dirt Block', 'dirt_block'),
            3: Item(3, 'Stone Block', 'stone_block'),
            4: Item(4, 'Oak Log', 'wood_block'),
            5: Item(5, 'Diamond Ore', 'diamond_ore_block'),
            6: Item(6, 'Iron Sword', 'sword_iron', stackable=False)
        }

        # 2. प्लेयर इन्वेंटरी (36 Slots: 9 Hotbar + 27 Main Inventory)
        self.slots = [None] * 36
        for i in range(36):
            self.slots[i] = {'item_id': 0, 'count': 0}

        print("[DATABASE] Inventory Logic System Initialized.")

    def add_item(self, item_id, amount=1):
        """इन्वेंटरी में आइटम जोड़ने का एडवांस लॉजिक"""
        item_data = self.item_db.get(item_id)
        if not item_data: return False

        # पहले चेक करें कि क्या यह पहले से किसी स्लॉट में है (Stacking)
        if item_data.stackable:
            for slot in self.slots:
                if slot['item_id'] == item_id and slot['count'] < item_data.max_stack:
                    slot['count'] += amount
                    print(f"[INV] Added {amount} to existing stack of {item_data.name}")
                    return True

        # अगर नया स्लॉट चाहिए
        for i in range(36):
            if self.slots[i]['item_id'] == 0: # Empty slot
                self.slots[i]['item_id'] = item_id
                self.slots[i]['count'] = amount
                print(f"[INV] {item_data.name} added to new slot {i}")
                return True
        
        print("[INV] Inventory Full!")
        return False

    def remove_item(self, slot_index, amount=1):
        """आइटम कम करना (जैसे ब्लॉक लगाने पर)"""
        if self.slots[slot_index]['count'] >= amount:
            self.slots[slot_index]['count'] -= amount
            if self.slots[slot_index]['count'] == 0:
                self.slots[slot_index]['item_id'] = 0 # Empty it
            return True
        return False

    def get_current_item_id(self, hotbar_index):
        """अभी हाथ में कौन सा आइटम है?"""
        return self.slots[hotbar_index]['item_id']

# ---------------------------------------------------------
# PROFESSIONAL ARCHITECTURE NOTE:
# एक असली गेम में, यहाँ JSON Serialization का कोड होता है 
# ताकि प्लेयर जब गेम बंद करे, तो उसकी इन्वेंटरी 'world_save.dat' 
# फाइल में सुरक्षित रहे। (यह File 20: save_system.py में आएगा)
# ---------------------------------------------------------

# Global Inventory Instance
inventory = InventorySystem()
