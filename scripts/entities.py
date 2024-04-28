import pygame as pg
from scripts.timer import Timer
from scripts.utils import load_images

class PhysicsEntity:
    def __init__(self, game, type, pos, size):
        '''DEVELOPMENT VARIABLES ONLY DONT KEEP IN FINAL ITERATION'''

        self.creativeMode = False
        '''END OF DEV'''
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.type = type
        self.size = size
        self.pos = list(pos) # Figure out why other than just making a new variable

        self.velocity = pg.Vector2(0, 0)
        self.last_velocity = pg.Vector2(0, 0)
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.isJumping = False
        self.isAlive = True # Used later to determine whether game is over

        self.anim_offset = (-16, -20)

        # Animation list
        self.animations = {
            "idle": Timer(load_images("idle", self.size[1] // 16), "idle"),
            "run": Timer(load_images("run", self.size[1] // 16), "run"),
            "jump": Timer(load_images("jump", self.size[1] // 16), "jump", is_loop=False),
            "sprint": Timer(load_images("sprint", self.size[1] // 16), "sprint"),
        }

        self.current_animation = self.animations["idle"]
        self.flip = False

    def update_animation(self):
        self.current_animation.next_frame()

    def set_action(self, action):
        # check if the new action is different from the previous one
        if action != self.current_animation.action:
            self.current_animation = self.animations[action]
            self.current_animation.reset()

    # def rect(self):
    #     return pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


    # used for collecting books bc default rect was not working
    def rect(self, offset=(0,0)):
        return pg.Rect(self.pos[0] - offset[0], self.pos[1]-offset[1], self.size[0], self.size[1])


    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
    
        if self.creativeMode:
            # This will ignore velocity and just input straight direction movement to fly around map
            # had to add this change as adding one way change broke the logic for some reason
            frame_movement = (movement[0] * 10, movement[1] * 10)
            self.pos[0] += frame_movement[0]
            self.pos[1] += frame_movement[1]
        else:
            # In-game movement physics
            if movement[0] != 0:
                # Constant velocity when user inputs movement
                self.velocity[0] = movement[0] * self.settings.x_velocity
    
            if self.isJumping:
                # We want to make sure while in the air the velocity of the player is only dependent on the last velocity he was in and not the movement
                self.velocity[0] = movement[0] * 2 * self.settings.x_velocity
            else:
                self.velocity[0] = self.velocity[0] - self.settings.friction if self.velocity[0] > 1 else self.velocity[0] + self.settings.friction if self.velocity[0] < -1 else 0
                self.last_velocity[0] = self.velocity[0]
    
            frame_movement = (self.velocity[0], self.velocity[1])
    
            self.pos[0] += frame_movement[0]
            entity_rect = self.rect()
            oneway_rects = tilemap.oneway_rects_around(self.pos)
            for rect in tilemap.physics_rects_around(self.pos):
                if entity_rect.colliderect(rect):
                    if rect not in oneway_rects:
                        if frame_movement[0] > 0:
                            entity_rect.right = rect.left
                            self.collisions['right'] = True
                        if frame_movement[0] < 0:
                            entity_rect.left = rect.right
                            self.collisions['left'] = True
                        self.pos[0] = entity_rect.x
    
            self.pos[1] += frame_movement[1]
            entity_rect = self.rect()
            oneway_rects = tilemap.oneway_rects_around(self.pos)
            for rect in tilemap.physics_rects_around(self.pos):
                if entity_rect.colliderect(rect):
                    if rect not in oneway_rects or self.velocity[1] >= 0:
                        if frame_movement[1] > 0:
                            entity_rect.bottom = rect.top
                            self.collisions['down'] = True
                        if frame_movement[1] < 0:
                            entity_rect.top = rect.bottom
                            self.collisions['up'] = True
                        self.pos[1] = entity_rect.y
    
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
    
        self.velocity[1] = min(self.settings.max_gravity, self.velocity[1] + self.settings.y_velocity)
    
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
    
        self.animations.update()

    def draw(self, offset=(0, 0)):
        self.screen.blit(pg.transform.flip(self.current_animation.image(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]) )


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0 # For jumping animation

        self.last_sprint_time = 0
        self.is_sprinting = False
        self.sprint_end_pos = None
        #add a sound to notify the player when the sprint is ready
        self.sprint_sound = pg.mixer.Sound('./assets/Sound/sprint-ready.wav')
        #temp set the volume of the sound to 50%
        self.sprint_sound.set_volume(0.5)
        #a flag make sure the sound only play once
        self.sprint_sound_played = False
        self.on_ladder = False


    def update(self, tilemap, movement=(0, 0)):
        # Check if sprint key is pressed and cooldown is over
        keys = pg.key.get_pressed()
        # Sprint active when cooldown is over
        if keys[pg.K_LSHIFT] and pg.time.get_ticks() - self.last_sprint_time > self.settings.sprint_cooldown:
            self.is_sprinting = True
            # TODO - Play a sound effect for sprinting
            self.last_sprint_time = pg.time.get_ticks()
            #set sprint end position base on sprint_distance
            self.sprint_end_pos = self.pos[0] + self.settings.sprint_distance if not self.flip else self.pos[0] - self.settings.sprint_distance
        #play sprint ready sound
        if not self.is_sprinting and pg.time.get_ticks() - self.last_sprint_time > self.settings.sprint_cooldown:
            if not self.sprint_sound_played: #check if the sound has been played
                self.sprint_sound.play()
                self.sprint_sound_played = True
        #make sure the sound only play once per cooldown
        elif self.is_sprinting or pg.time.get_ticks() - self.last_sprint_time < self.settings.sprint_cooldown:
            self.sprint_sound_played = False

        if not self.is_sprinting:
            # Check if the player is on a climbable tile
            if any(tile['type'] == 'climbable' for tile in tilemap.tiles_around(self.pos)):
                self.on_ladder = True
            else:
                self.on_ladder = False

            if not self.on_ladder:
                # Player is not on a climbable tile, apply regular movement
                super().update(tilemap, movement=movement)
            else:
                # Player is on a climbable tile, allow movement onto the ladder
                self.pos[0] += movement[0] * self.settings.x_velocity

                # Check for collisions with platform tiles while on a ladder
                entity_rect = self.rect()
                for rect in tilemap.physics_rects_around(self.pos):
                    if entity_rect.colliderect(rect) and rect.top < self.pos[1] < rect.bottom:
                        # Player collides with a platform tile while on a ladder
                        if movement[1] < 0:  # Moving upward
                            entity_rect.top = rect.bottom
                        elif movement[1] > 0:  # Moving downward
                            entity_rect.bottom = rect.top
                        self.pos[1] = entity_rect.y
                self.pos[1] += self.velocity[1]
        else:
            #move player's location base on sprint_speed
            self.pos[0] += self.settings.x_velocity * self.settings.sprint_speed if not self.flip else -self.settings.x_velocity * self.settings.sprint_speed
            #set sprint termination
            if (not self.flip and self.pos[0] >= self.sprint_end_pos) or (self.flip and self.pos[0] <= self.sprint_end_pos):
                self.is_sprinting = False
                self.pos[0] = self.sprint_end_pos
            #sprint animation
            self.set_action('sprint')

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.isJumping = False

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
        
    def update_ladder(self, vertical_movement):
        if self.on_ladder:
            # Player is on a climbable tile, allow vertical movement
            self.pos[1] += vertical_movement * self.settings.climb_speed
            # Reset vertical velocity to prevent gravity from affecting the player on the ladder
            self.velocity[1] = 0 

            if self.pos[0] > 3473:
                self.pos[0] = 3473


    def rect(self, offset=(0, 0)):
        return super().rect(offset)
    
    def check_collision_with_boss(self, boss):
        return self.rect().colliderect(boss.rect())

class Boss(PhysicsEntity):
    def __init__(self, game, player, pos, size):
        super().__init__(game, 'boss', pos, size)
        self.player = player
        self.boost_end_time = 0
        self.cooldown_end_time = 0
        self.is_boosted = False

        # Animation list
        self.boss_animations = {
            "walk": Timer(self.load_boss_images("walk", self.size[1] // 16), "walk"),
        }

        self.current_animation = self.boss_animations["walk"]
        self.flip = False
        self.start_chasing_time = pg.time.get_ticks() + 5000

    def load_boss_images(self, boss_animation_name, scale):
        # Define base path for boss imgs
        Base_Boss_Path = "assets/Boss/Walk/"
        # Load all images for the boss
        temp_list = []
        # Count number of files in the folder
        boss_num_of_frames = 16  # There are 16 frames for the boss animation
        for i in range(boss_num_of_frames):
            # Load boss img
            boss_img = pg.image.load(
                Base_Boss_Path
                + f"boss-{boss_animation_name}-{str(i).zfill(2)}-1.3.png"
            ).convert_alpha()
            # Scale boss img if needed
            boss_img = pg.transform.scale(
                boss_img, (int(boss_img.get_width() * scale), int(boss_img.get_height() * scale))
            )
            temp_list.append(boss_img)
        return temp_list
    
    def update(self):
        if pg.time.get_ticks() >= self.start_chasing_time:
            direction = pg.Vector2(self.player.pos) - pg.Vector2(self.pos)
            distance = direction.length()
            speed = self.settings.boss_speed
            current_time = pg.time.get_ticks()
            
            if distance > 0:
                direction = direction.normalize()
            
            #Boss boost if distance exceeds 400 and cooldown is over
            if distance > 400 and current_time > self.cooldown_end_time and not self.is_boosted:
                self.boost_end_time = current_time + self.settings.boost_duration
                self.is_boosted = True
            #After boosting, enter cooldown
            if self.is_boosted and current_time > self.boost_end_time:
                self.cooldown_end_time = current_time + self.settings.boost_cooldown
                self.is_boosted = False
            #If boosting, increase speed
            #TODO: add sound effect when boss start boosting
            if self.is_boosted:
                speed += self.settings.boss_speed_boost
            #Speed return to normal is distance less than 100
            if distance < 100:
                speed = self.settings.boss_speed
                
            #Update boss's position
            self.pos[0] += direction.x * speed
            self.pos[1] += direction.y * speed
            
            #Flip the boss's imgs depends on the player's position
            self.flip = self.player.pos[0] < self.pos[0]
            
            print(f"Current distance to player: {distance}")
            print(f"Current speed: {speed}")
            
        self.update_animation()

if __name__ == "__main__":
    print("Incorrect file ran! Run python3 game.py")
