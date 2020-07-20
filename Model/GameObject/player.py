import pygame as pg
import math
import random
import Const
from Model.GameObject.entity import *

class Player:

    def __init__(self, player_id, player_name, is_AI):
        # basic
        self.player_name = player_name
        self.player_id = player_id
        self.is_AI = is_AI
        # status
        self.life = Const.PLAYER_LIFE
        self.attack_radius = Const.ATTACK_RADIUS
        self.player_radius = Const.PLAYER_RADIUS
        self.voltage = 0
        self.keep_item_id = Const.NO_ITEM
        self.invincible_time = 0
        self.invincible_battery_time = 0
        self.uncontrollable_time = 0
        self.attack_power = Const.ATTACK_POWER
        self.attack_cool_down_time = 0
        self.attack_cool_down = Const.ATTACK_COOL_DOWN_TIME
        self.jump_quota = Const.PLAYER_JUMP_QUOTA
        # move
        self.direction = pg.Vector2(1, 0)
        self.position = pg.Vector2(0, 0)
        self.velocity = pg.Vector2(Const.PLAYER_INIT_VELOCITY) # current velocity of user
        self.normal_speed = Const.PLAYER_INIT_SPEED # speed gain when players try to move left and right
        self.jump_speed =  Const.PLAYER_JUMP_SPEED # speed gain when players try to jump
        # others
        self.last_being_attacked_by = -1
        self.last_being_collided_with = -1
        self.last_being_attacked_time_elapsed = 0
        self.last_being_collided_time_elapsed = 0

        self.KO_amount = 0
        self.die_amount = 0

        self.KO_score = 0 # compute every tick
        self.die_score = 0 # compute every tick
        self.just_too_good_score = 0 # compute when timesup
        self.just_a_nerd_score = 0 # compute when timesup
        
        self.score = 0
        self.rank = 4

    def is_alive(self):
        return self.life > 0

    def is_invincible(self):
        return self.invincible_time > 0

    def is_controllable(self):
        return self.uncontrollable_time <= 0

    def can_attack(self):
        return self.attack_cool_down_time <= 0

    def has_item(self):
        return self.keep_item_id != Const.NO_ITEM

    def enhance(self, enhancement):
        self.attack_radius *= (1 + enhancement[Const.ATTACK_RADIUS_ENHANCEMENT_INDEX] * Const.ATTACK_RADIUS_ENHANCEMENT)
        self.normal_speed *= (1 + enhancement[Const.SPEED_ENHANCEMENT_INDEX] * Const.SPEED_ENHANCEMENT)
        self.attack_power *= (1 + enhancement[Const.ATTACK_POWER_ENHANCEMENT_INDEX] * Const.ATTACK_POWER_ENHANCEMENT)
        self.attack_cool_down *= (1 - enhancement[Const.ATTACK_COOL_DOWN_ENHANCEMENT_INDEX] * Const.ATTACK_COOL_DOWN_ENHANCEMENT)

    def set_position(self, position: pg.Vector2):
        self.position = pg.Vector2(position)

    def speed_function(self, time):
        return Const.PLAYER_SPEED_PARAMETER * time ** 2 + Const.PLAYER_FINAL_SPEED

    def update_every_tick(self, platforms: list, time):
        # Maintain normal speed
        self.maintain_speed_every_tick(time)

        # Maintain position
        self.move_every_tick()

        # Maintain horizontal and vertical velocity
        self.maintain_velocity_every_tick(platforms)

        # Maintain three timers
        self.maintain_timer_every_tick()

    def maintain_speed_every_tick(self, time):
        self.normal_speed = self.speed_function(time)

    def maintain_velocity_every_tick(self, platforms):
        self.velocity.y += Const.GRAVITY_ACCELERATION / Const.FPS
        unit = self.velocity.normalize()
        if self.is_controllable():
            # air drag (f = -kv => v = (1 - k/m) * v)
            self.velocity *= (1 - Const.DRAG_COEFFICIENT)
            # friction
            touch_platform = False
            for platform in platforms:
                if (platform.upper_left.y - self.position.y) < self.player_radius * 1.1 and\
                    platform.upper_left.x <= self.position.x <= platform.bottom_right.x:
                    touch_platform = True
                    break
            if touch_platform and self.velocity.x != 0:
                prev_velocity_x_dir = 1 if self.velocity.x > 0 else -1
                self.velocity.x -= prev_velocity_x_dir * Const.FRICTION_COEFFICIENT
                if self.velocity.x * prev_velocity_x_dir < 0:
                    self.velocity.x = 0

    def maintain_timer_every_tick(self):
        if self.invincible_time > 0:
            self.invincible_time -= 1
        if self.uncontrollable_time > 0:
            self.uncontrollable_time -= 1
        if self.attack_cool_down_time > 0:
            self.attack_cool_down_time -= 1
        if self.invincible_battery_time > 0:
            self.invincible_battery_time -= 1
            if self.invincible_battery_time == 0:
                self.player_radius /= Const.INVINCIBLE_BATTERY_PLAYER_RADIUS_RATIO
                self.attack_radius /= Const.INVINCIBLE_BATTERY_ATTACK_RADIUS_RATIO

    def move_every_tick(self):
        self.position += self.velocity / Const.FPS

    def maintain_score_every_tick(self):
        self.KO_score = self.KO_amount * 300
        self.die_score = -self.die_amount * 150
        self.score = self.KO_score + self.die_score

    def find_item_every_tick(self, items: list):
        # called by model update_players()
        for item in items:
            distance = (item.position - self.position).magnitude()
            if distance <= item.item_radius + self.player_radius:
                return item
        return None

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

    def overlap_resolved(self, other):
        distance = self.position - other.position
        if self.player_radius + other.player_radius <= distance.magnitude():
            return False
        if self.position.y < other.position.y:
            self.position.y = other.position.y - math.sqrt((self.player_radius + other.player_radius) ** 2 - (self.position.x - other.position.x) ** 2)
        else:
            other.position.y = self.position.y - math.sqrt((self.player_radius + other.player_radius) ** 2 - (self.position.x - other.position.x) ** 2)
        return True

    def bounce_reliable(self, collision_time):
        # Bounce when hitting platform for reliable version
        self.jump_quota = Const.PLAYER_JUMP_QUOTA
        self.position += self.velocity / Const.FPS * collision_time
        self.velocity.y *= -Const.ATTENUATION_COEFFICIENT
        self.position -= self.velocity / Const.FPS * collision_time
    
    def add_horizontal_velocity(self, direction: str):
        # EventPlayerMove
        if self.velocity.dot(Const.DIRECTION_TO_VEC2[direction]) > 0: # same direction
            if abs(self.velocity.x) <= self.normal_speed:
                self.velocity.x = self.normal_speed * Const.DIRECTION_TO_VEC2[direction].x
            else:
                pass
        else: # reverse direction
            self.velocity += self.normal_speed * Const.DIRECTION_TO_VEC2[direction]
        if direction == 'left':
            self.direction = pg.Vector2(-1, 0)
        elif (direction == 'right'):
            self.direction = pg.Vector2(1, 0)

    def jump(self):
        # EventPlayerJump
        if self.jump_quota > 0:
            self.velocity.y = -self.jump_speed
            self.jump_quota -= 1

    def attack(self, players, time):
        # EventPlayerAttack
        self.attack_cool_down_time = self.attack_cool_down
        for player in players:
            magnitude = (player.position - self.position).magnitude()
            # make sure that player is not self and player is alive and not invincible
            if player.player_id == self.player_id or not player.is_alive() or player.is_invincible():
                continue
            # attack if they are close enough
            if magnitude < self.attack_radius:
                unit = (player.position - self.position).normalize()
                player.be_attacked(unit, magnitude, self.attack_power, self.player_id, time)

    def be_attacked(self, unit, magnitude, attack_power, attacker_id, time):
        self.velocity += Const.BE_ATTACKED_ACCELERATION * self.voltage_acceleration() * attack_power * unit / magnitude / Const.FPS
        self.voltage += (Const.ATTACK_VOLTAGE_INCREASE / magnitude)
        self.last_being_attacked_by = attacker_id
        self.last_being_attacked_time_elapsed = time

    def be_attacked_by_pistol_bullet(self, unit, attacker_id, time):
        voltage_acceleration = self.voltage_acceleration()
        self.velocity += Const.BULLET_ACCELERATION * voltage_acceleration * unit / Const.FPS
        self.voltage += Const.BULLET_VOLTAGE_UP
        self.last_being_attacked_by = attacker_id
        self.last_being_attacked_time_elapsed = time

    def be_attacked_by_cancer_bomb(self, unit, magnitude, time):
        self.velocity += Const.BE_ATTACKED_ACCELERATION * unit / magnitude / Const.FPS
        self.voltage += Const.BOMB_ATK

    def be_attacked_by_zap_zap_zap(self, unit, attacker_id, time):
        voltage_acceleration = self.voltage_acceleration()
        self.voltage += Const.ZAP_ZAP_ZAP_OTHERS_VOLTAGE_UP
        self.velocity.y = -Const.ZAP_ZAP_ZAP_VERTICAL_ACCELERATION * voltage_acceleration / Const.FPS
        self.velocity.x = random.uniform(0, Const.ZAP_ZAP_ZAP_HORIZONTAL_ACCELERATION) * voltage_acceleration / Const.FPS \
                                            * (1 if unit.x > 0 else -1)
        self.last_being_attacked_by = attacker_id
        self.last_being_attacked_time_elapsed = time

    def voltage_acceleration(self):
        if self.voltage < 120:
            return 1 + self.voltage * Const.VOLTAGE_ACCELERATION_COEFFICIENT
        else:
            return 10 + self.voltage * Const.VOLTAGE_ACCELERATION_COEFFICIENT

    def die(self, players, time):
        # EventPlayerDied
        self.life -= 1
        self.die_amount += 1
        self.keep_item_id = Const.NO_ITEM
        if self.last_being_attacked_by != -1 and self.last_being_attacked_time_elapsed - time < Const.VALID_KO_TIME:
            players[self.last_being_attacked_by].KO_amount += 1
        elif self.last_being_collided_with != -1 and self.last_being_collided_time_elapsed - time < Const.VALID_KO_TIME:
            players[self.last_being_collided_with].KO_amount += 1

    def respawn(self, position: pg.Vector2):
        # EventPlayerRespawn
        # status
        if self.invincible_battery_time > 0:
            self.player_radius /= Const.INVINCIBLE_BATTERY_PLAYER_RADIUS_RATIO
            self.attack_radius /= Const.INVINCIBLE_BATTERY_ATTACK_RADIUS_RATIO
        self.voltage = 0
        self.invincible_time = Const.RESPAWN_INVINCIBLE_TIME
        self.uncontrollable_time = 0
        self.attack_cool_down_time = 0
        self.invincible_battery_time = 0
        self.jump_quota = Const.PLAYER_JUMP_QUOTA
        # move
        self.position = pg.Vector2(position)
        self.velocity = pg.Vector2(0, 0)
        # others
        self.last_being_attacked_by = -1
        self.last_being_collided_with = -1
        self.last_being_attacked_time_elapsed = 0
        self.last_being_collided_time_elapsed = 0

    def pick_item(self, item_id):
        self.keep_item_id = item_id
        
    def use_item(self, players, time):
        entities = []
        if self.keep_item_id == Const.BANANA_PISTOL:
            for angle in Const.BULLET_ANGLE:
                direction = self.direction.rotate(angle)
                pos = self.position + direction * (self.player_radius + Const.BULLET_RADIUS) * 1.02
                entities.append(PistolBullet(self.player_id, pos, direction * Const.BULLET_SPEED))
            pos = self.position - self.direction * (self.player_radius + Const.BANANA_PEEL_RADIUS) * 1.02 
            entities.append(BananaPeel(self.player_id, pos, pg.Vector2(0, 0)))

        elif self.keep_item_id == Const.BIG_BLACK_HOLE:
            entities.append(BigBlackHole(self.player_id, pg.Vector2(self.position)))

        elif self.keep_item_id == Const.CANCER_BOMB:
            entities.append(CancerBomb(self.player_id, pg.Vector2(self.position)))

        elif self.keep_item_id == Const.ZAP_ZAP_ZAP:
            self.voltage += Const.ZAP_ZAP_ZAP_SELF_VOLTAGE_UP
            for other in players:
                if abs(self.position.x - other.position.x) < Const.ZAP_ZAP_ZAP_RANGE and self != other\
                        and other.is_alive() and not other.is_invincible():
                    other.be_attacked_by_zap_zap_zap((other.position - self.position).normalize(), self.player_id, time)
                
        elif self.keep_item_id == Const.BANANA_PEEL:
            for angle, speed in zip(Const.BANANA_PEEL_DROP_ANGLE, Const.BANANA_PEEL_DROP_SPEED):
                if self.direction.x < 0:
                    direction = self.direction.rotate(angle)
                else:
                    direction = self.direction.rotate(-angle)
                pos = self.position + direction * (self.player_radius + Const.BANANA_PEEL_RADIUS) * 1.02
                entities.append(BananaPeel(self.player_id, pos, direction * speed))

        elif self.keep_item_id == Const.RAINBOW_GROUNDER:
            self.voltage -= Const.RAINBOW_GROUNDER_VOLTAGE_DOWN
            if self.voltage < 0:
                self.voltage = 0

        elif self.keep_item_id == Const.INVINCIBLE_BATTERY:
            if self.invincible_battery_time == 0:
                self.position.y -= (Const.INVINCIBLE_BATTERY_PLAYER_RADIUS_RATIO - 1) * self.player_radius
                self.player_radius *= Const.INVINCIBLE_BATTERY_PLAYER_RADIUS_RATIO
                self.attack_radius *= Const.INVINCIBLE_BATTERY_ATTACK_RADIUS_RATIO
            self.invincible_time = Const.INVINCIBLE_BATTERY_TIME
            self.invincible_battery_time = Const.INVINCIBLE_BATTERY_TIME

        self.keep_item_id = Const.NO_ITEM
        return entities
