import pygame as pg
from scripts.timer import Timer
import os

class PhysicsEntity:
    def __init__(self, game, type, pos, size):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.type = type
        self.size = size
        self.pos = list(pos) # Figure out why other than just making a new variable

        self.velocity = pg.Vector2(0, 0)
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.isJumping = False
        self.isAlive = True # Used later to determine whether game is over


        # Animation list
        self.animations = {
            "idle": Timer(self.load_images("idle", self.size[1] // 16), "idle"),
            "run": Timer(self.load_images("run", self.size[1] // 16), "run"),
            "jump": Timer(self.load_images("jump", self.size[1] // 16), "jump"),
        }

        self.current_animation = self.animations["idle"]
        self.flip = False

    def load_images(self, animation_name, scale):
        # Define base path for player imgs
        Base_Player_Path = "assets/Adventurer/Indvidual Sprites/"
        # Load all images for the player
        temp_list = []
        # Count number of files in the folder
        num_of_frames = len(os.listdir(Base_Player_Path + f"{animation_name}"))
        for i in range(num_of_frames):
            # Load player img
            img = pg.image.load(
                Base_Player_Path
                + f"{animation_name}/adventurer-{animation_name}-0{i}-1.3.png"
            ).convert_alpha()
            # Scale player img if needed
            img = pg.transform.scale(
                img, (int(img.get_width() * scale), int(img.get_height() * scale))
            )
            temp_list.append(img)
        return temp_list
    
    def update_animation(self):
        self.current_animation.next_frame()
    
    def set_action(self, action):
        # check if the new action is different from the previous one
        if action != self.current_animation.action:
            self.current_animation = self.animations[action]
            self.current_animation.reset()
    
    def rect(self):
        return pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def update(self, tilemap, movement=(0, 0)):
        self.colliions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            print(rect)
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y


        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.colliions['down'] or self.colliions['up']:
            self.velocity[1] = 0

        self.animations.update()

        
    def draw(self, offset=(0, 0)):
        self.screen.blit(pg.transform.flip(self.current_animation.image(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]) )


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0 # For jumping animation

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
        
        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')