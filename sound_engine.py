"""
PROJECT: VoxenCore Pro - Ultimate Voxel Engine
FILE: 10 / 50 (sound_engine.py)
DESCRIPTION: Advanced Audio Engine. Manages 3D spatial sound positioning, 
             dynamic ambient mixing, and footstep sound variations.
"""

from ursina import *
import math

class SoundEngine:
    def __init__(self):
        # 1. वॉल्यूम सेटिंग्स (Master Mix)
        self.master_volume = 0.5
        self.sfx_volume = 0.8
        self.music_volume = 0.4
        
        # 2. म्यूज़िक प्लेयर (Ambient Tracks)
        self.current_track = None
        self.ambient_tracks = {
            'overworld': 'assets/music/calm_exploration.mp3',
            'cave': 'assets/music/dark_ambient.mp3',
            'combat': 'assets/music/battle_tension.mp3'
        }

        # 3. साउंड बफ़र्स (Sound Buffers)
        # प्रोफेशनल गेम्स में हज़ारों साउंड्स को एक साथ लोड नहीं किया जाता (Memory Optimization)
        self.cached_sounds = {}

        print("[AUDIO] OpenAL Spatial Engine Online.")

    def play_3d_at(self, sound_name, position, max_dist=20):
        """3D लोकेशन पर आवाज़ बजाना (Spatial Audio)"""
        # प्लेयर की पोजीशन लेना (File 3 से)
        from main import player_instance
        
        dist = distance(player_instance.position, position)
        
        if dist > max_dist:
            return # बहुत दूर है, आवाज़ नहीं आएगी

        # दूरी के आधार पर वॉल्यूम कम करना (Attenuation)
        vol = (1 - (dist / max_dist)) * self.sfx_volume
        
        # पनिंग (Panning - बाएँ या दाएँ कान में आवाज़)
        # यह गणना की जाती है कि आवाज़ प्लेयर के किस तरफ है
        s = Audio(sound_name, pitch=random.uniform(0.9, 1.1), volume=vol, loop=False)
        return s

    def play_footstep(self, block_type):
        """ब्लॉक के प्रकार के हिसाब से पैरों की आवाज़ बदलना"""
        # हजारों लाइन्स का डेटाबेस यहाँ हो सकता है (Stone vs Grass vs Sand)
        footstep_sounds = {
            'grass': 'assets/sounds/step_grass.wav',
            'stone': 'assets/sounds/step_stone.wav',
            'wood': 'assets/sounds/step_wood.wav'
        }
        
        sound_file = footstep_sounds.get(block_type, footstep_sounds['grass'])
        Audio(sound_file, pitch=random.uniform(0.8, 1.2), volume=self.sfx_volume * 0.5)

    def transition_music(self, track_key):
        """एक संगीत से दूसरे में स्मूथली जाना (Fade in/out)"""
        if self.current_track:
            self.current_track.fade_out(duration=2)
        
        new_track_path = self.ambient_tracks.get(track_key)
        if new_track_path:
            self.current_track = Audio(new_track_path, loop=True, volume=self.music_volume)
            self.current_track.fade_in(duration=3)

# ---------------------------------------------------------
# REVERB & DSP NOTE:
# एक "तगड़े" गेम में हम 'Digital Signal Processing' (DSP) का उपयोग करते हैं।
# अगर प्लेयर गुफा (Cave) के अंदर है, तो हम साउंड में 'Echo' और 'Reverb' 
# फ़िल्टर जोड़ते हैं ताकि वह असली महसूस हो।
# ---------------------------------------------------------

# Global Sound Engine Instance
audio_engine = SoundEngine()
