import pygame as pg
import os
from pygame.sprite import Sprite
from scripts.timer import Timer
from scripts.settings import Settings


class Player(Sprite):
    def __init__(self, game, x, y, scale):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.world_offset = self.settings.world_offset
        # Set player status, use later
        self.alive = True
        self.velocity = pg.Vector2(0, 0)
        # Set Jump
        self.jump = False
        # Jump condition, in-air or not
        self.in_air = True
        # vertical velocity
        self.vel_y = 0

        # Animation list
        self.animations = {
            "idle": Timer(self.load_images("idle", scale), "idle"),
            "run": Timer(self.load_images("run", scale), "run"),
            "jump": Timer(self.load_images("jump", scale), "jump"),
        }
        self.current_animation = self.animations["idle"]
        # Set player location
        self.rect = self.current_animation.image().get_rect()
        self.rect.center = (x, y)
        # Set player direction
        self.direction = 1

        self.map_bg = pg.transform.scale(
            pg.image.load("./assets/Map/main_background.png").convert_alpha(),
            (self.settings.screen_width, self.settings.screen_height),
        )

    def load_images(self, animation_name, scale):
        # Define base path for player imgs
        Base_Player_Path = "assets/Adventurer/Indvidual Sprites/"
        # Load all images for the player
        temp_list = []
        # Count number of files in the folder
        num_of_frames = len(os.listdir(Base_Player_Path + f"{animation_name}"))
        for i in range(num_of_frames):
            # Load player img
            img = pg.image.load(
                Base_Player_Path
                + f"{animation_name}/adventurer-{animation_name}-0{i}-1.3.png"
            ).convert_alpha()
            # Scale player img if needed
            img = pg.transform.scale(
                img, (int(img.get_width() * scale), int(img.get_height() * scale))
            )
            temp_list.append(img)
        return temp_list

    def update_animation(self):
        self.current_animation.next_frame()

    # Set player's movement
    def move(self):
        # Horizontal Movement
        self.velocity.x += (
            self.settings.move_right - self.settings.move_left
        ) * self.settings.acceleration
        # Moving direction
        if self.velocity.x > 0:
            self.direction = 1
        elif self.velocity.x < 0:
            self.direction = -1

        # Jump setting
        if self.jump and self.in_air == False:
            # jump height
            self.vel_y = -8
            # inital state
            self.jump = False
            self.in_air = True

        # Apply gravity
        self.vel_y += self.settings.gravity
        # Prevent player from falling out of the window
        if self.rect.bottom + self.vel_y > self.settings.screen_height:
            self.vel_y = self.settings.screen_height - self.rect.bottom
            self.in_air = False
        self.rect.y += self.vel_y

        # Apply move friction
        if self.velocity.x != 0:
            self.velocity.x += self.velocity.x * self.settings.friction
        # Set velocity cap
        if abs(self.velocity.x) > self.settings.max_velocity:
            self.velocity.x = (
                self.settings.max_velocity
                if self.velocity.x > 0
                else -self.settings.max_velocity
            )

        # Set movement boundary
        if self.rect.left + self.velocity.x < 0:
            # -5 is the end of the left boundary
            if self.world_offset[0] > -5:
                self.world_offset[0] += 0
            else:
                # move camera left
                self.rect.left = 0
                self.world_offset[0] += 1

        elif self.rect.right + self.velocity.x > self.settings.screen_width:
            # -2520 is the end of the right boundary
            if self.world_offset[0] < -2518:
                self.world_offset[0] -= 0
            else:
                # move camera right
                self.world_offset[0] -= 1
                self.rect.right = self.settings.screen_width
        else:
            self.rect.x += self.velocity.x

    def update_action(self, new_action):
        # check if the new action is different from the previous one
        if new_action != self.current_animation.action:
            self.current_animation = self.animations[new_action]
            self.current_animation.reset()

    # draw players on the screen
    def draw(self):
        # Flip the image if moving to the left
        if self.direction == -1:
            self.screen.blit(
                pg.transform.flip(self.current_animation.image(), True, False),
                self.rect,
            )
        else:
            self.screen.blit(self.current_animation.image(), self.rect)

    def draw_BG(self):
        # redraw backround to cover up previous animations
        self.screen.blit(self.map_bg, (0, 0))


if __name__ == "__main__":
    print("Wrong file to run game. Run game.py instead!!")
