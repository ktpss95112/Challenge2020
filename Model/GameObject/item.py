import Const
import pygame as pg

class Item(object):
    __slots__ = ('item_id', 'position', 'item_radius', 'velocity', 'drag')

    def __init__(self, item_id, position, item_radius, drag):
        self.item_id = item_id
        self.position = position
        self.item_radius = item_radius    
        self.velocity = pg.Vector2(0,0)
        self.drag = drag

    def update_every_tick(self, platforms: list):
        # Maintain velocity
        self.maintain_velocity_every_tick()

        # Maintain position, make sure that the player do not pass through the platform
        self.move_every_tick(platforms)

    def maintain_velocity_every_tick(self):
        # Modify the horizontal velocity (drag)
        if abs(self.velocity.x) < Const.HORIZONTAL_SPEED_MINIMUM:
            self.velocity.x = 0
        elif abs(self.velocity.x) > Const.DRAG_CRITICAL_SPEED:
            self.velocity.x /= 2
        elif self.velocity.x > 0:
            self.velocity.x -= self.velocity.x ** 2.5 * Const.DRAG_COEFFICIENT
            self.velocity.x = self.velocity.x if self.velocity.x > 0 else 0
        elif self.velocity.x < 0:
            self.velocity.x += (-self.velocity.x) ** 2.5 * Const.DRAG_COEFFICIENT
            self.velocity.x = self.velocity.x if self.velocity.x < 0 else 0

        # Modify the vertical velocity (drag and gravity)
        self.velocity.y += Const.GRAVITY_ACCELERATION_FOR_ITEM / Const.FPS
        if self.velocity.y <= 2 * Const.VERTICAL_DRAG_EMERGE_SPEED:
            self.velocity.y /= 2
        elif self.velocity.y <= Const.VERTICAL_DRAG_EMERGE_SPEED:
            self.velocity.y = Const.VERTICAL_DRAG_EMERGE_SPEED

    def move_every_tick(self, platforms):
        prev_position = pg.Vector2(self.position)
        self.position += self.velocity / Const.FPS
        for platform in platforms:
            if platform.upper_left.x <= self.position.x <= platform.bottom_right.x:
                if prev_position.y <= platform.upper_left.y - self.item_radius <= self.position.y:
                    self.position.y = platform.upper_left.y - self.item_radius
                    self.velocity.y = 0
                    break
