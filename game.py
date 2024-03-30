import pygame as pg
import sys
from pygame.locals import *
from pygame.sprite import Sprite, Group

from settings import Settings
from player import Player

# START
# Use later
vec = pg.math.Vector2  # 2 dimensional


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), 0, 32
        )
        pg.display.set_caption("Pygame Platform")
        # Create first player
        # initial height is set to be (screen_height - 19) to avoid upward movement at the start of the game

        # TODO - Should have game as input instead of screen, so that player movement doesn't have to taken from settings py
        self.player = Player(
            self.screen, 0, self.settings.screen_height - 19, 1, self.settings
        )

        # TODO - Simplfy players no need for groups. There are only map, monster and player
        self.sprites = Group()
        self.sprites.add(self.player)

        # Player Movement Bools
        self.moving_left = False
        self.moving_right = False

    
    def check_events(self):
        for event in pg.event.get():
            #Quit Condition
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            #Keydown Press
            if event.type == KEYDOWN:
                key = event.key
                if key == K_d or key == K_RIGHT:
                    self.moving_right = True
                if key == K_a or key == K_LEFT:
                    self.moving_left = True
                if key == K_SPACE and self.player.alive:
                    self.player.jump = True
            #Keyup Press
            if event.type == KEYUP:
                key = event.key
                if key == K_d or key == K_RIGHT:
                    self.moving_right = False
                if key == K_a or key == K_LEFT:
                    self.moving_left = False

        self.settings.move_left = self.moving_left
        self.settings.move_right = self.moving_right

    def play(self):

        while True:
            # TODO - Lets change how event handling is placed (separate method)
            # As well as how the user animation is made and how entities are updated
            # The current code assumes that all classes will follow the same methods.
            # But monster might be different
            
            # Check pygame events (movement)
            self.check_events()
            # END of TODO

            # TODO - Implement wihtin player update()
            if self.player.alive:
                # update jump action, action(2) for jump
                if self.player.in_air:
                    self.player.update_action(2)
                # update player's action
                elif self.moving_left or self.moving_right:
                    # if moving, using action 1 for run
                    self.player.update_action(1)
                else:
                    # if not, using action 0 for idle
                    self.player.update_action(0)
            # END of TODO
                    
            # TODO - Remove to handle drawing the updaing in the same line (inside class)
                # self.player.update()
                    
            for entity in self.sprites:
                # draw bg color before each loop
                entity.draw_BG()
                # player animation
                entity.update_animation()
                # draw players
                entity.draw()
                # move player
                entity.move()
            # END of TODO

            pg.display.update()
            self.clock.tick(self.settings.fps)


if __name__ == "__main__":
    """Call py game.py to initiate and run the game"""
    level = Game()
    level.play()
