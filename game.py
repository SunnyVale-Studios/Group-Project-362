import pygame
import sys
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2  # 2 dimensional

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # create surface object
        self.surf = pygame.Surface((30, 30))
        # give surface a color
        self.surf.fill((128, 255, 40))
        # create rect object
        # center defines starting object when drawn
        # top left corner is origin point with (0,0)
        self.rect = self.surf.get_rect(center=(10, 420))


class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))


PT1 = platform()
P1 = Player()


all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display_surface.fill((0, 0, 0))

    for entity in all_sprites:
        display_surface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(FPS)
