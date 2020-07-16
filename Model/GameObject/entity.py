import Const
import pygame as pg
import random

# If update_every_tick return False,it should be removed from entity list
class Entity:
    def __init__(self, user_id, position: pg.Vector2, velocity: pg.Vector2, timer):
        self.user_id = user_id
        self.position = position
        self.velocity = velocity
        self.timer = timer

    def update_every_tick(self, players, items, platforms, time):
        return False

    def maintain_velocity_every_tick(self, platforms):
        self.velocity.y += Const.GRAVITY_ACCELERATION / Const.FPS
        unit = self.velocity.normalize()
        # air drag (f = -kv => v = (1 - k/m) * v)
        self.velocity *= (1 - Const.DRAG_COEFFICIENT)
        # friction
        touch_platform = False
        for platform in platforms:
            if (platform.upper_left.y - self.position.y) < 25 and\
                platform.upper_left.x <= self.position.x <= platform.bottom_right.x:
                touch_platform = True
                break
        if touch_platform and self.velocity.x != 0:
            prev_velocity_x_dir = 1 if self.velocity.x > 0 else -1
            self.velocity.x -= prev_velocity_x_dir * Const.FRICTION_COEFFICIENT
            if self.velocity.x * prev_velocity_x_dir < 0:
                self.velocity.x = 0 

    def move_every_tick(self, platforms, radius):
        prev_position = pg.Vector2(self.position)
        self.position += self.velocity / Const.FPS
        for platform in platforms:
            if platform.upper_left.x <= self.position.x <= platform.bottom_right.x:
                if prev_position.y <= platform.upper_left.y - radius <= self.position.y:
                    self.position.y = platform.upper_left.y - radius
                    self.velocity.y = 0
                    break

    def maintain_timer_every_tick(self):
        self.timer -= 1


class PistolBullet(Entity):
    def __init__(self, user_id, position, velocity): # direction is a unit pg.vec2
        super().__init__(user_id, position, velocity, Const.BULLET_TIME)
    
    def update_every_tick(self, players, items, platforms, time):
        self.move_every_tick([], Const.BULLET_RADIUS)
        self.maintain_timer_every_tick()
        
        for player in players:
            if player.is_alive() and not player.is_invincible():
                if (player.position - self.position).magnitude() < player.player_radius + Const.BULLET_RADIUS:
                    player.be_attacked_by_pistol_bullet(self.velocity.normalize(), self.user_id, time)
                    return False
        return True if self.timer > 0 else False


class BigBlackHole(Entity):
    def __init__(self, user_id, position):
        super().__init__(user_id, position, pg.Vector2(0, 0), Const.BLACK_HOLE_TIME)

    def update_every_tick(self, players, items, platforms, time):
        self.maintain_timer_every_tick()
        valid_players = [player for player in players if player.is_alive() and not player.is_invincible() and\
                        player.player_id != self.user_id]
        self.attract(valid_players + items)
        return True if self.timer > 0 else False

    def attract(self, objects):
        for obj in objects: 
            dist = (self.position - obj.position).magnitude()
            # check whether object is outside BLACK_HOLE_EFFECT_RADIUS
            if dist > Const.BLACK_HOLE_EFFECT_RADIUS:
                unit = (self.position - obj.position).normalize()
                magnitude = Const.BLACK_HOLE_GRAVITY_ACCELERATION / (self.position - obj.position).magnitude() ** 0.3
                obj.velocity += magnitude * unit / Const.FPS
            else:
                # counterclockwise rotation
                normal = (self.position - obj.position).normalize()
                tangent = pg.Vector2(-normal.y, normal.x)
                if (normal.y < 0 and tangent.x < 0) or (normal.y > 0 and tangent.x > 0):
                    tangent *= -1
                obj.velocity = pg.Vector2(0, Const.GRAVITY_ACCELERATION / Const.FPS) + tangent / dist * 50000 + normal * 250


class CancerBomb(Entity):
    def __init__(self, user_id, position):
        super().__init__(user_id, position, pg.Vector2(0, 0), Const.BOMB_TIME)
        self.red = False

    def update_every_tick(self, players, items, platforms, time):
        self.maintain_velocity_every_tick(platforms)
        self.move_every_tick(platforms, Const.BOMB_RADIUS)
        self.maintain_timer_every_tick()

        self.red = True if (self.timer <= 60 or (self.timer // 9) % 2 == 0) else False

        if self.timer == 0:
            for player in players:
                if player.is_alive() and not player.is_invincible():
                    distance = (player.position - self.position).magnitude()
                    if distance < Const.BOMB_MINIMUM_DISTANCE:
                        distance = Const.BOMB_MINIMUM_DISTANCE
                    if distance <= Const.BOMB_EXPLODE_RADIUS:
                        # Attack power == normal player's attack power
                        player.be_attacked_by_cancer_bomb((player.position - self.position).normalize(), distance, time)
            return False
        return True


class BananaPeel(Entity):
    # Make the player temparorily can't control move direction,the player wouldn't be affect by drag force while affected.
    def __init__(self, user_id, position, velocity):
        super().__init__(user_id, position, velocity, Const.BANANA_PEEL_TIME)

    def update_every_tick(self, players, items, platforms, time):
        self.maintain_velocity_every_tick(platforms)
        self.move_every_tick(platforms, Const.BANANA_PEEL_RADIUS)
        self.maintain_timer_every_tick()

        for player in players:
            if player.is_alive() and not player.is_invincible() and\
                (player.position - self.position).magnitude() < player.player_radius + Const.BANANA_PEEL_RADIUS:
                player.uncontrollable_time += Const.BANANA_PEEL_AFFECT_TIME
                return False
        return True if self.timer > 0 else False


class DeathRain(Entity):
    # A box that would produce lots of item when be touched
    def __init__(self, platforms):
        super().__init__(None, self.find_position(platforms), Const.DEATH_RAIN_VELOCITY, None)

    def update_every_tick(self, players, items, platforms, time):
        self.move_every_tick(platforms, Const.DEATH_RAIN_RADIUS)

        for player in players:
            if player.is_alive() and not player.is_invincible() and\
                (player.position - self.position).magnitude() < player.player_radius + Const.DEATH_RAIN_RADIUS:
                return False
        return True

    def find_position(self, platforms):
        platform_amount = len(platforms)
        platform = platforms[random.randint(0, platform_amount - 1)]
        return pg.Vector2((platform.upper_left[0] + platform.bottom_right[0]) // 2, -100)
