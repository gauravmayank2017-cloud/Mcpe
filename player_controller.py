"""
PROJECT: VoxenCore Pro - Ultimate Voxel Engine
FILE: 3 / 50 (player_controller.py)
DESCRIPTION: Advanced First-Person Controller with Physics, Raycasting, 
             and Interaction Logic. Handles gravity and velocity vectors.
"""

from ursina import *
from ursina.prefabs.first_person_controller import First_Person_Controller

class VoxenPlayer(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        
        # 1. प्लेयर की फिजिकल प्रॉपर्टीज (Physics)
        self.speed = 8
        self.jump_height = 2
        self.gravity = 0.8
        self.velocity = Vec3(0,0,0)
        self.grounded = False
        self.walking = False
        
        # 2. कैमरा और विजुअल (Advanced Camera Logic)
        self.controller = First_Person_Controller(
            model='cube',
            z=-10,
            color=color.orange,
            origin_y=-.5,
            speed=self.speed,
            collider='box'
        )
        self.controller.cursor.texture = 'assets/crosshair.png' # कस्टम क्रॉसहेयर
        self.controller.cursor.scale = 0.02
        
        # 3. हेड बॉबिंग (Head Bobbing for Realism)
        self.bob_speed = 10
        self.bob_amount = 0.05
        self.timer = 0

    def update(self):
        """हर फ्रेम में प्लेयर की स्थिति अपडेट करना"""
        self.handle_movement()
        self.check_interaction()
        self.apply_gravity()

    def handle_movement(self):
        # चलना और दौड़ना (Sprinting)
        if held_keys['left shift']:
            self.controller.speed = self.speed * 1.5
        else:
            self.controller.speed = self.speed

        # हेड बॉबिंग लॉजिक
        if self.controller.direction != Vec3(0,0,0):
            self.timer += time.dt * self.bob_speed
            self.controller.camera_pivot.y = 2 + math.sin(self.timer) * self.bob_amount
        else:
            self.timer = 0
            self.controller.camera_pivot.y = lerp(self.controller.camera_pivot.y, 2, time.dt * 10)

    def check_interaction(self):
        """ब्लॉक तोड़ने और लगाने का एडवांस सिस्टम (Raycasting)"""
        # स्क्रीन के बीच से एक अदृश्य किरण (Ray) निकलती है
        hit_info = raycast(self.controller.camera_pivot.world_position, 
                           self.controller.camera_pivot.forward, 
                           distance=5)
        
        if hit_info.hit:
            # अगर माउस का लेफ्ट बटन दबाया (Block Breaking)
            if held_keys['left mouse']:
                if hit_info.entity:
                    destroy(hit_info.entity)
                    # यहाँ File #10 (Particle System) को कॉल किया जा सकता है
            
            # अगर राइट बटन दबाया (Block Placing)
            if held_keys['right mouse']:
                # यह लॉजिक अगली फाइल (voxel_system.py) से कनेक्ट होगा
                pass

    def apply_gravity(self):
        """कस्टम ग्रेविटी इंजन"""
        # जमीन चेक करना
        ray = raycast(self.controller.world_position + Vec3(0, 1, 0), Vec3(0, -1, 0), distance=1.1)
        if ray.hit:
            self.grounded = True
            if self.velocity.y < 0:
                self.velocity.y = 0
        else:
            self.grounded = False
            self.velocity.y -= self.gravity * time.dt

        # जंपिंग (Jumping)
        if self.grounded and held_keys['space']:
            self.velocity.y = self.jump_height

        self.controller.y += self.velocity.y

# ---------------------------------------------------------
# SYSTEM HOOKS (For File Integration)
# ---------------------------------------------------------
def input(key):
    if key == 'q': # इन्वेंटरी शॉर्टकट
        print("[UI] Opening Inventory (Redirecting to File 15...)")

# यह फाइल अकेली नहीं चलेगी, इसे main.py (File 1) इम्पोर्ट करेगा।
