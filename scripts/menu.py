import pygame as pg

""" Have a main menu, where the player, can start the game, settings, exit and a info tab to tell the player how to play the game (images or text) """
class Menu:
    def __init__(self, game):
        self.game = game
        self.game
    

    def buttonPress(self, button):
        # Trigger when one of the itmes get selected
        pass

    def update(self):
        # Continoulsy check for user input on the buttons or
        pass


    def draw(self):
        # Update
        pass

### Create buttons with generic functions
class Button:
    def __init__(self, game, pos, size, function):
        self.game = game
        self.pos = pos
        self.size = size
        self.function = function
    
    def buttonPress(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass
    