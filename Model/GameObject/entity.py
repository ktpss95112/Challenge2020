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
        self.timer = 1000 / Const.BULLET_VELOCITY def update_every_tick(self, players):
        self.timer -= 1/Const.FPS
        self.position += self.velocity / Const.FPS
        print("bullet flying")
        if self.timer <= 0:
            return False
        for player in players:
            if (player.position - self.position).magnitude() < player.player_radius + Const.BULLET_RADIUS:
                print("someone got shoot")
                player.voltage += Const.BULLET_ATK
                #prevent remove failture
                self.position = pg.Vector2(-1000,-2000)
                self.velocity = pg.Vector2(0,0)
                return False
        return True



class BananaPeel(Entity):
    def __init__(self, position, direction): #direction is a unit pg.vec2 
        self.position = position
        self.timer = Const.BANANA_PEEL_TIME
    def update_every_tick(self, players):
        
        self.timer -= 1/Const.FPS
        if timer <= 0:
            return False
        #Implement later
        return True

                 
class CancerBomb(Entity):
    def __init__(self, position):
        self.position = position
        self.timer = Const.BOMB_TIME
        print("create bomb")

    def update_every_tick(self, players):
        self.timer -= 1 / Const.FPS
        if self.timer <= 0:
            for player in players:
                if (player.position - self.position).magnitude() <=  Const.BOMB_EXPLODE_RADIUS:
                    player.voltage += Const.BOMB_ATK
            print("EXPLOSION! " + str(self.position))
            return False
        return True

class BigBlackHole(Entity):
    def __init__(self, position):
        self.position = position
        self.timer = Const.BLACK_HOLE_TIME

    def update_every_tick(self, players):
        self.timer -= 1 / Const.FPS
        #Implement later
        return False 
