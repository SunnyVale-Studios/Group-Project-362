import pygame as pg
import sys




""" Have a main menu, where the player, can start the game, settings, exit and a info tab to tell the player how to play the game (images or text) """
class Menu:
    def __init__(self, game):
        self.font = pg.font.SysFont(None, 48)
        self.title = pg.font.SysFont(None, 72)
        self.text_color = (0, 0, 0)
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.main_menu_buttons = [
            Button(self, 0, (self.screen_rect.centerx - 200, self.screen_rect.top + 40), (400, 100)),
            Button(self, 1, (self.screen_rect.centerx - 100, self.screen_rect.centery - 200), (200, 75)),
            Button(self, 2, (self.screen_rect.centerx - 100, self.screen_rect.centery - 50), (200, 75)),
            Button(self, 3, (self.screen_rect.centerx - 100, self.screen_rect.centery + 100), (200, 75)),
            Button(self, 4, (self.screen_rect.right - 240, self.screen_rect.bottom - 120), (100, 100)),
            Button(self, 5, (self.screen_rect.right - 120, self.screen_rect.bottom - 120), (100, 100))
        ]

        self.reset_menu_buttons = [
            Button(self, 6, (self.screen_rect.centerx - 100, self.screen_rect.centery - 50), (200, 75)),
            Button(self, 3, (self.screen_rect.centerx - 100, self.screen_rect.centery + 100), (200, 75))
        ]

        self.pause_menu_buttons = [
            Button(self, 6, (self.screen_rect.centerx - 100, self.screen_rect.centery - 50), (200, 75)),
            Button(self, 3, (self.screen_rect.centerx - 100, self.screen_rect.centery + 100), (200, 75)),
            Button(self, 5, (self.screen_rect.right - 120, self.screen_rect.bottom - 120), (100, 100))
        ]

    def update(self):
        # Continoulsy check for user input on the buttons or
        mouse = pg.mouse.get_pos()
        clicked = pg.mouse.get_pressed()[0]
        if not self.game.started:
            for button in self.main_menu_buttons:
                button.update(mouse, clicked)
        elif not self.game.player.isAlive and self.game.player.jumpscare_image.get_alpha() == 0:
            for button in self.reset_menu_buttons:
                button.update(mouse, clicked)
        elif self.game.paused:
            
            for button in self.pause_menu_buttons:
                button.update(mouse, clicked)

### Create buttons with generic functions
class Button:
    buttons = {
        0:["game_title", "The Lost Pages"],
        1:["start_button", "Start"],
        2:["settings_button", "Settings"],
        3:["exit_button", "Quit"],
        4:["info_button", "i"],
        5:["audio_button", ""],
        6:["reset_button", "Reset"]
    }
    def __init__(self, menu, button, pos, size):
        self.menu = menu
        self.button = button
        self.rect = pg.Rect(pos, size)
        self.selected = False
        if button == 0:
            self.text = menu.title.render(Button.buttons[button][1], True, (255, 255, 255))
        else:
            self.text = menu.font.render(Button.buttons[button][1], True, menu.text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center
        
    def buttonPress(self):
        match self.button:
            case 0:
                print("This is title. Nothing here???")
                pass
            case 1:
                if not self.menu.game.started:
                    self.menu.game.started = True
                pass
            case 2:
                print("Open Settings")
                pass
            case 3:
                pg.quit()
                sys.exit()
                pass
            case 4:
                print("Info about Game")
                pass
            case 5:
                print("Toggle Audio")
                # Change photo from audio to audio slashed(muted)
                pass
            case 6:
                self.menu.game.reset()
                pass

    def update(self, mouse_pos, isClicked):
        # TODO - Check for interaction with the button only when visible
        if not self.selected and self.rect.collidepoint(mouse_pos):
            self.selected = True
        if self.selected and not self.rect.collidepoint(mouse_pos):
            self.selected = False
        if isClicked:
            if self.rect.collidepoint(mouse_pos):
                self.buttonPress()
        # Draw
        self.draw()

    def draw(self):
        if self.button != 0:
            pg.draw.rect(self.menu.screen, (174, 120, 81) if not self.selected else (223, 159, 94), self.rect)
        self.menu.screen.blit(self.text, self.text_rect)