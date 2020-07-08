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


class Cutin_board(Cutin_base):
    frames = tuple()

    # TODO: Image of board
    board_image = pg.Surface(Const.CUTIN_BOARD_SIZE, pg.SRCALPHA)
    board_image.fill((192, 192, 192))

    # TODO: Image of player
    players = tuple(
        scaled_surface(
            load_image(os.path.join(Const.IMAGE_PATH, Const.PLAYER_PIC[_i])),
            0.15
        )
        for _i in range(0, 20, 5)
    )

    @classmethod
    def init_convert(cls):
        cls.frames = tuple( _frame.convert_alpha() for _frame in cls.frames )
        cls.players = tuple( _player.convert_alpha() for _player in cls.players)

    def __init__(self, player_id, delay_of_frames, expire_time):
        self.player_id = player_id
        self._timer = 0
        self.delay_of_frames = delay_of_frames
        self.frame_index_to_draw = 0
        self.expire_time = expire_time
        self.expired = False
        self.board = pg.Surface(Const.CUTIN_BOARD_SIZE, pg.SRCALPHA)
        self.board_speed = Const.CUTIN_BOARD_INITIAL_SPEED
        self.board_position = list(Const.CUTIN_BOARD_INITIAL_POSITION)
        self.board_up = False

    def update(self):
        self._timer += 1
        self.update_board_position()
        if self._timer == self.expire_time:
            self.board_up = True
        if self.board_position[1] < -Const.CUTIN_BOARD_SIZE[1]:
            self.expired = True
        

    def draw(self, screen, update=True):
        self.board.blit(
            self.board_image,
            (0, 0)
        )
        self.board.blit(
            self.players[self.player_id],
            self.players[self.player_id].get_rect(center=(Const.CUTIN_PLAYER_POSITION))
        )
        screen.blit(
            self.board,
            self.board.get_rect(center=self.board_position)
        )

        if update:
            self.update()
    
    def update_board_position(self):
        # Board down
        if not self.board_up:
            self.board_position[1] += self.board_speed / Const.FPS
            self.board_speed += Const.CUTIN_GRAVITY / Const.FPS
            distance = Const.CUTIN_BOARD_FINAL_POSITION[1] - self.board_position[1]
            if distance < 0:
                self.board_speed *= -Const.ATTENUATION_COEFFICIENT
                self.board_position[1] += 2 * distance
            if abs(self.board_speed) < Const.CUTIN_SPEED_MINIMUM:
                self.board_speed = 0
        # Board up
        else:
            self.board_position[1] += self.board_speed / Const.FPS
            self.board_speed -= Const.CUTIN_GRAVITY / Const.FPS


class Cutin_text(Cutin_board):
    skill_name = 'Skill Name'
    def __init__(self, player_id):
        super().__init__(player_id, 1, 3 * Const.FPS)
        self.type_time = np.zeros(len(self.skill_name), dtype=np.int8)
        self.type_time[:] = np.random.randint(5, 20, size=len(self.skill_name))
        self.font = pg.font.Font(os.path.join(Const.FONT_PATH, 'Noto', 'NotoSansCJK-Black.ttc'), 36)

    def update(self):
        self._timer += 1
        self.update_board_position()
        if self.type_time[-1] == 0:
            self.board_up = True
        if self.board_position[1] < -Const.CUTIN_BOARD_SIZE[1]:
            self.expired = True

    def draw(self, screen, update=True):
        self.board.fill((19, 19, 19)) # For Test
        self.board.blit(
            self.players[self.player_id],
            self.players[self.player_id].get_rect(center=(Const.CUTIN_PLAYER_POSITION))
        )
        text_surface = self.font.render(self.word(), 1, pg.Color('white'))
        self.board.blit(
            text_surface,
            Const.CUTIN_TEXT_POSITION
        )
        screen.blit(
            self.board,
            self.board.get_rect(center=self.board_position)
        )

        if update:
            self.update()

    def word(self):
        word = ''
        for i in range(len(self.type_time)):
            if self.type_time[i] == 0:
                word += self.skill_name[i]
            else:
                self.type_time[i] -= 1
                break
        return word + '_'
        

class Cutin_big_black_hole(Cutin_text):
    skill_name = 'Black Hole'
    

class Cutin_zap_zap_zap(Cutin_text):
    skill_name = 'ZAP ZAP ZAP'
    def __init__(self, player_id):
        super().__init__(player_id)