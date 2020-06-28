import Const
import pygame as pg

class Item:
    def __init__(self, item_id, position, item_radius):
        self.item_id = item_id
        self.position = position
        self.item_radius = item_radius    
        self.velocity = pg.Vector2(0,0)
    def move_every_tick(self, platforms: list):
        # Move the player
        prev_position = pg.Vector2(self.position)
        self.position += self.velocity / Const.FPS

        # Modify the horizontal velocity
        if self.velocity.x > 0:
            self.velocity.x -= Const.HORIZONTAL_ACCELERATION / Const.FPS
            self.velocity.x = self.velocity.x if self.velocity.x > 0 else 0
        elif self.velocity.x < 0:
            self.velocity.x += Const.HORIZONTAL_ACCELERATION / Const.FPS
            self.velocity.x = self.velocity.x if self.velocity.x < 0 else 0

        # Modify the vertical velocity
        self.velocity.y += Const.GRAVITY_ACCELERATION_FOR_ITEM / Const.FPS

        # Make sure that the player do not pass through the platform
        for platform in platforms:
            if platform.upper_left.x <= self.position.x <= platform.bottom_right.x:
                if prev_position.y <= platform.upper_left.y - self.item_radius <= self.position.y:
                    self.position.y = platform.upper_left.y - self.item_radius
                    self.velocity.y = 0
                    break

