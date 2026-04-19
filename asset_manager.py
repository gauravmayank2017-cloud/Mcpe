"""
PROJECT: VoxenCore Pro - Ultimate Voxel Engine
FILE: 5 / 50 (asset_manager.py)
DESCRIPTION: Centralized asset loading system. Handles texture atlases, 
             sound buffers, and missing-texture fallbacks.
"""

from ursina import *
import os

class AssetManager:
    def __init__(self):
        # 1. टेक्सचर डिक्शनरी (हज़ारों ब्लॉक्स के लिए डेटा बेस)
        self.textures = {
            'grass': 'assets/textures/blocks/grass_diffuse.png',
            'dirt': 'assets/textures/blocks/dirt_diffuse.png',
            'stone': 'assets/textures/blocks/stone_diffuse.png',
            'sand': 'assets/textures/blocks/sand_diffuse.png',
            'wood': 'assets/textures/blocks/oak_log.png',
            'leaves': 'assets/textures/blocks/leaves_opaque.png',
            'glass': 'assets/textures/blocks/glass_clear.png',
            'bedrock': 'assets/textures/blocks/bedrock.png',
            'missing': 'assets/textures/error/magenta.png' # Fallback
        }

        # 2. साउंड लाइब्रेरी
        self.sounds = {
            'step_grass': 'assets/sounds/fx/footsteps/grass_1.wav',
            'block_break': 'assets/sounds/fx/world/break.wav',
            'bg_music': 'assets/sounds/music/ambient_overworld.mp3'
        }

        # 3. मॉडल्स
        self.models = {
            'player_hand': 'assets/models/viewmodel/arm.obj',
            'dropped_item': 'assets/models/entities/item_drop.obj'
        }

        self.pre_load_assets()

    def pre_load_assets(self):
        """गेम शुरू होने से पहले ज़रूरी चीज़ें मेमोरी में डालना (Loading Screen Logic)"""
        print("[ASSETS] Starting Pre-load sequence...")
        for key, path in self.textures.items():
            # यह चेक करता है कि फाइल असल में मौजूद है या नहीं
            # (असली गेम में यहाँ हजारों लाइन्स की चेकिंग होती है)
            try:
                load_texture(path)
            except:
                print(f"[ERROR] Asset missing: {path}. Using fallback.")
                self.textures[key] = self.textures['missing']

    def get_tex(self, name):
        """ब्लॉक के लिए टेक्सचर वापस करना"""
        return self.textures.get(name, self.textures['missing'])

    def play_fx(self, effect_name):
        """साउंड इफेक्ट प्ले करना"""
        if effect_name in self.sounds:
            s = Audio(self.sounds[effect_name], loop=False, autoplay=True)
            return s

# ---------------------------------------------------------
# DATA ARCHITECTURE NOTE:
# एक बड़े प्रोजेक्ट में, इस फाइल के अंदर हज़ारों लाइन का 'JSON' 
# या 'XML' डेटा होता है जो हर एक आइटम की प्रॉपर्टी बताता है।
# ---------------------------------------------------------

# Instance for Global Use
assets = AssetManager()
