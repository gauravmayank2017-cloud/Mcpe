"""
PROJECT: VoxenCore Pro - Ultimate Voxel Engine
FILE: 4 / 50 (block_definitions.py)
DESCRIPTION: Registry for all block types and their physical properties.
"""

from ursina import *

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture='grass', **kwargs):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=1,
            highlight_color=color.lime,
            **kwargs
        )
        
        # ब्लॉक डेटा
        self.health = 100
        self.is_breakable = True
        self.break_sound = Audio('assets/sounds/break.wav', autoplay=False)

    def on_break(self):
        """जब ब्लॉक टूटेगा (Particle System trigger)"""
        # File 12: particle_engine.py का इस्तेमाल यहाँ होगा
        self.break_sound.play()
        destroy(self)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                self.on_break()
            
            if key == 'right mouse down':
                # नया ब्लॉक लगाना (File 3: player_controller से डेटा लेकर)
                from player_controller import current_block_type
                Voxel(position=self.position + mouse.normal, texture=current_block_type)
