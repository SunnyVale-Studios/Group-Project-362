import pygame as pg
import sys
from pygame.locals import *
from pygame.sprite import Sprite

from settings import Settings
from player import Player

#START
# Use later
vec = pg.math.Vector2  # 2 dimensional

# Moved to settings
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
#END

class Platform(Sprite):
    #Make into a module later
    def __init__(self):
        super().__init__()
        self.surf = pg.Surface((WIDTH, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), 0, 32)
        pg.display.set_caption("Pygame Platform")
        self.player = Player(game=self)
        self.platform = Platform()

        self.sprites = pg.sprite.Group()
        self.sprites.add(self.player)
        self.sprites.add(self.platform)


    def play(self):
        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))

            for entity in self.sprites:
                self.screen.blit(entity.surf, entity.rect)

                pg.display.update()
                self.clock.tick(self.settings.fps)

if __name__ == "__main__":
    '''Call py game.py to initiate and run the game'''
    level = Game()
    level.play()
