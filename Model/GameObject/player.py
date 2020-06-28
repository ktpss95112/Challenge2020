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
        if abs(self.velocity.x) < Const.HORIZONTAL_SPEED_MINIMUM:
            self.velocity.x = 0
        elif self.velocity.x > 0:
            self.velocity.x -= self.velocity.x ** 2.5 * Const.DRAG_COEFFICIENT
            self.velocity.x = self.velocity.x if self.velocity.x > 0 else 0
        elif self.velocity.x < 0:
            self.velocity.x += (-self.velocity.x) ** 2.5 * Const.DRAG_COEFFICIENT
            self.velocity.x = self.velocity.x if self.velocity.x < 0 else 0

        # Modify the vertical velocity
        self.velocity.y += Const.GRAVITY_ACCELERATION / Const.FPS

        # Make sure that the player do not pass through the platform
        self.move(displacement, platforms)

        # Maintain self.invincible_time
        if self.invincible_time > 0:
            self.invincible_time -= 1
            if self.invincible_time == 0:
                self.player_radius = Const.PLAYER_RADIUS

    def collision(self, other, platforms: list):
        # Deal with collision with other player
        if (self.position - other.position).magnitude() >= (self.player_radius + other.player_radius) * 1.01:
            return
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
                    self.velocity.y = -self.velocity.y * Const.ATTENUATION_COEFFICIENT if abs(self.velocity.y) > Const.VERTICAL_SPEED_MINIMUM else 0
                    self.jump_quota = Const.PLAYER_JUMP_QUOTA
                    break

    def add_horizontal_velocity(self, direction: str):
        # Add horizontal velocity to the player along the direction.
        self.velocity += self.normal_speed * Const.DIRECTION_TO_VEC2[direction]

    def jump(self):
        # Add vertical velocity to the player.
        if self.jump_quota != 0:
            self.velocity.y = -self.jump_speed
            self.jump_quota -= 1

    def be_attacked(self , unit , magnitude):
        if self.invincible_time == 0:
            voltage_acceleration = self.voltage ** 1.35 + 100
            self.velocity += Const.BE_ATTACKED_ACCELERATION * voltage_acceleration * unit / magnitude / Const.FPS
            if self.voltage >= 100:
                self.velocity += Const.BE_ATTACKED_ACCELERATION * 10000 * unit / magnitude / Const.FPS
            self.voltage += (Const.VOLTAGE_INCREASE_CONST / magnitude)
        
    def respawn(self):
        self.position = pg.Vector2(Const.PLAYER_RESPAWN_POSITION[self.player_id])
        self.velocity = pg.Vector2(0, 0)
        self.voltage = 0
        self.jump_quota = Const.PLAYER_JUMP_QUOTA
        self.invincible_time = 2 * Const.FPS
    
    def use_item(self):
        if self.keep_item_id == Const.INVINCIBLE_BATTERY :
            self.position.y -= 2 * Const.PLAYER_RADIUS - self.player_radius
            self.player_radius = 2 * Const.PLAYER_RADIUS
            self.invincible_time = 5 * Const.FPS
        elif self.keep_item_id == Const.RAINBOW_GROUNDER :
            self.voltage -= 10
            if self.voltage < 0:
                self.voltage = 0
        self.keep_item_id = Const.NO_ITEM
