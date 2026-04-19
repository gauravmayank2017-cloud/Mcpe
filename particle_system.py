"""
PROJECT: VoxenCore Pro - Ultimate Voxel Engine
FILE: 11 / 50 (particle_system.py)
DESCRIPTION: High-performance particle emitter system. 
             Handles block-break fragments, smoke, and weather particles.
"""

from ursina import *
import random

class Particle(Entity):
    def __init__(self, position, color, velocity, lifetime=0.5):
        super().__init__(
            model='cube',
            position=position,
            scale=random.uniform(0.05, 0.15),
            color=color,
            collider=None # परफॉरमेंस के लिए कोलाइडर बंद
        )
        self.velocity = velocity
        self.lifetime = lifetime
        self.start_time = time.time()

    def update(self):
        # 1. मूवमेंट (Velocity + Gravity)
        self.velocity.y -= 0.5 * time.dt # ग्रेविटी
        self.position += self.velocity * time.dt
        
        # 2. लाइफटाइम चेक (मेमोरी बचाने के लिए)
        if time.time() - self.start_time > self.lifetime:
            destroy(self)

class FXManager:
    def __init__(self):
        self.max_particles = 200 # एक समय में अधिकतम कण
        print("[FX_ENGINE] Particle System Initialized.")

    def spawn_block_break(self, position, block_color):
        """जब ब्लॉक टूटता है तो 10-15 टुकड़े पैदा करना"""
        for i in range(12):
            # रैंडम दिशा में उछालना (Physics)
            random_vel = Vec3(
                random.uniform(-2, 2),
                random.uniform(2, 5),
                random.uniform(-2, 2)
            )
            Particle(
                position=position + Vec3(0, 0.5, 0),
                color=block_color,
                velocity=random_vel,
                lifetime=random.uniform(0.3, 0.8)
            )

    def spawn_explosion(self, position):
        """TNT फटने पर धुएं और आग के कण"""
        for i in range(30):
            p = Particle(
                position=position,
                color=random.choice([color.orange, color.gray, color.yellow]),
                velocity=Vec3(random.uniform(-5, 5), random.uniform(2, 8), random.uniform(-5, 5)),
                lifetime=1.0
            )
            p.scale *= 2 # धमाके के कण बड़े होंगे

# ---------------------------------------------------------
# OPTIMIZATION NOTE:
# एक प्रोफेशनल गेम में 'Instancing' का उपयोग होता है। 
# बजाय हर टुकड़े के लिए नया ऑब्जेक्ट बनाने के, हम GPU को 
# एक साथ 1000 टुकड़ों का डेटा भेजते हैं। (Advanced File #30 में आएगा)
# ---------------------------------------------------------

# Global FX Instance
fx_engine = FXManager()
