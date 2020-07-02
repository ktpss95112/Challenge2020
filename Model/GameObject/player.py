import pygame as pg
import Const
from Model.GameObject.entity import *

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.life = Const.PLAYER_LIFE
        self.player_radius = Const.PLAYER_RADIUS
        self.last_being_attacked_by = -1
        self.last_being_attacked_time_elapsed = 0
        self.invincible_time = 0
        self.KO_amount = 0
        self.can_not_control_time = 0
        self.be_KO_amount = 0
        self.voltage = 0
        self.direction = pg.Vector2(1,0)
        self.keep_item_id = Const.NO_ITEM
        self.position = pg.Vector2(Const.PLAYER_INIT_POSITION[player_id]) # is a pg.Vector2 (Const.PLAYER_INIT_POSITION is not update now!)
        self.velocity = pg.Vector2(Const.PLAYER_INIT_VELOCITY) # current velocity of user
        self.normal_speed = Const.PLAYER_NORMAL_SPEED # speed gain when players try to move left and right
        self.jump_speed =  Const.PLAYER_JUMP_SPEED # speed gain when players try to jump
        self.jump_quota = Const.PLAYER_JUMP_QUOTA
        self.score = 0

    def is_alive(self):
        return self.life > 0

    def move_every_tick(self, platforms: list):
        # Calcultate the distance to move
        displacement = self.velocity / Const.FPS

        # Modify the horizontal velocity
        if abs(self.velocity.x) < Const.HORIZONTAL_SPEED_MINIMUM:
            self.velocity.x = 0
        elif abs(self.velocity.x) > Const.DRAG_CRITICAL_SPEED:
            self.velocity.x /= 2
        elif self.velocity.x > 0 and self.can_not_control_time <= 0:
            self.velocity.x -= self.velocity.x ** 2.5 * Const.DRAG_COEFFICIENT
            self.velocity.x = self.velocity.x if self.velocity.x > 0 else 0
        elif self.velocity.x < 0 and self.can_not_control_time <= 0:
            self.velocity.x += (-self.velocity.x) ** 2.5 * Const.DRAG_COEFFICIENT
            self.velocity.x = self.velocity.x if self.velocity.x < 0 else 0

        # Modify the vertical velocity
        self.velocity.y += Const.GRAVITY_ACCELERATION / Const.FPS
        if self.velocity.y <= 2 * Const.VERTICAL_DRAG_EMERGE_SPEED:
            self.velocity.y /= 2
        elif self.velocity.y <= Const.VERTICAL_DRAG_EMERGE_SPEED:
            self.velocity.y = Const.VERTICAL_DRAG_EMERGE_SPEED

        # Make sure that the player do not pass through the platform
        self.move(displacement, platforms)
        
        # Maintain self.invincible_time
        if self.invincible_time > 0:
            self.invincible_time -= 1
            if self.invincible_time == 0:
                self.player_radius = Const.PLAYER_RADIUS

    def collision(self, other, platforms: list):
        # Deal with collision with other player
        distance = other.position - self.position
        try:
            unit = distance.normalize()
        except ValueError:
            unit = pg.Vector2(-0.1, 0)
        # Modify position
        if distance.magnitude() > (self.player_radius + other.player_radius) * 1.01: 
            return
        displacement = -(self.player_radius + other.player_radius) * unit + distance
        self.move(displacement, platforms)
        other.move(-displacement, platforms)

        # Modify velocity
        velocity_delta = (other.velocity.dot(unit) - self.velocity.dot(unit)) * unit
        self.velocity += velocity_delta
        other.velocity -= velocity_delta

    def collision_reliable(self, other, collision_time): # collsition time is a percentage of FPS
        # Collsion for reliable version
        self.position += self.velocity / Const.FPS * collision_time
        other.position += other.velocity / Const.FPS * collision_time
        unit = (other.position - self.position).normalize()
        velocity_delta = (other.velocity - self.velocity).dot(unit) * unit
        self.velocity += velocity_delta
        other.velocity -= velocity_delta
        self.position -= self.velocity / Const.FPS * collision_time
        other.position -= other.velocity / Const.FPS * collision_time

    def bounce_reliable(self, collision_time):
        # Bounce when hitting platform for reliable version
        self.jump_quota = Const.PLAYER_JUMP_QUOTA
        self.position += self.velocity / Const.FPS * collision_time
        self.velocity.y = -self.velocity.y * Const.ATTENUATION_COEFFICIENT
        self.position -= self.velocity / Const.FPS * collision_time

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
            if self.velocity.y > 0:
                self.velocity.y = -self.jump_speed
            else:
                self.velocity.y -= self.jump_speed
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
        self.last_being_attacked_by = -1
        self.last_being_attacked_time_elapsed = 0

    def use_item(self, players, entities):
        if self.keep_item_id == Const.INVINCIBLE_BATTERY:
            self.position.y -= 2 * Const.PLAYER_RADIUS - self.player_radius
            self.player_radius = 2 * Const.PLAYER_RADIUS
            self.invincible_time = 5 * Const.FPS
        
        elif self.keep_item_id == Const.RAINBOW_GROUNDER:
            self.voltage -= 10
            if self.voltage < 0:
                self.voltage = 0
        
        elif self.keep_item_id == Const.BANANA_PISTOL:
            pos = self.position + self.direction * ( self.player_radius + Const.BULLET_RADIUS) * 1.02
            entities.append( PistolBullet(pos, self.direction) )

            pos = self.position - self.direction * ( self.player_radius + Const.BANANA_PEEL_RADIUS) * 1.02 
            entities.append( BananaPeel(pos))

        elif self.keep_item_id == Const.CANCER_BOMB:
            entities.append( CancerBomb(pg.Vector2(self.position.x,self.position.y)) )
        
        elif self.keep_item_id == Const.BANANA_PEEL:
            pos = self.position - self.direction * ( self.player_radius + Const.BANANA_PEEL_RADIUS) * 1.02 
            entities.append( BananaPeel(pos))
             
        elif self.keep_item_id == Const.ZAP_ZAP_ZAP:
            self.voltage += 10
            for other in players :
                if abs( self.position.x - other.position.x ) < Const.ZAP_ZAP_ZAP_RANGE * self.player_radius and self != other\
                        and other.is_alive() and other.invincible_time <= 0:
                    other.voltage += 50

        elif self.keep_item_id == Const.BIG_BLACK_HOLE:
            entities.append( BigBlackHole(pg.Vector2(self.position.x, self.position.y), self.player_id) )
        self.keep_item_id = Const.NO_ITEM
