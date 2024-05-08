import pygame as pg
import time

class EndGame:
    def __init__(self, game):
        self.game = game
        self.start_time = None
        self.font = pg.font.Font(None, 50)
        self.sound_played = False
        self.image = pg.image.load('./assets/Boss/boss-on-fire.png')
        self.sound1 = pg.mixer.Sound('./assets/Sound/boss-death-sound.wav')
        self.sound2 = pg.mixer.Sound('./assets/Sound/fire-sound.wav')
        self.sound1_played = False
        self.sound2_played = False
        self.channel1 = pg.mixer.Channel(0)
        self.channel2 = pg.mixer.Channel(1)

    def display_end_game_text(self):
        if not self.start_time:
            self.start_time = time.time()
        elapsed_time = time.time() - self.start_time

        if elapsed_time < 15:  # Display for 15 seconds
            # Calculate the time used to collect all books
            time_used = (self.game.end_time - self.game.start_time) / 1000
            minutes = time_used // 60
            seconds = time_used % 60
            
            if not self.sound1_played and not self.sound2_played:
                self.channel1.play(self.sound1) 
                self.channel2.play(self.sound2)
                self.sound1_played = True
                self.sound2_played = True
                
            self.game.screen.blit(self.image, (self.game.settings.screen_width // 2 - self.image.get_width() // 2, self.game.settings.screen_height // 2 - self.image.get_height() // 2))
            text1 = self.font.render("The Power of Magic Books Condensed Into Flames", True, (48, 243, 255))
            text2 = self.font.render("Monster Shattered Into Ashes Amid Its Scream of Pain", True, (48, 243, 255))
            text3 = self.font.render("With Wisdom and Courage", True, (48, 243, 255))
            text4 = self.font.render("You Successfully Escaped From The Dark Forest", True, (48, 243, 255))
            text5 = self.font.render(f"Time Taken: {int(minutes)} mins {int(seconds)} secs", True, (48, 243, 255))
            self.game.screen.blit(text1, (self.game.settings.screen_width // 2 - text1.get_width() // 2, self.game.settings.screen_height // 2 - text1.get_height() // 2 - 70))
            self.game.screen.blit(text2, (self.game.settings.screen_width // 2 - text2.get_width() // 2, self.game.settings.screen_height // 2 - text2.get_height() // 2 - 10))
            self.game.screen.blit(text3, (self.game.settings.screen_width // 2 - text3.get_width() // 2, self.game.settings.screen_height // 2 - text3.get_height() // 2 + 50))
            self.game.screen.blit(text4, (self.game.settings.screen_width // 2 - text4.get_width() // 2, self.game.settings.screen_height // 2 - text4.get_height() // 2 + 110))
            self.game.screen.blit(text5, (self.game.settings.screen_width // 2 - text5.get_width() // 2, self.game.settings.screen_height // 2 - text5.get_height() // 2 + 170))
            
            # Play the sound only once
            if not self.sound_played:
                pg.mixer.Sound('./assets/Sound/happy-ending.wav').play()
                self.sound_played = True
        else:
            # Directly draw the reset menu buttons and update them
            for button in self.game.menu.reset_menu_buttons:
                button.draw()
                button.update(pg.mouse.get_pos(), self.game.wasClicked, self.game.isClicked)