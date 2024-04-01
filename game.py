import pygame as pg
import sys
from pygame.locals import *

from settings import Settings
from player import Player
from pytmx import load_pygame

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
        tmx_data = load_pygame("assets/Map/map_final.tmx")
        pg.display.set_caption("The Forgotten Pages")

        # Create first player
        # initial height is set to be (screen_height - 19) to avoid upward movement at the start of the game

        # Pass the game instance to the Player class
        self.player = Player(self, 0, self.settings.screen_height - 19, 1)

        # Use a dictionary to store different types of sprites
        self.entities = {
            "player": self.player,
            # 'monster': self.monster,
            # 'map': self.map,
        }

        # Player Movement Bools
        self.moving_left = False
        self.moving_right = False

    def check_events(self):
        for event in pg.event.get():
            # Quit Condition
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            # Keydown Press
            if event.type == KEYDOWN:
                key = event.key
                if key == K_d or key == K_RIGHT:
                    self.moving_right = True
                if key == K_a or key == K_LEFT:
                    self.moving_left = True
                if key == K_SPACE and self.player.alive:
                    self.player.jump = True
            # Keyup Press
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
            self.events_checker()
            self.update_entities()
            self.draw_entities()

            pg.display.update()
            self.clock.tick(self.settings.fps)

    def events_checker(self):
        # Check events
        self.check_events()

    def update_entities(self):
        # when player is alive
        if self.player.alive:
            # Update the animation
            self.player.update_animation()
            # update jump action for jump
            if self.player.in_air:
                self.player.update_action("jump")
            # update player's action
            elif self.moving_left or self.moving_right:
                # if moving, update action for run
                self.player.update_action("run")
            else:
                # if not, update action for idle
                self.player.update_action("idle")

            # Update all entities
            for entity in self.entities.values():
                entity.move()

    def draw_entities(self):
        for entity in self.entities.values():
            # draw bg color before each loop
            entity.draw_BG()
            # draw players
            entity.draw()


if __name__ == "__main__":
    """Call py game.py to initiate and run the game"""
    level = Game()
    level.play()
