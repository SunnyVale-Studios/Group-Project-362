import pygame as pg

""" Have a main menu, where the player, can start the game, settings, exit and a info tab to tell the player how to play the game (images or text) """
class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.main_menu_buttons = {
            "game_title" : Button(self, (self.screen_rect.centerx - 300, self.screen_rect.top + 30), (600, 100)),
            "start_button" : Button(self, (self.screen_rect.centerx - 150, self.screen_rect.centery - 200), (300, 100)),
            "settings_button" : Button(self, (self.screen_rect.centerx - 150, self.screen_rect.centery - 50), (300, 100)),
            "exit_button" : Button(self, (self.screen_rect.centerx - 150, self.screen_rect.centery + 100), (300, 100)),
            "info_button" : Button(self, (self.screen_rect.right - 240, self.screen_rect.bottom - 120), (100, 100)),
            "audio_button" : Button(self, (self.screen_rect.right - 120, self.screen_rect.bottom - 120), (100, 100))
        }

        self.reset_menu_buttons = {
            "reset_button" : Button(self, (self.screen_rect.centerx - 150, self.screen_rect.centery - 50), (300, 100))
        }

        self.pause_menu_buttons = {
            "quit_button" : Button(self, (self.screen_rect.centerx - 150, self.screen_rect.centery - 50), (300, 100)),
            "audio_button" : Button(self, (self.screen_rect.right - 120, self.screen_rect.bottom - 120), (100, 100))
        }

        

    def buttonPress(self, button):
        # Trigger when one of the itmes get selected
        pass

    def update(self):
        # Continoulsy check for user input on the buttons or
        if not self.game.started:
            for button in self.main_menu_buttons.values():
                button.update()
        elif not self.game.player.isAlive:
            for button in self.reset_menu_buttons.values():
                button.update()
        elif self.game.paused:
            
            for button in self.pause_menu_buttons.values():
                button.update()

### Create buttons with generic functions
class Button:
    def __init__(self, menu, pos, size):
        self.menu = menu
        self.rect = pg.Rect(pos, size)
        
    
    def buttonPress(self):
        pass

    def update(self):
        # TODO - Check for interaction with the button only when visible

        # Draw
        self.draw()

    def draw(self):
        pg.draw.rect(self.menu.screen, (255, 255, 255), self.rect)
    