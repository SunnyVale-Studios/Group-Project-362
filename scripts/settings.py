class Settings:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = int(self.screen_width * 0.8)
        self.fps = 60
        self.gravity = 1
        self.acceleration = 0.5
        self.friction = -0.3
        self.max_velocity = 4.0
        self.move_left = 0
        self.move_right = 0

        # world_offset to move the map as the player reaches the edges
        # [x,y]; -100 allows player to see underneath more but can be changed later
        self.world_offset = [-5, -100]


if __name__ == "__main__":
    print("Wrong file to run game. Run game.py instead!!")
