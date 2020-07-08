import Const
import pygame as pg
import random

# If update_every_tick return False,it should be removed from entity list
class Entity(object):
    __slots__ = ('user_id', 'position')

    def __init__(self, user_id, position):
        self.user_id = user_id
        self.position = position

    def update_every_tick(self, players):
        return False


class PistolBullet(Entity):
    __slots__ = ('timer', 'velocity')

    def __init__(self, user_id, position, direction): # direction is a unit pg.vec2
        super().__init__(user_id, position)
        self.timer = Const.BULLET_TIME
        self.velocity = Const.BULLET_VELOCITY * direction
    
    def update_every_tick(self, players, items, platforms, time):
        self.timer -= 1
        self.position += self.velocity / Const.FPS
        # print("bullet flying, " + str(self.position))
        if self.timer <= 0:
            return False
        for player in players:
            if player.is_alive() and not player.is_invincible():
                vec = player.position - self.position
                magnitude = vec.magnitude() * 10
                if vec.magnitude() < player.player_radius + Const.BULLET_RADIUS:
                    # print("someone got shoot")
                    player.be_attacked(self.velocity.normalize(), magnitude, self.user_id, time)
                    # prevent remove failure
                    self.position = pg.Vector2(-1000, -2000)
                    self.velocity = pg.Vector2(0, 0)
                    return False
        return True


class BigBlackHole(Entity):
    __slots__ = ('timer',)

    def __init__(self, user_id, position):
        super().__init__(user_id, position)
        self.timer = Const.BLACK_HOLE_TIME

    def update_every_tick(self, players, items, platforms, time):
        self.timer -= 1
        if self.timer <= 0:
            return False
        # attract players
        for player in players:
            if player.is_alive() and not player.is_invincible() and player.player_id != self.user_id:
                dist = (self.position - player.position).magnitude()
                # check whether player is outside BLACK_HOLE_EFFECT_RADIUS
                if dist > Const.BLACK_HOLE_EFFECT_RADIUS:
                    unit = (self.position - player.position).normalize()
                    magnitude = Const.BLACK_HOLE_GRAVITY_ACCELERATION / (self.position - player.position).magnitude() ** 0.3
                    player.velocity += magnitude * unit / Const.FPS
                else:
                    normal = (self.position - player.position).normalize()
                    tangent = pg.Vector2(normal.y, -normal.x)
                    if tangent.dot(player.velocity) < 0:
                        tangent = -tangent
                    player.velocity = pg.Vector2(0, Const.GRAVITY_ACCELERATION / Const.FPS) + tangent / dist * 30000 + normal * 120
        # attract items
        for item in items:
            dist = (self.position - item.position).magnitude()
            # check whether item is outside BLACK_HOLE_EFFECT_RADIUS
            if dist > Const.BLACK_HOLE_EFFECT_RADIUS:
                unit = (self.position - item.position).normalize()
                magnitude = Const.BLACK_HOLE_GRAVITY_ACCELERATION / (self.position - item.position).magnitude() ** 0.3
                item.velocity += magnitude * unit / Const.FPS
            else:
                normal = (self.position - item.position).normalize()
                tangent = pg.Vector2(normal.y, -normal.x)
                if tangent.dot(item.velocity) < 0:
                    tangent = -tangent
                item.velocity = pg.Vector2(0, Const.GRAVITY_ACCELERATION / Const.FPS) + tangent / dist * 30000 + normal * 120
        return True


class CancerBomb(Entity):
    __slots__ = ('timer', 'velocity')

    def __init__(self, user_id, position):
        super().__init__(user_id, position)
        self.timer = Const.BOMB_TIME
        self.velocity = pg.Vector2(0,0)

    def update_every_tick(self, players, items, platforms, time):
       # gravity effect
        self.velocity.y += Const.GRAVITY_ACCELERATION / Const.FPS
        prev_position_y = self.position.y
        self.position += self.velocity / Const.FPS
        for platform in platforms:
            if platform.upper_left.x <= self.position.x <= platform.bottom_right.x and\
                prev_position_y <= platform.upper_left.y - Const.BANANA_PEEL_RADIUS <= self.position.y:
                self.position.y = platform.upper_left.y - Const.BANANA_PEEL_RADIUS
                self.velocity.y = -self.velocity.y * Const.ATTENUATION_COEFFICIENT if abs(self.velocity.y) > Const.VERTICAL_SPEED_MINIMUM else 0
                break
        self.timer -= 1
        if self.timer <= 0:
            for player in players:
                if player.is_alive() and not player.is_invincible():
                    distance = player.position - self.position
                    if distance.magnitude() < Const.BOMB_MINIMUM_DISTANCE:
                        distance = pg.Vector2(0, Const.BOMB_MINIMUM_DISTANCE)
                    if distance.magnitude() <= Const.BOMB_EXPLODE_RADIUS:
                        # Attack power == normal player's attack power
                        voltage_acceleration = player.voltage ** 1.35 + 10
                        player.velocity += Const.BE_ATTACKED_ACCELERATION * voltage_acceleration * distance.normalize() / distance.magnitude() / Const.FPS
                        player.voltage += Const.BOMB_ATK
            return False
        return True


class BananaPeel(Entity):
    __slots__ = ('timer', 'velocity')

    # Make the player temparorily can't control move direction,the player wouldn't be affect by drag force while affected.
    def __init__(self, user_id, position): #direction is a unit pg.vec2
        super().__init__(user_id, position)
        self.timer = Const.BANANA_PEEL_TIME
        self.velocity = pg.Vector2(0,0)

    def update_every_tick(self, players, items, platforms, time):
       # gravity effect
        self.velocity.y += Const.GRAVITY_ACCELERATION / Const.FPS
        prev_position_y = self.position.y
        self.position += self.velocity / Const.FPS
        for platform in platforms:
            if platform.upper_left.x <= self.position.x <= platform.bottom_right.x and\
                prev_position_y <= platform.upper_left.y - Const.BANANA_PEEL_RADIUS <= self.position.y:
                self.position.y = platform.upper_left.y - Const.BANANA_PEEL_RADIUS
                self.velocity.y = -self.velocity.y * Const.ATTENUATION_COEFFICIENT if abs(self.velocity.y) > Const.VERTICAL_SPEED_MINIMUM else 0
                break
        self.timer -= 1
        if self.timer <= 0:
            return False
        for player in players:
            if player.is_alive() and not player.is_invincible() and\
                (player.position - self.position).magnitude() < player.player_radius + Const.BANANA_PEEL_RADIUS:
                player.uncontrollable_time = Const.BANANA_PEEL_AFFECT_TIME
                return False
        if not Const.LIFE_BOUNDARY.collidepoint(self.position):
            return False
        return True

