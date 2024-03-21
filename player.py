import pygame as pg
import os
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self, screen, x, y ,scale, settings):
        super().__init__()
        self.screen = screen
        self.settings = settings
        #Set player status, use later
        self.alive = True
        self.velocity = pg.Vector2(0,0)
        #Set Jump
        self.jump = False
        #Jump condition, in-air or not
        self.in_air = True
        #vertical velocity
        self.vel_y = 0
        #Animation list
        self.animation_list = []
        self.frame_index = 0
        #Action type (0 for idle, 1 for run)
        self.action = 0
        self.update_time = pg.time.get_ticks()
        
        #Define base path for player imgs
        Base_Player_Path = 'assets/Adventurer/Indvidual Sprites/'
        
        #load all images for the player
        animation_types = ['idle', 'run', 'jump']
        for animation in animation_types:
            #reset temp list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(Base_Player_Path + f'{animation}'))
            #idle animation
            for i in range(num_of_frames): 
                #load player img
                self.img = pg.image.load(Base_Player_Path + f'{animation}/adventurer-{animation}-0{i}-1.3.png')
                #scale player img if needed
                self.img = pg.transform.scale(self.img, (int(self.img.get_width() * scale), int(self.img.get_height() * scale)))
                temp_list.append(self.img)
            self.animation_list.append(temp_list)
        
        self.image = self.animation_list[self.action][self.frame_index]
        #Set player location
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        #Set player direction
        self.direction = 1
    
    #Set player's movement
    def move(self):
        #Horizontal Movement
        self.velocity.x += (self.settings.move_right - self.settings.move_left) * self.settings.acceleration
        #Moving direction
        if self.velocity.x >0:
            self.direction = 1
        elif self.velocity.x <0:
            self.direction = -1
        
        #Jump setting
        if self.jump and self.in_air == False:
            #jump height
            self.vel_y = -8
            #inital state
            self.jump = False
            self.in_air = True
        
        #Apply gravity
        self.vel_y += self.settings.gravity
        #Prevent player from falling out of the window
        if self.rect.bottom + self.vel_y > self.settings.screen_height:
            self.vel_y = self.settings.screen_height - self.rect.bottom
            self.in_air = False
        self.rect.y += self.vel_y
        
        
        #Apply move friction
        if self.velocity.x != 0:
            self.velocity.x += self.velocity.x * self.settings.friction
        #Set velocity cap    
        if abs(self.velocity.x) > self.settings.max_velocity:
            self.velocity.x = self.settings.max_velocity if self.velocity.x > 0 else -self.settings.max_velocity
        #Set movement boundary
        if self.rect.left + self.velocity.x < 0:
            self.rect.left = 0
        elif self.rect.right + self.velocity.x > self.settings.screen_width:
            self.rect.right = self.settings.screen_width
        else:
            self.rect.x += self.velocity.x
    
    #Set player animation
    def update_animation(self):
        self.ANIMATION_COOLDOWN = 100
        #update img depend on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if there is enough time has passed since last update
        if pg.time.get_ticks() - self.update_time > self.ANIMATION_COOLDOWN:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
        #reset index if run out of list
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        
    
    def update_action(self, new_action):
        #check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            #update animation setting
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()
    
    #draw players on the screen
    def draw(self):
        # Flip the image if moving to the left
        if self.direction == -1:
            self.screen.blit(pg.transform.flip(self.image, True, False), self.rect)
        else:
            self.screen.blit(self.image, self.rect)
        
    def draw_BG(self):
        self.screen.fill((25, 25, 25))
        
    
if __name__ == "__main__":
    print("Wrong file to run game. Run game.py instead!!")