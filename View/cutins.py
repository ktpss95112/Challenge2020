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
        
        if self._timer == self.expire_time:
            self.expired = True
        elif self._timer % self.delay_of_frames == 0:
            self.frame_index_to_draw = (self.frame_index_to_draw + 1) % len(self.frames)

    def draw(self, screen, update=True):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(**self.pos),
        )

        if update: self.update()


class Cutin_big_black_hole(Cutin_raster):
    def __init__(self):
        super().__init__(2, len(self.frames))