"""
PROJECT: VoxenCore Pro - Ultimate Voxel Engine
FILE: 9 / 50 (entity_manager.py)
DESCRIPTION: Artificial Intelligence (AI) and Entity Management system. 
             Handles Pathfinding, Spawning, and Mob Behavior States.
"""

from ursina import *
import math
import random

class LivingEntity(Entity):
    def __init__(self, position=(0,0,0), model='cube', texture='white_cube', **kwargs):
        super().__init__(
            model=model,
            position=position,
            texture=texture,
            collider='box',
            origin_y=-0.5,
            **kwargs
        )
        
        # 1. एंटिटी स्टेट्स (Entity Stats)
        self.health = 20
        self.speed = 3
        self.is_hostile = False
        self.state = 'IDLE' # IDLE, WANDER, CHASE, ATTACK
        
        # 2. AI टाइमर्स
        self.wander_timer = 0
        self.change_dir_time = random.randint(2, 5)
        self.target_dir = Vec3(0,0,0)

    def update(self):
        """AI का मुख्य लूप - हर फ्रेम में निर्णय लेना"""
        if self.health <= 0:
            self.die()
            return

        # प्लेयर की दूरी चेक करना (File 3: player_controller से प्लेयर की पोजीशन लेना)
        from main import player_instance # ग्लोबल प्लेयर एक्सेस
        dist = distance(self.world_position, player_instance.position)

        if self.is_hostile and dist < 15:
            self.state = 'CHASE'
        elif dist > 20:
            self.state = 'IDLE'
        
        self.execute_behavior(player_instance, dist)

    def execute_behavior(self, player, dist):
        """व्यवहार का कार्यान्वयन (Execution of Logic)"""
        if self.state == 'CHASE':
            # प्लेयर की तरफ घूमना और चलना
            self.look_at_2d(player.position, 'y')
            self.position += self.forward * self.speed * time.dt
            
            # कोलिजन अवॉयडेंस (Raycasting to jump over blocks)
            ray = raycast(self.position + Vec3(0,0.5,0), self.forward, distance=1)
            if ray.hit and self.grounded:
                self.jump()

        elif self.state == 'IDLE' or self.state == 'WANDER':
            self.wander_logic()

    def wander_logic(self):
        """बिना किसी लक्ष्य के इधर-उधर घूमना"""
        self.wander_timer += time.dt
        if self.wander_timer > self.change_dir_time:
            self.target_dir = Vec3(random.uniform(-1,1), 0, random.uniform(-1,1)).normalized()
            self.wander_timer = 0
            self.change_dir_time = random.randint(2, 8)
        
        self.position += self.target_dir * (self.speed * 0.5) * time.dt

    def die(self):
        """मृत्यु और लूट (Loot System - File 22)"""
        print(f"[ENTITY] {self.name} has perished.")
        destroy(self)

class EntityManager:
    def __init__(self):
        self.active_mobs = []
        self.max_mobs = 20
        print("[ENTITY_SYSTEM] AI Controller Hub Online.")

    def spawn_mob(self, mob_type, position):
        """नई एंटिटी पैदा करना"""
        if len(self.active_mobs) < self.max_mobs:
            new_mob = LivingEntity(position=position)
            if mob_type == 'zombie':
                new_mob.color = color.green
                new_mob.is_hostile = True
                new_mob.name = "Zombie_Alpha"
            
            self.active_mobs.append(new_mob)
            return new_mob

# ---------------------------------------------------------
# PATHFINDING NOTE:
# एक प्रोफेशनल गेम में यहाँ 'A* (A-Star) Algorithm' का उपयोग होता है।
# यह एल्गोरिदम हज़ारों नोड्स (Blocks) को स्कैन करता है ताकि एंटिटी 
# सबसे छोटे रास्ते से प्लेयर तक पहुँच सके।
# ---------------------------------------------------------

# Instance
mob_manager = EntityManager()
