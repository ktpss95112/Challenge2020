import Const
import pygame as pg

class Item:
    def __init__(self, item_id, position, item_radius, drag):
        self.item_id = item_id
        self.position = position
        self.item_radius = item_radius    
        self.velocity = pg.Vector2(0,0)
        self.drag = drag
    def move_every_tick(self, platforms: list):
        '''
        if self.velocity.magnitude() > Const.DRAG_CRITICAL_SPEED:
            self.velocity.x = Const.DRAG_CRITICAL_SPEED

        # Modify the vertical velocity
        self.velocity.y += (Const.GRAVITY_ACCELERATION - self.drag * self.velocity.y ** 2) / Const.FPS
        self.velocity.y += Const.GRAVITY_ACCELERATION / Const.FPS
        if self.velocity.y <= 2 * Const.VERTICAL_DRAG_EMERGE_SPEED:
            self.velocity.y /= 2
        elif self.velocity.y <= Const.VERTICAL_DRAG_EMERGE_SPEED:
            self.velocity.y = Const.VERTICAL_DRAG_EMERGE_SPEED
        '''
        # Modify the horizontal velocity
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

        # Modify the vertical velocity
        self.velocity.y += Const.GRAVITY_ACCELERATION / Const.FPS
        if self.velocity.y <= 2 * Const.VERTICAL_DRAG_EMERGE_SPEED:
            self.velocity.y /= 2
        elif self.velocity.y <= Const.VERTICAL_DRAG_EMERGE_SPEED:
            self.velocity.y = Const.VERTICAL_DRAG_EMERGE_SPEED

        # Move the item
        prev_position = pg.Vector2(self.position)
        self.position += self.velocity / Const.FPS

        # Make sure that the item does not pass through the platform
        for platform in platforms:
            if platform.upper_left.x <= self.position.x <= platform.bottom_right.x:
                if prev_position.y <= platform.upper_left.y - self.item_radius <= self.position.y:
                    self.position.y = platform.upper_left.y - self.item_radius
                    self.velocity.y = 0
                    break

