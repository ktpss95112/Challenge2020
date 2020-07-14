'''
* How Animation works:

tick = 0
animations = []
while True:
    for ani in animations:
        if ani.expired:
            animations.remove(ani)

    animations.append(new_animation)

    for ani in animations:
        ani.draw(screen)

    tick += 1
'''
import os
import pygame as pg
import numpy as np
import random

from Events.EventManager import *
from Model.Model import GameEngine
from Model.GameObject.player import Player
from Model.GameObject.item import Item
from View.utils import scaled_surface, load_image
import Const

'''
VERY IMPORTANT !!!
VERY IMPORTANT !!!
VERY IMPORTANT !!!

Once you add a new class in this module, you have to add CLASS.init_convert()
in the init_otherobjects() function!
'''


class Animation_base(object):
    '''
    Base class of all animation.
    There will be a list (call it ANI) of all currently effective animations in main.py of view.
    To start an animation, you have to append the new Animation to ANI.
    Every animation in ANI should be drawn (if valid) or be discarded (if expired) in every tick.
    '''
    __slots__ = ('_timer', 'expired')

    def __init__(self, delay_of_frames, **pos):
        self._timer = 0
        self.expired = False

    def update(self):
        pass

    # the "update" argument is for the purpose of GraphicalView.theworld_background in View/main.py
    def draw(self, screen, update=True):
        # draw first
        # update second
        pass


class Animation_raster(Animation_base):
    __slots__ = ('delay_of_frames', 'frame_index_to_draw', 'expire_time', 'pos')
    frames = tuple()

    @classmethod
    def init_convert(cls):
        cls.frames = tuple( _frame.convert_alpha() for _frame in cls.frames )

    def __init__(self, delay_of_frames, expire_time, **pos):
        self._timer = 0
        self.delay_of_frames = delay_of_frames
        self.frame_index_to_draw = 0
        self.expire_time = expire_time
        self.expired = False
        pos[next(iter(pos))] = pg.math.Vector2(pos[next(iter(pos))]) # turn tuple into vec2
        self.pos = pos

    def update(self):
        self._timer += 1

        if self._timer == self.expire_time:
            self.expired = True
        elif self._timer % self.delay_of_frames == 0:
            self.frame_index_to_draw = (self.frame_index_to_draw + 1) % len(self.frames)

        # update self.pos if needed
        # self.pos[ next(iter(self.pos)) ] = pg.math.Vector2(next_pos)
        # or
        # self.pos[ next(iter(self.pos)) ] += pg.math.Vector2(dx, dy)

    # the "update" argument is for the purpose of GraphicalView.theworld_background in View/main.py
    def draw(self, screen, update=True):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(**self.pos),
        )

        if update: self.update()


class Animation_Bomb_Explode(Animation_raster):
    frames = tuple(
        scaled_surface(
            load_image(os.path.join(Const.IMAGE_PATH, f'explosion_{_i}.png')),
            0.8
        )
            for _i in range(1, 18)
    )

    def __init__(self, **pos):
        super().__init__(2, 2*len(self.frames), **pos)


class Animation_Lightning(Animation_raster):
    __slots__ = ('lightning_alpha', 'image')

    lightning = pg.transform.smoothscale(load_image(os.path.join(Const.IMAGE_PATH, 'lightning.png')),
    (int(2 * Const.ZAP_ZAP_ZAP_RANGE), 800))

    @classmethod
    def init_convert(cls):
        cls.lightning = cls.lightning.convert_alpha()

    def __init__(self, pos):
        self._timer = 0
        self.delay_of_frames = 2
        self.expire_time = 27
        self.expired = False
        self.pos = pos - Const.ZAP_ZAP_ZAP_RANGE
        self.lightning_alpha = random.randint(100, 255)

    def update(self):
        self._timer += 1
        if self._timer == self.expire_time:
            self.expired = True

    def draw(self, screen, update=True):
        if self._timer % 7 == 0:
            sign = [-1, 1]
            self.pos += random.randint(3, 10) * random.choice(sign)
            self.lightning_alpha = random.randint(100, 255)
        self.image = self.lightning.subsurface(pg.Rect(0, 0, 2 * Const.ZAP_ZAP_ZAP_RANGE, (Const.ARENA_SIZE[1] / self.expire_time ) * self._timer))
        self.image.set_alpha(self.lightning_alpha)
        screen.blit(
            self.image,
            (self.pos,0),
            )
        if (self._timer>11 and self._timer<17) or (self._timer>22 and self._timer<24):
            pg.draw.rect(screen, (255, 255, 255, 10), pg.Rect((0, 0), Const.WINDOW_SIZE))

        if update: self.update()


