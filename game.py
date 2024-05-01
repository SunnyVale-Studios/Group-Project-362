import pygame as pg
import sys
import random

from pygame.locals import *
from pytmx import load_pygame

from scripts.settings import Settings
from scripts.entities import Player, Boss
from scripts.tilemap import Tilemap
from scripts.books import BookManager

# Use later
vec = pg.math.Vector2  # 2 dimensional

class Game:
    def __init__(self):
        # Start pygame and default settings
        pg.init()
        pg.mixer.init()
        self.settings = Settings()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height), 0, 32)
        pg.display.set_caption("The Forgotten Pages")

        # load map
        self.tmx_data = load_pygame("./assets/Map/map_final.tmx")

        """
        print(self.tmx_data.layers[2].name)
        print(self.tmx_data.layers[1].name)
        print(self.tmx_data.layers[3].name)
        """

        self.map_bg = pg.transform.scale(pg.image.load("./assets/Map/main_background.png").convert_alpha(), (self.settings.screen_width, self.settings.screen_height),)

        # Create first player
        # initial height is set to be (screen_height - 19) to avoid upward movement at the start of the game

        # Pass the game instance to the Player class
        # self.player = Player(self, 0, self.settings.screen_height - 19, 1)
        # OLD self.player = Player(self, 0, self.screen.get_size()[1] - 19, 1.25)
        self.player = Player(self, (2000, self.screen.get_size()[1] - 19), (16, 32))
        self.tilemap = Tilemap(self, self.tmx_data.layers[2], self.tmx_data.layers[1], self.tmx_data.layers[3], tile_size=16)

        # 8 is the amount of books we want spawned
        self.book_manager = BookManager(8)
        
        #Create the boss
        self.boss = Boss(self, self.player, (self.player.pos[0] - 100, self.screen.get_size()[1] - 19), (20, 32))
        
        # Player Movement Bools
        self.moving_left = False
        self.moving_right = False
        # left, right, up, down
        self.movement = [False, False, False, False]
        # TEMP DEV
        self.up = False
        self.down = False
        # END DEV

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
                    self.movement[1] = True
                if key == K_a or key == K_LEFT:
                    self.movement[0] = True
                if key == K_SPACE and not self.player.isJumping:
                    self.player.velocity.y = -self.settings.jump_velocity
                    self.player.isJumping = True #new
                # REMOVE AFTER DEV
                if key == K_c: # Creative Mode to fly around
                    self.player.creativeMode = not self.player.creativeMode
                if key == K_w and self.player.creativeMode:
                    self.up = True
                if key == K_s and self.player.creativeMode:
                    self.down = True
                # END REMOVE

                if key == K_UP and self.player.on_ladder:
                    self.movement[2] = True
                if key == K_DOWN and self.player.on_ladder:
                    self.movement[3] = True

                
                #Reset the game when pressing r key while player is dead
                if key == K_r and not self.player.isAlive:
                    self.reset()
                if key == K_q:
                    pg.quit()
                    sys.exit()
            # Keyup Press
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

                # REMOVE AFTER DEV
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
            
            #TODO: Game-ending condition 1 - player dead
            if self.player.check_collision_with_boss(self.boss):
                print("Player collided with the boss!")
                self.player.isAlive = False

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
            self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]), (self.down - self.up))) # self.up - self.down is just for flying around the map

            if self.player.on_ladder:
                self.player.update_ladder(self.movement[3] - self.movement[2])  # Update ladder movement separately

        
            # Update boss and other items here
            # TODO
            self.boss.update_animation()
            self.boss.update()
            

    # display the map to the screen
    def display_map(self, tmx_data, world_offset):
        for layer in tmx_data:
            if layer.name == "Foreground": continue
            # x,y,surface

            for tile in layer.tiles():
                x_pixel = tile[0] * 16 - world_offset[0]
                y_pixel = tile[1] * 16 - world_offset[1]

                # draw surface onto the screen
                self.screen.blit(tile[2], (x_pixel, y_pixel))

    def display_foreground(self, tmx_data, world_offset):
        # Lazy way to do it but its working for now
        for layer in tmx_data:
            if layer.name == "Foreground":
              for tile in layer.tiles():
                  x_pixel = tile[0] * 16 - world_offset[0]
                  y_pixel = tile[1] * 16 - world_offset[1]

                  # draw surface onto the screen
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
        # draw bg color before each loop
        self.screen.blit(self.map_bg, (0, 0))


        # draw the map
        self.display_map(self.tmx_data, render_offset)
        
        # DEV MODE enable map collision mode
        self.tilemap.draw(self.screen, render_offset)
        # Display books on screen
        player_rect = self.player.rect()
        self.book_manager.update(player_rect)
        self.book_manager.draw(self.screen, render_offset)

        self.player.draw(render_offset)

        self.display_foreground(self.tmx_data, render_offset)

        
        self.boss.draw(render_offset)
    
    #Display a text on the topright corner
    def render_text(self):
        # Check if cooldown is over
        if pg.time.get_ticks() - self.player.last_sprint_time < self.settings.sprint_cooldown:
            #The color is gray out when the sprint is not ready
            text_color = (128, 128, 128)
        else:
            #The color of text turn white when sprint is ready
            text_color = (255, 255, 255)

        #Change the font later
        font = pg.font.Font(None, 25)
        text = font.render("Sprint Ready!", True, text_color)
        text_rect = text.get_rect()
        #This make sure the text do not go out of the window
        text_rect.topright = (self.settings.screen_width - 20, 20)
        self.screen.blit(text, text_rect)

        books_text = font.render(f"Books Collected: {self.book_manager.total_collected_books}", True, (255, 255, 255))
        books_text_rect = books_text.get_rect(topright=(self.settings.screen_width - 20, 50))
        self.screen.blit(books_text, books_text_rect)
    
   
        
    #Game reset
    def reset(self):
        #reset the player
        self.player = Player(self, (2000, self.screen.get_size()[1] - 19), (8, 16))
        self.player.isAlive = True
        #reset the boss
        self.boss = Boss(self, self.player, (self.player.pos[0] - 100, self.screen.get_size()[1] - 19), (8, 16))
        #TODO:reset other game condition
        self.book_manager.reset()


if __name__ == "__main__":
    """Call py game.py to initiate and run the game"""
    level = Game()
    level.play()
