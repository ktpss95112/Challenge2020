import Const
import pygame as pg

# If update_every_tick return False,it should be removed from entity list
class Entity:
    def __init__(self, position):
        self.position = position
    def update_every_tick(self, players):
        return False 

class PistolBullet(Entity):
    def __init__(self, position, direction): #direction is a unit pg.vec2 
        self.position = position
        self.velocity = Const.BULLET_VELOCITY * direction
        self.timer = 1000 / Const.BULLET_VELOCITY 
    def update_every_tick(self, players, platforms):
        self.timer -= 1/Const.FPS
        self.position += self.velocity / Const.FPS
        #print("bullet flying, " + str(self.position))
        if self.timer <= 0:
            return False
        for player in players:
            if (player.position - self.position).magnitude() < player.player_radius + Const.BULLET_RADIUS:
                #print("someone got shoot")
                player.voltage += Const.BULLET_ATK
                #prevent remove failture
                self.position = pg.Vector2(-1000,-2000)
                self.velocity = pg.Vector2(0,0)
                return False
        return True


class BananaPeel(Entity):
#Make the player temparorily can't control move direction,the player wouldn't be affect by drag force while affected.
    def __init__(self, position): #direction is a unit pg.vec2 
        self.position = position
        self.timer = Const.BANANA_PEEL_TIME
        self.velocity = pg.Vector2(0,0)
    def update_every_tick(self, players,platforms):
       #---------gravity-------
        self.velocity.y += Const.GRAVITY_ACCELERATION /Const.FPS
        prev_position_y = self.position.y
        self.position += self.velocity / Const.FPS
        for platform in platforms:
            if platform.upper_left.x <= self.position.x <= platform.bottom_right.x:
                if prev_position_y <= platform.upper_left.y - Const.BANANA_PEEL_RADIUS <= self.position.y:
                    self.position.y = platform.upper_left.y - Const.BANANA_PEEL_RADIUS
                    self.velocity.y = -self.velocity.y * Const.ATTENUATION_COEFFICIENT if abs(self.velocity.y) > Const.VERTICAL_SPEED_MINIMUM else 0
                    break
        #------------------------
        self.timer -= 1/Const.FPS
        if self.timer <= 0:
            return False

        for player in players:
            if (player.position - self.position).magnitude() < player.player_radius + Const.BANANA_PEEL_RADIUS:
                player.can_not_control_time = Const.BANANA_PEEL_AFFECT_TIME
                return False
        #Implement later
        return True

                 
class CancerBomb(Entity):
    def __init__(self, position):
        self.position = position
        self.timer = Const.BOMB_TIME
        self.velocity = pg.Vector2(0,0) 

    def update_every_tick(self, players, platforms):
       #---------gravity-------
        self.velocity.y += Const.GRAVITY_ACCELERATION /Const.FPS
        prev_position_y = self.position.y
        self.position += self.velocity / Const.FPS
        for platform in platforms:
            if platform.upper_left.x <= self.position.x <= platform.bottom_right.x:
                if prev_position_y <= platform.upper_left.y - Const.BANANA_PEEL_RADIUS <= self.position.y:
                    self.position.y = platform.upper_left.y - Const.BANANA_PEEL_RADIUS
                    self.velocity.y = -self.velocity.y * Const.ATTENUATION_COEFFICIENT if abs(self.velocity.y) > Const.VERTICAL_SPEED_MINIMUM else 0
                    break
        #------------------------
        self.timer -= 1 / Const.FPS
        if self.timer <= 0:
            for player in players:
                if (player.position - self.position).magnitude() <=  Const.BOMB_EXPLODE_RADIUS:
                    player.voltage += Const.BOMB_ATK
            print("EXPLOSION! " + str(self.position))
            return False
        return True

class BigBlackHole(Entity):
    def __init__(self, position, user):
        self.position = position
        self.timer = Const.BLACK_HOLE_TIME
        self.user = user

    def update_every_tick(self, players, platforms):
        self.timer -= 1 / Const.FPS
        if self.timer <= 0:
            return False
        for player in players:
            if player.is_alive():
                if (self.position - player.position).magnitude() > Const.PLAYER_RADIUS + 10:
                    unit = (self.position - player.position).normalize()
                    magnitude = Const.BLACK_HOLE_GRAVITY_ACCELERATION / (self.position - player.position).magnitude() ** 0.3
                    player.velocity += magnitude * unit / Const.FPS
                else:
                    player.velocity = pg.Vector2((0, 0))
        return True
