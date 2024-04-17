class Settings:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = int(self.screen_width * 0.8) # 1:.8
        self.fps = 60
        self.x_velocity = 3.0 # Just to make travseing faster before sprint is implemented
        self.jump_velocity = 5.0

if __name__ == "__main__":
    print("Incorrect file ran! Run python3 game.py")