class Animation_player_attack(Animation_raster):
    __slots__ = ('player',)

    frames = tuple(
        scaled_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'electricattack.png')),
            0.1 + (_i * 0.002)
        )
        for _i in range(1, 7)
    )

    def __init__(self, player: Player):
        # TODO: refactor the following code, use super().__init__
        self._timer = 0
        self.delay_of_frames = 2
        self.frame_index_to_draw = 0
        self.expire_time = 2*len(self.frames)
        self.expired = False
        self.player = player

    def draw(self, screen, update=True):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(center=(self.player.position.x , self.player.position.y - Const.ATTACK_ERROR)),
        )

        if update: self.update()


class Animation_player_attack_big(Animation_raster):
    __slots__ = ('player',)

    frames = tuple(
        scaled_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'electricattack.png')),
            0.2 + (_i * 0.002)
        )
        for _i in range(1, 7)
    )

    def __init__(self, player: Player):
        # TODO: refactor the following code, use super().__init__
        self._timer = 0
        self.delay_of_frames = 2
        self.frame_index_to_draw = 0
        self.expire_time = 2*len(self.frames)
        self.expired = False
        self.player = player

    def draw(self, screen, update=True):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(center=(self.player.position.x , self.player.position.y - 2*Const.ATTACK_ERROR)),
        )

        if update: self.update()


class Animation_Bomb_Explode(Animation_raster):
    __slots__ = ('vibration',)

    frames = tuple(
        scaled_surface(
            load_image(os.path.join(Const.IMAGE_PATH, f'explosion_{_i}.png')),
            0.8
        )
            for _i in range(1, 18)
    )

    def __init__(self, **pos):
        super().__init__(2, 2*len(self.frames), **pos)
        r = Const.BOMB_SCREEN_VIBRATION_RADIUS
        self.vibration = np.zeros((Const.BOMB_TIME, 2), dtype=np.int8)
        self.vibration[:Const.BOMB_SCREEN_VIBRATION_DURATION, :] = np.random.randint(-r, r+1, size=(Const.BOMB_SCREEN_VIBRATION_DURATION, 2))

    def draw(self, screen, update=True):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(**self.pos),
        )
        screen.blit(screen.copy(), self.vibration[self._timer])

        if update: self.update()

class Animation_Rainbow(Animation_raster):
    frames = tuple(
        scaled_surface(
            load_image(os.path.join(Const.IMAGE_PATH, f'rainbow_{_i}.png')),
            1
        )
            for _i in range(1, 12)
    )

    def __init__(self, **pos):
        super().__init__(4, 4*(len(self.frames) + 10), **pos)

    def update(self):
        self._timer += 1

        if self._timer == self.expire_time:
            self.expired = True
        elif self._timer % self.delay_of_frames == 0:
            self.frame_index_to_draw = (self.frame_index_to_draw + 1) % (len(self.frames) + 10)

    def draw(self, screen, update=True):
        screen.blit(
            self.frames[min(self.frame_index_to_draw, 10)],
            self.frames[min(self.frame_index_to_draw, 10)].get_rect(**self.pos),
        )
        if update: self.update()

