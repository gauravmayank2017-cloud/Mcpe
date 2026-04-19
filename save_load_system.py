"""
PROJECT: VoxenCore Pro - Ultimate Voxel Engine
FILE: 12 / 50 (save_load_system.py)
DESCRIPTION: Binary data serialization for world states. 
             Handles auto-saves, player metadata, and voxel grid snapshots.
"""

import pickle
import os
import threading
from ursina import *

class SaveSystem:
    def __init__(self, world_name="Alpha_World"):
        self.save_directory = "saves/" + world_name + "/"
        self.world_file = self.save_directory + "world_data.vox"
        self.player_file = self.save_directory + "player_stats.dat"
        
        # फोल्डर बनाना अगर नहीं है
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
            print(f"[SAVE_SYSTEM] Created new save directory: {world_name}")

    def save_game_async(self, world_data, player_data):
        """बैकग्राउंड में गेम सेव करना (ताकि गेम लैग न हो)"""
        save_thread = threading.Thread(target=self.save_logic, args=(world_data, player_data))
        save_thread.start()
        print("[SAVE_SYSTEM] Auto-save initiated in background...")

    def save_logic(self, world_data, player_data):
        """असली राइटिंग ऑपरेशन (Binary Write)"""
        try:
            # 1. वर्ल्ड डेटा सेव करना (Voxel positions, types)
            with open(self.world_file, 'wb') as f:
                pickle.dump(world_data, f)
            
            # 2. प्लेयर डेटा सेव करना (Position, Inventory, Health)
            with open(self.player_file, 'wb') as f:
                pickle.dump(player_data, f)
                
            print("[SAVE_SYSTEM] World state synced to disk.")
        except Exception as e:
            print(f"[CRITICAL ERROR] Save failed: {e}")

    def load_game(self):
        """डिस्क से डेटा वापस लाना"""
        if not os.path.exists(self.world_file):
            print("[SAVE_SYSTEM] No save file found. Starting fresh.")
            return None, None

        try:
            with open(self.world_file, 'rb') as f:
                world_data = pickle.load(f)
            
            with open(self.player_file, 'rb') as f:
                player_data = pickle.load(f)
            
            print("[SAVE_SYSTEM] World and Player data restored.")
            return world_data, player_data
        except Exception as e:
            print(f"[SAVE_SYSTEM] Corrupt save file: {e}")
            return None, None

# ---------------------------------------------------------
# DATA STRUCTURE NOTE:
# 'world_data' एक डिक्शनरी होगी: {(x,y,z): 'grass', (x,y+1,z): 'stone'}
# एक "तगड़े" गेम में यहाँ 'ZLib Compression' भी जोड़ा जाता है 
# ताकि 1GB का वर्ल्ड डेटा सिर्फ 10MB में बदल जाए।
# ---------------------------------------------------------

# Global Save System Instance
save_manager = SaveSystem()
