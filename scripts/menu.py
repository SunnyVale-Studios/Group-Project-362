import pygame as pg

""" Have a main menu, where the player, can start the game, settings, exit and a info tab to tell the player how to play the game (images or text) """
class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.buttons = {
            "start_button" : Button(self, (self.screen_rect.centerx - 50, 30), (100, 50)),
            "settings_button" : Button(self, (self.screen_rect.centerx - 50, 100), (100, 50)),
            "exit_button" : Button(self, (self.screen_rect.centerx - 50, 180), (100, 50)),
            "info_button" : Button(self, (self.screen_rect.right - 240, self.screen_rect.bottom - 120), (100, 100)),
            "audio_button" : Button(self, (self.screen_rect.right - 120, self.screen_rect.bottom - 120), (100, 100))
        }

    def buttonPress(self, button):
        # Trigger when one of the itmes get selected
        pass

    def update(self):
        # Continoulsy check for user input on the buttons or
        for button in self.buttons.values():
            button.draw()

### Create buttons with generic functions
class Button:
    def __init__(self, menu, pos, size):
        self.menu = menu
        self.rect = pg.Rect(pos, size)
        
    
    def buttonPress(self):
        pass

    def update(self):
        pass

    def draw(self):
        pg.draw.rect(self.menu.screen, (255, 255, 255), self.rect)
    