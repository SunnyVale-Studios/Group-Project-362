import pygame
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2 # 2 dimensional

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60 

FramePerSec = pygame.time.Clock()
display_surface = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("GAME")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # create surface object
        self.surf = pygame.surface((30,30)) 
        # give surface a color
        self.surface.fill((128,255,40))
        # create rect object
        # center defines starting object when drawn
        # top left corner is origin point with (0,0)
        self.rect = self.surf.get_rect(center=(10,420))

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH,20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))
PT1 = platform()
P1 = Player()