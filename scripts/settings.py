class Settings:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = int(self.screen_width * 0.8)
        self.fps = 60
        self.gravity = 1 # not used
        self.acceleration = 1.5 #not used
        self.friction = -0.3 #not used
        self.max_velocity = 10.0 #not used
        self.jump_velocity = 15.0 #not used

        # world_offset to move the map as the player reaches the edges
        # [x,y]; -100 allows player to see underneath more but can be changed later
        self.world_offset = [-5, -32] # not used


if __name__ == "__main__":
    print("Wrong file to run game. Run game.py instead!!")
