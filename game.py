import pygame as pg
import sys

from pygame.locals import *
from pytmx import load_pygame

from scripts.settings import Settings
from scripts.entities import Player
from scripts.tilemap import Tilemap
from scripts.books import BookManager

vec = pg.math.Vector2

class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height), 0, 32)
        pg.display.set_caption("The Forgotten Pages")

        self.tmx_data = load_pygame("./assets/Map/map_final.tmx")
        self.map_bg = pg.transform.scale(pg.image.load("./assets/Map/main_background.png").convert_alpha(), (self.settings.screen_width, self.settings.screen_height))

        self.player = Player(self, (2000, self.screen.get_size()[1] - 19), (8, 16))
        self.tilemap = Tilemap(self, self.tmx_data.layers[2], self.tmx_data.layers[1], self.tmx_data.layers[3], tile_size=16)

        self.moving_left = False
        self.moving_right = False
        self.movement = [False, False, False, False]
        self.up = False
        self.down = False

        self.offset = [0, 0]
        self.book_manager = BookManager(8)

    def check_events(self):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                key = event.key
                if key == K_d or key == K_RIGHT:
                    self.movement[1] = True
                if key == K_a or key == K_LEFT:
                    self.movement[0] = True
                if key == K_SPACE and not self.player.isJumping:
                    self.player.velocity.y = -self.settings.jump_velocity
                    self.player.isJumping = True
                if key == K_c:
                    self.player.creativeMode = not self.player.creativeMode
                if key == K_w and self.player.creativeMode:
                    self.up = True
                if key == K_s and self.player.creativeMode:
                    self.down = True
                if key == K_UP and self.player.on_ladder:
                    self.movement[2] = True
                if key == K_DOWN and self.player.on_ladder:
                    self.movement[3] = True
                if key == K_q:
                    pg.quit()
                    sys.exit()
            if event.type == KEYUP:
                key = event.key
                if key == K_d or key == K_RIGHT:
                    self.movement[1] = False
                if key == K_a or key == K_LEFT:
                    self.movement[0] = False
                if key == K_UP:
                    self.movement[2] = False
                if key == K_DOWN:
                    self.movement[3] = False
                if key == K_w:
                    self.up = False
                if key == K_s:
                    self.down = False

    def play(self):
        while True:
            self.events_checker()
            self.update_entities()
            self.draw_entities()
            self.render_text()

            pg.display.update()
            self.clock.tick(self.settings.fps)

    def events_checker(self):
        self.check_events()

    def update_entities(self):
        if self.player.isAlive:
            self.player.update_animation()
            self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]), (self.down - self.up)))

            if self.player.on_ladder:
                self.player.update_ladder(self.movement[3] - self.movement[2])

            player_rect = self.player.rect()
            self.book_manager.update(player_rect, self.offset)

    def display_map(self, tmx_data, world_offset):
        for layer in tmx_data:
            if layer.name == "Foreground": continue
            for tile in layer.tiles():
                x_pixel = tile[0] * 16 - world_offset[0]
                y_pixel = tile[1] * 16 - world_offset[1]
                self.screen.blit(tile[2], (x_pixel, y_pixel))

    def display_foreground(self, tmx_data, world_offset):
        for layer in tmx_data:
            if layer.name == "Foreground":
              for tile in layer.tiles():
                  x_pixel = tile[0] * 16 - world_offset[0]
                  y_pixel = tile[1] * 16 - world_offset[1]
                  self.screen.blit(tile[2], (x_pixel, y_pixel))

    def draw_entities(self):
        x_diff = self.offset[0] + ((self.player.rect().centerx - self.settings.screen_width / 2 - self.offset[0]) / 30)
        y_diff = self.offset[1] + ((self.player.rect().centery - self.settings.screen_height / 2 - self.offset[1]) / 30)

        if x_diff < 0:
           self.offset[0] = 0
        elif x_diff >= 2520:
            self.offset[0] = 2520
        else:
            self.offset[0] = int(x_diff)

        if y_diff < 0:
            self.offset[1] = 0
        elif y_diff >= 1120:
            self.offset[1] = 1120
        else:
            self.offset[1] = int(y_diff)

        render_offset = (int(self.offset[0]), int(self.offset[1]))
        self.screen.blit(self.map_bg, (0, 0))

        self.display_map(self.tmx_data, render_offset)
    
        # display books
        player_rect = self.player.rect(render_offset)
        self.book_manager.update(player_rect, render_offset)
        self.book_manager.draw(self.screen, render_offset)

        self.player.draw(render_offset)
        self.display_foreground(self.tmx_data, render_offset)

    def render_text(self):
        font = pg.font.Font(None, 25)
        text_color = (255, 255, 255) if pg.time.get_ticks() - self.player.last_sprint_time >= self.settings.sprint_cooldown else (128, 128, 128)

        sprint_text = font.render("Sprint Ready!", True, text_color)
        sprint_text_rect = sprint_text.get_rect(topright=(self.settings.screen_width - 20, 20))
        self.screen.blit(sprint_text, sprint_text_rect)

        books_text = font.render(f"Books Collected: {self.book_manager.total_collected_books}", True, (255, 255, 255))
        books_text_rect = books_text.get_rect(topright=(self.settings.screen_width - 20, 50))
        self.screen.blit(books_text, books_text_rect)

if __name__ == "__main__":
    level = Game()
    level.play()
