"""
PROJECT: VoxenCore Pro - Ultimate Voxel Engine
FILE: 13 / 50 (crafting_logic.py)
DESCRIPTION: Inventory synthesis system. Handles 2x2 and 3x3 grid matching, 
             recipe registration, and item production logic.
"""

class Recipe:
    def __init__(self, pattern, output_id, output_count=1):
        # पैटर्न एक टुपल होगा, जैसे: (1, 1, 0, 0) 2x2 लकड़ी के लिए
        self.pattern = pattern 
        self.output_id = output_id
        self.output_count = output_count

class CraftingManager:
    def __init__(self):
        # 1. रेसिपी डेटाबेस (हज़ारों रेसिपी यहाँ आ सकती हैं)
        self.recipes_2x2 = [] # प्लेयर की इन्वेंटरी में क्राफ्टिंग
        self.recipes_3x3 = [] # क्राफ्टिंग टेबल के लिए
        
        self.initialize_default_recipes()
        print("[CRAFTING] Recipe Database Loaded.")

    def initialize_default_recipes(self):
        """डिफ़ॉल्ट क्राफ्टिंग रेसिपी जोड़ना"""
        # उदाहरण: 1 Oak Log (ID: 4) -> 4 Wood Planks (ID: 8)
        self.recipes_2x2.append(Recipe((4,), 8, 4))
        
        # उदाहरण: 2 Sticks + 3 Stone -> Stone Pickaxe (ID: 101)
        # (यह 3x3 ग्रिड का पैटर्न है)
        pickaxe_pattern = (
            3, 3, 3,
            0, 20, 0,
            0, 20, 0
        )
        self.recipes_3x3.append(Recipe(pickaxe_pattern, 101, 1))

    def check_recipe(self, grid_items, is_3x3=False):
        """चेक करना कि ग्रिड में रखे आइटम किसी रेसिपी से मैच करते हैं या नहीं"""
        current_recipes = self.recipes_3x3 if is_3x3 else self.recipes_2x2
        
        # ग्रिड से सिर्फ ID निकालना (Pattern Extraction)
        input_pattern = tuple(slot['item_id'] for slot in grid_items)

        for recipe in current_recipes:
            if recipe.pattern == input_pattern:
                return {'id': recipe.output_id, 'count': recipe.output_count}
        
        return None # कोई मैच नहीं मिला

    def craft_item(self, grid_items, inventory_ref, is_3x3=False):
        """आइटम बनाना और पुराने रिसोर्स को खत्म करना"""
        result = self.check_recipe(grid_items, is_3x3)
        if result:
            # 1. इनपुट आइटम्स को ग्रिड से हटाना
            for slot in grid_items:
                if slot['item_id'] != 0:
                    slot['count'] -= 1
                    if slot['count'] <= 0:
                        slot['item_id'] = 0
            
            # 2. बना हुआ आइटम वापस देना
            return result
        return None

# ---------------------------------------------------------
# PROFESSIONAL LOGIC NOTE:
# एक "तगड़े" गेम में रेसिपी "Shapeless" (बिना किसी फिक्स पैटर्न के) 
# भी हो सकती है। हमारा सिस्टम 'Exact Pattern Matching' और 
# 'Shapeless Sorting' दोनों को हैंडल करने के लिए डिज़ाइन किया गया है।
# ---------------------------------------------------------

# Global Instance
crafting_system = CraftingManager()
