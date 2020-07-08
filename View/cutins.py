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
    '''
    Base class for all cut-in with a board
    '''
    # TODO: Image of board
    board_image = pg.Surface(Const.CUTIN_BOARD_SIZE, pg.SRCALPHA)
    board_image.fill((192, 192, 192))

    # TODO(?): Image of player
    players = tuple(
        scaled_surface(
            load_image(os.path.join(Const.IMAGE_PATH, Const.PLAYER_PIC[_i])),
            0.15
        )
        for _i in range(0, 20, 5)
    )

    @classmethod
    def init_convert(cls):
        cls.players = tuple( _player.convert_alpha() for _player in cls.players)

    def __init__(self, player_id, expire_time=Const.FPS):
        self.player_id = player_id
        self._timer = 0
        self.expire_time = expire_time
        self.expired = False
        self.board = pg.Surface(Const.CUTIN_BOARD_SIZE, pg.SRCALPHA)
        self.board_speed = Const.CUTIN_BOARD_INITIAL_SPEED
        self.board_position = list(Const.CUTIN_BOARD_INITIAL_POSITION)
        self.board_up = False

    def update(self):
        # Scroll the board back and set expired to true after board become invisible
        self._timer += 1
        self.update_board_position()
        if self._timer == self.expire_time:
            self.board_up = True
        if self.board_position[1] < -Const.CUTIN_BOARD_SIZE[1]:
            self.expired = True
    
    def draw(self, screen, update=True):
        # Draw board with image of player
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
        # Update position of board
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
                self.board_position[1] = Const.CUTIN_BOARD_FINAL_POSITION[1]
        # Board up
        else:
            self.board_position[1] += 2 * self.board_speed / Const.FPS
            self.board_speed -= Const.CUTIN_GRAVITY / Const.FPS


class Cutin_text(Cutin_board):
    '''
    Base class of all cut-ins that need to show text on board
    '''
    skill_name = 'Skill Name'
    def __init__(self, player_id):
        # Add type_time to random type speed of typewriter
        super().__init__(player_id)
        self.type_time = np.zeros(len(self.skill_name), dtype=np.int8)
        self.type_time[:] = np.random.randint(5, 20, size=len(self.skill_name))
        self.font = pg.font.Font(os.path.join(Const.FONT_PATH, 'Noto', 'NotoSansCJK-Black.ttc'), 36)
        self.stay_time = Const.CUTIN_STAY_TIME # The time cut-in would stay after every thing finish

    def update(self):
        # Update board position and update the state
        self._timer += 1
        self.update_board_position()
        if self.type_time[-1] == 0:
            self.stay_time -= 1
        if self.stay_time == 0:
            self.board_up = True
        if self.board_position[1] < -Const.CUTIN_BOARD_SIZE[1]:
            self.expired = True

    def draw(self, screen, update=True):
        # Draw board with name of skill and player
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
        # Determine the text to show
        word = ''
        for i in range(len(self.type_time)):
            if self.type_time[i] == 0:
                word += self.skill_name[i]
            else:
                self.type_time[i] -= 1
                break
        if self.type_time[-1] != 0 or (self._timer // Const.CUTIN_CURSOR_PERIOD) % 2 != 0:
            word += '_'
        return word
        

class Cutin_big_black_hole(Cutin_text):
    # Cut-in of big black hole
    skill_name = 'Black Hole'


def init_cutin():
    Cutin_big_black_hole.init_convert()