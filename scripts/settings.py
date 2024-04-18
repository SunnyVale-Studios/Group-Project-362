class Settings:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = int(self.screen_width * 0.8) # 1:.8
        self.fps = 60
        self.x_velocity = 3.0
        self.y_velocity = 0.5
        self.max_gravity = 10
        self.friction = 0.2
        self.jump_velocity = 11.0
        self.sprint_distance = 80 #change sprint distance
        self.sprint_speed = 3 #sprinting spped
        self.sprint_cooldown = 3000 #sprint cooldown - 3 seconds
       

if __name__ == "__main__":
    print("Incorrect file ran! Run py game.py")
