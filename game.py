import pygame as pg
import sys
from pygame.locals import *
from pytmx import load_pygame

from scripts.settings import Settings
from scripts.entities import Player
from scripts.tilemap import Tilemap


# Use later
vec = pg.math.Vector2  # 2 dimensional

class Game:
    def __init__(self):
        # Start pygame and default settings
        pg.init()
        self.settings = Settings()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height), 0, 32)
        pg.display.set_caption("The Forgotten Pages")

        # load map
        self.tmx_data = load_pygame("./assets/Map/map_final.tmx")
        self.world_offset = self.settings.world_offset
        self.map_bg = pg.transform.scale(pg.image.load("./assets/Map/main_background.png").convert_alpha(), (self.settings.screen_width, self.settings.screen_height),)

        # Create first player
        # initial height is set to be (screen_height - 19) to avoid upward movement at the start of the game

        # Pass the game instance to the Player class
        # self.player = Player(self, 0, self.settings.screen_height - 19, 1)
        # OLD self.player = Player(self, 0, self.screen.get_size()[1] - 19, 1.25)
        self.player = Player(self, (0, self.screen.get_size()[1] - 19), (8, 16))
        self.tilemap = Tilemap(self, tile_size=16)

        # Use a dictionary to store different types of sprites
        self.entities = {
            "player": self.player,
            # 'monster': self.monster,
            # 'map': self.map,
        }

        # Player Movement Bools
        self.moving_left = False
        self.moving_right = False
        self.movement = [False, False]

        self.offset = [0, 0]

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
                    self.moving_right = True #OLD
                    self.movement[1] = True # New
                if key == K_a or key == K_LEFT:
                    self.moving_left = True #old
                    self.movement[0] = True #new
                if key == K_SPACE:
                    self.player.velocity.y = -3 #new
                if key == K_q:
                    pg.quit()
                    sys.exit()
            # Keyup Press
            if event.type == KEYUP:
                key = event.key
                if key == K_d or key == K_RIGHT:
                    self.moving_right = False #old
                    self.movement[1] = False #new
                if key == K_a or key == K_LEFT:
                    self.moving_left = False #old
                    self.movement[0] = False #new

        self.settings.move_left = self.moving_left # remove
        self.settings.move_right = self.moving_right # remove
        
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
        if self.player.isAlive:
            # Update the animation
            self.player.update_animation()
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))

            # Update boss and other items here
            # TODO

    # display the map to the screen
    def display_map(self, tmx_data, world_offset):
        for layer in tmx_data:
            # x,y,surface
            for tile in layer.tiles():
                x_pixel = tile[0] * 16 - world_offset[0]
                y_pixel = tile[1] * 16 - world_offset[1]
                # draw surface onto the screen
                self.screen.blit(tile[2], (x_pixel, y_pixel))

    def draw_entities(self):
        self.offset[0] += (self.player.rect().centerx - self.settings.screen_width / 2 - self.offset[0]) / 30
        self.offset[1] += (self.player.rect().centery - self.settings.screen_height / 3 - self.offset[1]) / 30
        render_offset = (int(self.offset[0]), int(self.offset[1]))
        # draw bg color before each loop
        self.screen.blit(self.map_bg, (0, 0))
        # draw the map
        self.display_map(self.tmx_data, render_offset)

        for entity in self.entities.values():
            # draw players
            entity.draw(render_offset)


if __name__ == "__main__":
    """Call py game.py to initiate and run the game"""
    level = Game()
    level.play()
