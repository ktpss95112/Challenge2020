import os
import pygame as pg
import numpy as np

from Events.EventManager import *
from Model.Model import GameEngine
from Model.GameObject.player import Player
from Model.GameObject.item import Item
from View.utils import scaled_surface, load_image
import Const


class Cutin_base():
    '''
    Base class of all cutin.
    There will be a list (call it CUTIN) of all currently effective cutins in main.py of view.
    To start an cutin, you have to append the new cutin to CUTIN.
    The first-in animation in CUTIN should be drawn (if valid) or be discarded (if expired) in every tick.
    '''

    def __init__(self, delay_of_flames):
        self._timer = 0
        self.expired = False

    def update(self):
        pass

    # the "update" argument is for the purpose of GraphicalView.theworld_background in View/main.py
    def draw(self, screen, update=True):
        # draw first
        # update second
        pass


class Cutin_raster(Cutin_base):
    frames = tuple()
    # TODO: Make board beautiful
    board = pg.Surface(Const.CUTIN_BOARD_SIZE, pg.SRCALPHA)

    @classmethod
    def init_convert(cls):
        cls.frames = tuple( _frame.convert_alpha() for _frame in cls.frames )

    def __init__(self, delay_of_frames, expire_time):
        self._timer = 0
        self.delay_of_frames = delay_of_frames
        self.frame_index_to_draw = 0
        self.expire_time = expire_time
        self.expired = False

    def update(self):
        self._timer += 1
        self.update_board_position()
        if self._timer == self.expire_time:
            self.expired = True

    def draw(self, screen, update=True):
        screen.blit(
            self.board,
            self.board.get_rect(center=self.board_position)
        )

        if update:
            self.update()
    
    def update_board_position(self):
        self.board_position[1] += self.board_speed / Const.FPS
        self.board_speed += Const.CUTIN_GRAVITY / Const.FPS
        distance = Const.CUTIN_BOARD_FINAL_POSITION[1] - self.board_position[1]
        if distance < 0:
            self.board_speed *= -Const.ATTENUATION_COEFFICIENT
            self.board_position[1] += 2 * distance
        if abs(self.board_speed) < Const.CUTIN_SPEED_MINIMUM:
            self.board_speed = 0


class Cutin_big_black_hole(Cutin_raster):
    def __init__(self):
        super().__init__(1, 120)
        self.board_speed = 0
        self.board_position = list(Const.CUTIN_BOARD_INITIAL_POSITION)
        

class Cutin_zap_zap_zap(Cutin_raster):
    def __init__(self):
        super().__init__(1, 120)