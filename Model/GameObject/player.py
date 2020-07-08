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
        self.uncontrollable_time = 0
        self.attack_cool_down_time = 0
        self.jump_quota = Const.PLAYER_JUMP_QUOTA
        # move
        self.direction = pg.Vector2(1,0)
        self.position = pg.Vector2(0, 0)
        self.velocity = pg.Vector2(Const.PLAYER_INIT_VELOCITY) # current velocity of user
        self.normal_speed = Const.PLAYER_INIT_SPEED # speed gain when players try to move left and right
        self.jump_speed =  Const.PLAYER_JUMP_SPEED # speed gain when players try to jump
        # others
        self.last_being_attacked_by = -1
        self.last_being_attacked_time_elapsed = 0
        self.KO_amount = 0
        self.be_KO_amount = 0
        self.score = 0

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
        self.jump_speed *= (1 + enhancement[Const.JUMP_ENHANCEMENT_INDEX] * Const.JUMP_ENHANCEMENT)

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
        self.maintain_velocity_every_tick()

        # Maintain three timers
        self.maintain_timer_every_tick()

    def maintain_speed_every_tick(self, time):
        self.normal_speed = self.speed_function(time)

    def maintain_velocity_every_tick(self):
        # Modify the horizontal velocity (drag)
        if abs(self.velocity.x) < Const.HORIZONTAL_SPEED_MINIMUM:
            self.velocity.x = 0
        elif abs(self.velocity.x) > Const.DRAG_CRITICAL_SPEED:
            self.velocity.x /= 2
        elif self.velocity.x > 0 and self.is_controllable():
            self.velocity.x -= self.velocity.x ** 2.5 * Const.DRAG_COEFFICIENT
            self.velocity.x = self.velocity.x if self.velocity.x > 0 else 0
        elif self.velocity.x < 0 and self.is_controllable():
            self.velocity.x += (-self.velocity.x) ** 2.5 * Const.DRAG_COEFFICIENT
            self.velocity.x = self.velocity.x if self.velocity.x < 0 else 0

        # Modify the vertical velocity (drag and gravity)
        self.velocity.y += Const.GRAVITY_ACCELERATION / Const.FPS
        if self.velocity.y <= 2 * Const.VERTICAL_DRAG_EMERGE_SPEED:
            self.velocity.y /= 2
        elif self.velocity.y <= Const.VERTICAL_DRAG_EMERGE_SPEED:
            self.velocity.y = Const.VERTICAL_DRAG_EMERGE_SPEED

    def maintain_timer_every_tick(self):
        if self.invincible_time > 0:
            self.invincible_time -= 1
            if self.invincible_time == 0:
                self.player_radius = Const.PLAYER_RADIUS
        if self.uncontrollable_time > 0:
            self.uncontrollable_time -= 1
        if self.attack_cool_down_time > 0:
            self.attack_cool_down_time -= 1

    def move_every_tick(self):
        self.position += self.velocity / Const.FPS

    def find_item_every_tick(self, items: list):
        # called by model update_players()
        for item in items:
            distance = (item.position - self.position).magnitude()
            if distance <= item.item_radius + self.player_radius:
                return item
        return None

    def maintain_score_every_tick(self, highest_KO_amount):
        # called by model update_players()
        self.score = self.KO_amount * 30 - self.be_KO_amount * 15
        if self.be_KO_amount == 0:
            self.score += 100
        if self.KO_amount == highest_KO_amount:
            self.score += 50

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
        # Add horizontal velocity to the player along the direction.
        self.velocity += self.normal_speed * Const.DIRECTION_TO_VEC2[direction]
        if direction == 'left':
            self.direction = pg.Vector2(-1, 0)
        elif (direction == 'right'):
            self.direction = pg.Vector2(1, 0)

    def jump(self):
        # EventPlayerJump
        # Add vertical velocity to the player.
        if self.jump_quota != 0:
            if self.velocity.y > 0:
                self.velocity.y = -self.jump_speed
            else:
                self.velocity.y -= self.jump_speed
            self.jump_quota -= 1

    def attack(self, players, time):
        # EventPlayerAttack
        self.attack_cool_down_time = Const.ATTACK_COOL_DOWN_TIME
        for player in players:
            magnitude = (player.position - self.position).magnitude()
            # make sure that player is not self and player is alive and not invincible
            if player.player_id == self.player_id or not player.is_alive() or player.is_invincible():
                continue
            # attack if they are close enough
            if (self.player_radius == Const.INVINCIBLE_BATTERY_PLAYER_RADIUS and magnitude < Const.INVINCIBLE_BATTERY_ATTACK_RADIUS) or magnitude < self.attack_radius:
                unit = (player.position - self.position).normalize()
                player.be_attacked(unit, magnitude, self.player_id, time)

    def be_attacked(self, unit, magnitude, attacker_id, time):
        voltage_acceleration = self.voltage ** 1.35 + 100
        self.velocity += Const.BE_ATTACKED_ACCELERATION * voltage_acceleration * unit / magnitude / Const.FPS
        if self.voltage >= 100:
            self.velocity += Const.BE_ATTACKED_ACCELERATION * 10000 * unit / magnitude / Const.FPS
        self.voltage += (Const.VOLTAGE_INCREASE_CONST / magnitude)
        self.last_being_attacked_by = attacker_id
        self.last_being_attacked_time_elapsed = time

    def die(self, players, time):
        # EventPlayerDied
        self.life -= 1
        atk_id = self.last_being_attacked_by
        atk_t = self.last_being_attacked_time_elapsed
        if atk_id != -1 and atk_t - time < Const.VALID_KO_TIME:
            self.be_KO_amount += 1
            players[atk_id].KO_amount += 1

    def respawn(self, position: pg.Vector2):
        # EventPlayerRespawn
        # status
        self.player_radius = Const.PLAYER_RADIUS
        self.voltage = 0
        self.invincible_time = Const.RESPAWN_INVINCIBLE_TIME
        self.uncontrollable_time = 0
        self.attack_cool_down_time = 0
        self.jump_quota = Const.PLAYER_JUMP_QUOTA
        self.keep_item_id = Const.NO_ITEM
        # move
        self.position = pg.Vector2(position)
        self.velocity = pg.Vector2(0, 0)
        # others
        self.last_being_attacked_by = -1
        self.last_being_attacked_time_elapsed = 0

    def pick_item(self, item):
        # EventPlayerPickItem
        self.keep_item_id = item.item_id
        
    def use_item(self, players, time):
        # EventPlayerUseItem
        entities = []
        if self.keep_item_id == Const.BANANA_PISTOL:
            pos = self.position + self.direction * (self.player_radius + Const.BULLET_RADIUS) * 1.02
            entities.append(PistolBullet(self.player_id, pos, self.direction))
            pos = self.position - self.direction * (self.player_radius + Const.BANANA_PEEL_RADIUS) * 1.02 
            entities.append(BananaPeel(self.player_id, pos))

        elif self.keep_item_id == Const.BIG_BLACK_HOLE:
            entities.append(BigBlackHole(self.player_id, pg.Vector2(self.position.x, self.position.y)))

        elif self.keep_item_id == Const.CANCER_BOMB:
            entities.append(CancerBomb(self.player_id, pg.Vector2(self.position.x, self.position.y)))

        elif self.keep_item_id == Const.ZAP_ZAP_ZAP:
            self.voltage += Const.ZAP_ZAP_ZAP_SELF_VOLTAGE_UP
            for other in players :
                if abs(self.position.x - other.position.x) < Const.ZAP_ZAP_ZAP_RANGE and self != other\
                        and other.is_alive() and not other.is_invincible():
                    voltage_acceleration = other.voltage ** 1.35 + 100
                    other.voltage += Const.ZAP_ZAP_ZAP_OTHERS_VOLTAGE_UP
                    other.velocity.y = -Const.ZAP_ZAP_ZAP_VERTICAL_ACCELERATION * voltage_acceleration / Const.FPS
                    other.velocity.x = random.uniform(0, Const.ZAP_ZAP_ZAP_HORIZONTAL_ACCELERATION) * voltage_acceleration / Const.FPS \
                                       * (1 if self.position.x < other.position.x else -1)
                
        elif self.keep_item_id == Const.BANANA_PEEL:
            pos = self.position - self.direction * (self.player_radius + Const.BANANA_PEEL_RADIUS) * 1.02 
            entities.append(BananaPeel(self.player_id, pos))

        elif self.keep_item_id == Const.RAINBOW_GROUNDER:
            self.voltage -= Const.RAINBOW_GROUNDER_VOLTAGE_DOWN
            if self.voltage < 0:
                self.voltage = 0

        elif self.keep_item_id == Const.INVINCIBLE_BATTERY:
            self.position.y -= Const.INVINCIBLE_BATTERY_PLAYER_RADIUS - self.player_radius
            self.player_radius = Const.INVINCIBLE_BATTERY_PLAYER_RADIUS
            self.invincible_time = Const.INVINCIBLE_BATTERY_TIME

        self.keep_item_id = Const.NO_ITEM
        return entities
