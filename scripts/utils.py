import pygame as pg
import os

def load_images( animation_name, scale):
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

