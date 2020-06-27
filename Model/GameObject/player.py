import pygame as pg
import Const

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.player_radius = Const.PLAYER_RADIUS
        self.last_being_attacked_by = -1
        self.last_being_attacked_time_elapsed = 0
        self.invincible_time = 0
        self.KO_amount = 0
        self.be_KO_amount = 0
        self.voltage = 0
        self.keep_item_id = Const.NO_ITEM
        self.position = pg.Vector2(Const.PLAYER_INIT_POSITION[player_id]) # is a pg.Vector2 (Const.PLAYER_INIT_POSITION is not update now!)
        self.velocity = pg.Vector2(Const.PLAYER_INIT_VELOCITY) # current velocity of user
        self.normal_speed = Const.PLAYER_NORMAL_SPEED # speed gain when players try to move left and right
        self.jump_speed =  Const.PLAYER_JUMP_SPEED # speed gain when players try to jump
        self.jump_quota = Const.PLAYER_JUMP_QUOTA

    def move_every_tick(self, platforms: list):
        # Calcultate the distance to move
        displacement = self.velocity / Const.FPS

        # Modify the horizontal velocity
        if self.velocity.x > 0:
            self.velocity.x -= Const.HORIZONTAL_ACCELERATION / Const.FPS
            self.velocity.x = self.velocity.x if self.velocity.x > 0 else 0
        elif self.velocity.x < 0:
            self.velocity.x += Const.HORIZONTAL_ACCELERATION / Const.FPS
            self.velocity.x = self.velocity.x if self.velocity.x < 0 else 0

        # Modify the vertical velocity
        self.velocity.y += Const.GRAVITY_ACCELERATION / Const.FPS

        # Make sure that the player do not pass through the platform
        self.move(displacement, platforms)

    def collision(self, other, platforms: list):
        # Collision with other player
        distance = other.position - self.position
        try:
            unit = distance.normalize()
        except ValueError:
            unit = pg.Vector2(-0.1, 0)

        # Modify velocity
        velocity_delta = (other.velocity.dot(unit) - self.velocity.dot(unit)) * unit
        self.velocity += velocity_delta
        other.velocity -= velocity_delta

        # Modify position
        displacement = -(self.player_radius + other.player_radius) * unit + distance
        self.move(displacement, platforms)
        other.move(-displacement, platforms)

    def move(self, displacement: pg.Vector2, platforms: list):
        # Move and check if collide with platform
        prev_position_y = self.position.y
        self.position += displacement
        for platform in platforms:
            if platform.upper_left.x <= self.position.x <= platform.bottom_right.x:
                if prev_position_y <= platform.upper_left.y - self.player_radius <= self.position.y:
                    self.position.y = platform.upper_left.y - self.player_radius
                    self.velocity.y = -self.velocity.y * Const.ATTENUATION_COEFFICIENT if abs(self.velocity.y) > Const.SPEED_MINIMUM else 0
                    self.jump_quota = Const.PLAYER_JUMP_QUOTA
                    break

    def add_horizontal_velocity(self, direction: str):
        '''
        Add horizontal velocity to the player along the direction.
        '''
        self.velocity += self.normal_speed * Const.DIRECTION_TO_VEC2[direction]

    def jump(self):
        '''
        Add vertical velocity to the player.
        '''
        if self.jump_quota != 0:
            self.velocity = self.jump_speed * pg.Vector2(0, -1)
            self.jump_quota -= 1

    def be_attacked(self , unit , magnitude):
        if magnitude > Const.BE_ATTACKED_MAX_ACCELERATION_DISTANCE:
            self.velocity += Const.BE_ATTACKED_ACCELERATION * unit / magnitude / Const.FPS
        else:
            self.velocity += Const.BE_ATTACKED_ACCELERATION * unit / Const.BE_ATTACKED_MAX_ACCELERATION_DISTANCE / Const.FPS
    
    def respawn(self):
        self.position = pg.Vector2(Const.PLAYER_RESTART_POSITION[self.player_id])
        self.velocity = pg.Vector2(0, 0)
        self.voltage = 0
    
    def use_item(self):
        self.keep_item_id = Const.NO_ITEM
