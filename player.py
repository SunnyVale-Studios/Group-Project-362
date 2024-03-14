import pygame as pg
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        # create surface object
        self.surf = pg.Surface((30, 30))
        # give surface a color
        self.surf.fill((128, 255, 40))
        # create rect object
        # center defines starting object when drawn
        # top left corner is origin point with (0,0)
        self.rect = self.surf.get_rect(center=(10, 420))

if __name__ == "__main__":
    print("Wrong file to run game. Run game.py instead!!")