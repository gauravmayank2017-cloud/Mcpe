"""
PROJECT: VoxenCore Pro - Ultimate Voxel Engine
FILE: 6 / 50 (ui_framework.py)
DESCRIPTION: Heads-Up Display (HUD) management. Handles inventory slots, 
             health visualization, and crosshair rendering.
"""

from ursina import *

class GameUI:
    def __init__(self):
        # 1. क्रॉसहेयर (The Crosshair)
        self.crosshair = Entity(
            parent=camera.ui,
            model='quad',
            texture='assets/ui/crosshair.png', # File 5 में डिफाइंड है
            scale=0.03,
            color=color.white
        )

        # 2. हॉटबार (Hotbar - 9 Slots)
        self.hotbar = Entity(
            parent=camera.ui,
            model='quad',
            texture='assets/ui/hotbar_bg.png',
            scale=(0.5, 0.08),
            position=(0, -0.45),
            color=color.rgba(255, 255, 255, 200)
        )

        # 3. हेल्थ बार (Health Bar)
        self.health_bar_bg = Entity(
            parent=camera.ui,
            model='quad',
            scale=(0.3, 0.02),
            position=(-0.6, -0.45),
            color=color.black66
        )
        self.health_inner = Entity(
            parent=self.health_bar_bg,
            model='quad',
            scale=(1, 1),
            position=(0, 0),
            color=color.red,
            origin_x=-0.5 # लेफ्ट से राइट कम होगा
        )

        # 4. इन्वेंटरी डेटा (Current Selection)
        self.selected_slot = 0
        self.slots = [None] * 9
        self.selector_box = Entity(
            parent=self.hotbar,
            model=Mesh(vertices=[(-0.5,-0.5,0), (0.5,-0.5,0), (0.5,0.5,0), (-0.5,0.5,0)], mode='line', thickness=2),
            scale=(1/9, 1),
            position=(-0.44, 0),
            color=color.yellow
        )

    def update_selected_slot(self, slot_index):
        """जब प्लेयर 1-9 दबाता है तो सेलेक्टर को हिलाना"""
        if 0 <= slot_index < 9:
            self.selected_slot = slot_index
            # गणितीय कैलकुलेशन सेलेक्टर की पोजीशन के लिए
            self.selector_box.x = -0.44 + (slot_index * (0.88 / 8))
            print(f"[UI] Slot {slot_index + 1} selected.")

    def update_health(self, current, maximum):
        """हेल्थ कम या ज्यादा होने पर बार को अपडेट करना"""
        self.health_inner.scale_x = current / maximum
        if self.health_inner.scale_x < 0.3:
            self.health_inner.color = color.orange
        else:
            self.health_inner.color = color.red

# ---------------------------------------------------------
# UI ANIMATION LOGIC:
# एक प्रोफेशनल गेम में यहाँ हज़ारों लाइनें होती हैं जो:
# 1. स्क्रीन शेक (Screen Shake) जब प्लेयर को चोट लगे।
# 2. इन्वेंटरी खोलते समय ब्लर इफेक्ट (Blur Effect)।
# 3. बटन्स पर होवर करने पर साउंड प्ले करना।
# ---------------------------------------------------------

# Global UI Instance
ui = GameUI()
