import Const
import pygame as pg

class Item:
    def __init__(self, item_id, position, item_radius, drag):
        self.item_id = item_id
        self.position = position
        self.item_radius = item_radius    
        self.velocity = pg.Vector2(0,0)
        self.drag = drag

    def update_every_tick(self, platforms: list):
        # Maintain velocity
        self.maintain_velocity_every_tick(platforms)

        # Maintain position, make sure that the player do not pass through the platform
        self.move_every_tick(platforms)

    def maintain_velocity_every_tick(self, platforms):
        self.velocity.y += Const.GRAVITY_ACCELERATION / Const.FPS
        unit = self.velocity.normalize()
        # air drag (f = -kv => v = (1 - k/m) * v)
        self.velocity *= (1 - Const.DRAG_COEFFICIENT)
        # friction
        touch_platform = False
        for platform in platforms:
            if (platform.upper_left.y - self.position.y) < self.item_radius * 1.1 and\
                platform.upper_left.x <= self.position.x <= platform.bottom_right.x:
                touch_platform = True
                break
        if touch_platform and self.velocity.x != 0:
            prev_velocity_x_dir = 1 if self.velocity.x > 0 else -1
            self.velocity.x -= prev_velocity_x_dir * Const.FRICTION_COEFFICIENT
            if self.velocity.x * prev_velocity_x_dir < 0:
                self.velocity.x = 0

    def move_every_tick(self, platforms):
        prev_position = pg.Vector2(self.position)
        self.position += self.velocity / Const.FPS
        for platform in platforms:
            if platform.upper_left.x <= self.position.x <= platform.bottom_right.x:
                if prev_position.y <= platform.upper_left.y - self.item_radius <= self.position.y:
                    self.position.y = platform.upper_left.y - self.item_radius
                    self.velocity.y = 0
                    break