class Animation_Black_Hole:
    __slots__ = ('area', 'center', '_timer', 'expire_time', 'expired')
    black_background = None

    radius_max = 150
    radius_min = 50
    phase1_time = Const.BLACK_HOLE_TIME
    phase2_time = 2 * Const.FPS

    @classmethod
    def init_convert(cls):
        cls.black_background = pg.Surface((2 * cls.radius_max, 2 * cls.radius_max))

        cls.transformedxi = []
        cls.transformedyi = []

        # the vibration radius grows by time
        vibration_radius_max = 3
        cls.vibration_radius = np.rint(np.random.rand(2, cls.phase1_time) * np.linspace(0, vibration_radius_max, cls.phase1_time))

        # obtain Cartesian coordinate and polar coordinate
        xv, yv = np.mgrid[-cls.radius_max:cls.radius_max, -cls.radius_max:cls.radius_max]
        r, t = np.hypot(xv, yv), np.arctan2(yv, xv)

        for _timer in range(cls.phase1_time):

            # the radius of rotation decreases by time
            rotate_radius = int(cls.radius_max - (cls.radius_max - cls.radius_min) / cls.phase1_time * _timer)
            # rotate_radius = np.linspace(cls.radius_max, cls.radius_min, cls.phase1_time, dtype=np.int)

            # new theta for rotation
            newt = t - (20 * ((_timer / Const.FPS * 2 + 1) / 6)**3) * (-np.abs((r / rotate_radius - 0.5)) + 0.5)**3

            # new radius for space compression
            newr = cls.radius_max * (r / cls.radius_max) ** (1 / (1 + _timer / Const.FPS / 4))

            # calculate rotated
            mask_rotate = (r <= rotate_radius)
            rotatedxv = np.where(mask_rotate, (r * np.cos(newt)).astype(np.int), xv) + cls.radius_max
            rotatedyv = np.where(mask_rotate, (r * np.sin(newt)).astype(np.int), yv) + cls.radius_max

            # calculate compressed
            mask_compress = (r <= cls.radius_max)
            compressedxv = np.where(mask_compress, (newr * np.cos(t)).astype(np.int), xv) + cls.radius_max
            compressedyv = np.where(mask_compress, (newr * np.sin(t)).astype(np.int), yv) + cls.radius_max

            # combine
            yi, xi = np.indices((2 * cls.radius_max, 2 * cls.radius_max))
            cls.transformedxi.append(xi[rotatedyv, rotatedxv][compressedyv, compressedxv])
            cls.transformedyi.append(yi[rotatedyv, rotatedxv][compressedyv, compressedxv])

    def __init__(self, center):
        '''
        center could be:
            * 2-element tuple/list
            * pygame.Vector2
            * np.ndarray with shape (2,)
        '''
        self._timer = 0
        self.expire_time = self.phase1_time + self.phase2_time
        self.expired = False

        self.area = pg.Rect(0, 0, 2 * self.radius_max, 2 * self.radius_max)
        self.center = np.array(center)

    def update(self):
        self._timer += 1
        if self._timer >= self.expire_time:
            self.expired = True

    def draw(self, screen, update=True):
        if self._timer < Const.BLACK_HOLE_TIME: self.area.center = self.center + self.vibration_radius[:, self._timer]
        else                                  : self.area.center = self.center
        canvas = screen.get_rect()

        # If this animation is completely outside the canvas, no need to draw it.
        # This prevents "ValueError: subsurface rectangle outside surface area" in the following pg.Surface.subsurface()
        # More precisely, area_inside would become `pg.Rect(_, _, 0, 0)`, causing subsurface to fail.
        if not canvas.contains(self.area):
            if update: self.update()
            return

        # phase 1: twist the screen
        if self._timer < Const.BLACK_HOLE_TIME:
            area_inside = self.area.clip(canvas)

            sub_background = pg.Surface.subsurface(screen, area_inside)

            self.black_background.fill(pg.Color(0x232323)) # TODO: use Const.BACKGROUND_COLOR
            position = {}
            if self.area.left < canvas.left: position['left'] = canvas.left - self.area.left
            else                           : position['left'] = 0
            if self.area.top < canvas.top  : position['top'] = canvas.top - self.area.top
            else                           : position['top'] = 0

            self.black_background.blit(sub_background, sub_background.get_rect(**position))
            sub_background = self.black_background

            source_array = pg.surfarray.array3d(sub_background)
            result_array = source_array[self.transformedyi[self._timer], self.transformedxi[self._timer]]

            result = pg.surfarray.make_surface(result_array)
            # uncommented the following line if the quality is too poor
            # result = pg.transform.smoothscale(pg.transform.smoothscale(result, (100, 100)), result.get_size())
            screen.blit(result, self.area)

        # phase 2: explode
        else:
            pass

        if update: self.update()


def init_animation():
    Animation_player_attack.init_convert()
    Animation_player_attack_big.init_convert()
    Animation_Bomb_Explode.init_convert()
    Animation_Lightning.init_convert()
    Animation_Rainbow.init_convert()
    Animation_Black_Hole.init_convert()
