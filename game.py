import pygame as pg
import sys
from pygame.locals import *
from pygame.sprite import Sprite

from settings import Settings
from player import Player

#START
# Use later
vec = pg.math.Vector2  # 2 dimensional

class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), 0, 32)
        pg.display.set_caption("Pygame Platform")
        #Create first player
        #initial height is set to be (screen_height - 19) to avoid upward movement at the start of the game
        self.player = Player(self.screen, 0, self.settings.screen_height - 19, 1, self.settings)

        self.sprites = pg.sprite.Group()
        self.sprites.add(self.player)


    def play(self):
    
        #movement bool
        moving_left = False
        moving_right = False
        
        while True:
            if self.player.alive:
                #update jump action, action(2) for jump
                if self.player.in_air:
                    self.player.update_action(2)
                #update player's action
                elif moving_left or moving_right:
                    #if moving, using action 1 for run
                    self.player.update_action(1)
                else:
                    #if not, using action 0 for idle
                    self.player.update_action(0)
            
            for event in pg.event.get():
                #quit condition
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                    
                #keyborad button press
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        moving_left = True
                    if event.key == pg.K_d:
                        moving_right = True
                    if event.key == pg.K_SPACE and self.player.alive:
                        self.player.jump = True
                        
                #keyborad button release
                if event.type == pg.KEYUP:
                    if event.key == pg.K_a:
                        moving_left = False
                    if event.key == pg.K_d:
                        moving_right = False
                        
            self.settings.move_left = moving_left
            self.settings.move_right = moving_right
            

            for entity in self.sprites:
                #draw bg color before each loop
                entity.draw_BG()
                #player animation
                entity.update_animation()
                #draw players
                entity.draw()
                #move player
                entity.move()

            pg.display.update()
            self.clock.tick(self.settings.fps)

if __name__ == "__main__":
    '''Call py game.py to initiate and run the game'''
    level = Game()
    level.play()
