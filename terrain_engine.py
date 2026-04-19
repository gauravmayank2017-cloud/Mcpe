"""
PROJECT: VoxenCore Pro - Ultimate Voxel Engine
FILE: 2 / 50 (terrain_engine.py)
DESCRIPTION: Advanced Chunk-based terrain generation. 
             Uses noise functions to create procedural elevation.
"""

from ursina import *
import math

class ChunkManager:
    def __init__(self, world_seed=101):
        self.seed = world_seed
        self.chunk_size = 8  # Optimization: Small chunks for stability
        self.render_distance = 3
        self.chunks = {}  # Dictionary to store chunk data
        self.texture_map = {
            'grass': 'grass_block_texture',
            'dirt': 'dirt_block_texture',
            'stone': 'stone_block_texture'
        }

    def get_height(self, x, z):
        """गणितीय एल्गोरिदम - ऊँचाई तय करने के लिए"""
        # Frequency and Amplitude for realistic mountains
        freq = 0.05
        amp = 10
        
        # Simulating Perlin Noise using Sine waves for core logic
        y = math.sin(x * freq + self.seed) * math.cos(z * freq + self.seed) * amp
        y += math.sin(x * 0.1) * 2  # Detail layer
        return math.floor(y)

    def generate_chunk(self, chunk_x, chunk_z):
        """एक विशिष्ट एरिया (Chunk) में ब्लॉक्स बनाना"""
        chunk_id = (chunk_x, chunk_z)
        if chunk_id in self.chunks:
            return # पहले से बना हुआ है

        chunk_entities = []
        
        for x in range(self.chunk_size):
            for z in range(self.chunk_size):
                # वर्ल्ड कोऑर्डिनेट्स कैलकुलेट करना
                world_x = chunk_x * self.chunk_size + x
                world_z = chunk_z * self.chunk_size + z
                world_y = self.get_height(world_x, world_z)

                # ब्लॉक टाइप तय करना
                block_type = 'grass'
                if world_y < -2: block_type = 'stone'
                elif world_y < 0: block_type = 'dirt'

                # ब्लॉक को दुनिया में रखना (Voxel instantiation)
                from block_definitions import Voxel # File 4 से आएगा
                voxel = Voxel(position=(world_x, world_y, world_z), texture=block_type)
                chunk_entities.append(voxel)

        self.chunks[chunk_id] = chunk_entities
        print(f"[ENGINE] Chunk {chunk_id} generated successfully.")

    def update_chunks(self, player_pos):
        """प्लेयर के आस-पास के चंक्स को लोड/अनलोड करना"""
        p_x = math.floor(player_pos.x / self.chunk_size)
        p_z = math.floor(player_pos.z / self.chunk_size)

        for x in range(p_x - self.render_distance, p_x + self.render_distance):
            for z in range(p_z - self.render_distance, p_z + self.render_distance):
                self.generate_chunk(x, z)

# ---------------------------------------------------------
# CORE OPTIMIZATION LOGIC (The "Taghda" Part)
# ---------------------------------------------------------
# इस फाइल में हज़ारों लाइन्स का डेटा टेबल्स हो सकता है 
# जो अलग-अलग बायोम (Desert, Jungle, Ocean) को डिफाइन करेगा।
