'''
* How to add a cut-in:

class Cutin_example(Cutin_text):
    skill_name = 'A great name of your skill'

    # Override draw() function to modify the place text appeard
    def draw():
        ...
'''
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

    def __init__(self):
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
    images = {
        'board' : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'cutin', 'board.png')), 0.2),
    }

    # TODO(?): Image of player
    players_image = tuple(
        scaled_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', Const.PLAYER_PIC[_i])),
            0.0375
        )
        for _i in range(0, 20, 5)
    )

    @classmethod
    def init_convert(cls):
        cls.players_image = tuple( _player.convert_alpha() for _player in cls.players_image)
        cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }

    def __init__(self, player_id, expire_time=Const.FPS):
        self.player_id = player_id
        self._timer = 0
        self.expire_time = expire_time
        self.expired = False
        self.board_height = self.images['board'].get_height()
        self.board_width = self.images['board'].get_width()
        self.board_speed = Const.CUTIN_BOARD_INITIAL_SPEED
        self.board_position = list(Const.CUTIN_BOARD_INITIAL_POSITION)
        self.board_up = False
        self.board_stop = False

    def update(self):
        # Scroll the board back and set expired to true after board become invisible
        self._timer += 1
        self.update_board_position()
        if self._timer == self.expire_time:
            self.board_up = True
        if self.board_position[1] < -2 * self.board_height:
            self.expired = True

    def draw(self, screen, update=True):
        # Draw board with image of player
        self.board = self.images['board'].copy()

        self.board.blit(
            self.players_image[self.player_id],
            self.players_image[self.player_id].get_rect(center=(self.board_width / 2, self.board_height / 2))
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
            distance = self.board_height / 2 - self.board_position[1]
            if distance < 0:
                self.board_speed *= -Const.CUTIN_BOARD_ATTENUATION_COEFFICIENT
                self.board_position[1] += 2 * distance
                self.board_stop = True
            if abs(self.board_speed) < Const.CUTIN_SPEED_MINIMUM:
                self.board_speed = 0
                self.board_position[1] = self.board_height / 2
        # Board up
        else:
            self.board_position[1] += 2 * self.board_speed / Const.FPS
            self.board_speed -= Const.CUTIN_GRAVITY / Const.FPS


class Cutin_raster(Cutin_board):
    '''
    Base class of all cut-ins that need to show text on board
    '''
    skill_name = 'Skill Name'
    images = {
        'board' : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'cutin', 'board.png')), 0.2),
        'emoticon_1' : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'players', 'ball_emoticon_first.png')), 0.27),
        'emoticon_2' : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'players', 'ball_emoticon_second.png')), 0.27),
        'emoticon_3' : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'players', 'ball_emoticon_third.png')), 0.27),
        'emoticon_4' : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'players', 'ball_emoticon_fourth.png')), 0.27),
    }
    def __init__(self, player_id, players, ev_manager : EventManager):
        # Add type_time to random type speed of typewriter
        super().__init__(player_id)
        self.rank = self.ranking(players)
        self.type_time = np.zeros(len(self.skill_name), dtype=np.int8)
        self.type_time[1:] = np.random.randint(5, 10, size=len(self.skill_name) - 1)
        self.fontLarge = pg.font.Font(os.path.join(Const.FONT_PATH, 'bitter', 'Bitter-Bold.ttf'), 54)
        self.fontSmall = pg.font.Font(os.path.join(Const.FONT_PATH, 'bitter', 'Bitter-Bold.ttf'), 6)
        self.stay_time = Const.CUTIN_STAY_TIME # The time cut-in would stay after every thing finish
        self.text_type = False
        self.ev_manager = ev_manager

    def update(self):
        # Update board position and update the state
        self._timer += 1
        self.update_board_position()
        if self.board_stop:
            self.text_type = True
        if self.type_time[-1] == 0:
            self.stay_time -= 1
        if self.stay_time == 0:
            self.board_up = True
        if self.board_position[1] < -2 * self.board_height:
            self.expired = True

    def draw(self, screen, update=True):
        # Draw board with name of skill and player
        # Draw player on board
        self.board = self.images['board'].copy()
        player = self.players_image[self.player_id].copy()

        # Draw emotion on player
        self.emotion_draw(player)

        self.board.blit(
            player,
            player.get_rect(center=(5 * self.board_width / 7, 5 * self.board_height / 6))
        )

        # Update text to show
        text = self.text()

        # Draw skill's name on board
        text_surface = self.fontLarge.render(text, 1, pg.Color('white'))
        self.board.blit(
            text_surface,
            (self.board_width / 11, 3 * self.board_height / 7)
        )

        text_on_laptop = self.fontSmall.render(text, 1, pg.Color('white'))
        text_on_laptop = pg.transform.rotate(text_on_laptop, 32)
        self.board.blit(
            text_on_laptop,
            text_on_laptop.get_rect(bottomleft=(256, 394))
        )

        # Draw board to screen
        screen.blit(
            self.board,
            self.board.get_rect(center=self.board_position)
        )

        if update:
            self.update()

    def emotion_draw(self, target):
        target.blit(
            self.images[self.rank],
            self.images[self.rank].get_rect(center=(target.get_width() / 2, target.get_height() / 2))
        )

    def text(self):
        # Determine the text to show
        if not self.text_type:
            return ''
        word = ''
        for i in range(len(self.type_time)):
            if self.type_time[i] == 0:
                word += self.skill_name[i]
            else:
                self.type_time[i] -= 1
                if self.type_time[i] == 0:
                    self.ev_manager.post(EventTypeSound())
                break
        if self.type_time[-1] != 0 or (self._timer // Const.CUTIN_CURSOR_PERIOD) % 2 != 0:
            word += '_'
        return word

    def ranking(self, players):
        rank = 1
        for player in players:
            if player.player_id != self.player_id and player.score > players[self.player_id].score:
                rank += 1
        return rank


class Cutin_big_black_hole(Cutin_raster):
    # Cut-in of big black hole
    skill_name = 'Black Hole'
    images = {
        'board' : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'cutin', 'board.png')), 0.2),
        'big_black_hole' : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_blackHole_normal.png')), 0.2),
        1 : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'players', 'ball_emoticon_first.png')), 0.27),
        2 : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'players', 'ball_emoticon_second.png')), 0.27),
        3 : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'players', 'ball_emoticon_third.png')), 0.27),
        4 : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'players', 'ball_emoticon_fourth.png')), 0.27),
    }

    def draw(self, screen, update=True):
        # Draw board with name of skill and player
        # Draw player on board
        self.board = self.images['board'].copy()
        player = self.players_image[self.player_id].copy()
        # Draw emotion on player
        self.emotion_draw(player)

        self.board.blit(
            player,
            player.get_rect(center=(5 * self.board_width / 7, 5 * self.board_height / 6))
        )

        # Draw big black hole
        self.board.blit(
            self.images['big_black_hole'],
            self.images['big_black_hole'].get_rect(center=(self.board_width / 4, 4 * self.board_height / 5))
        )

        # Update text to show
        text = self.text()

        # Draw skill's name on board
        text_surface = self.fontLarge.render(text, 1, pg.Color('white'))
        self.board.blit(
            text_surface,
            (self.board_width / 11, 3 * self.board_height / 7)
        )

        text_on_laptop = self.fontSmall.render(text, 1, pg.Color('white'))
        text_on_laptop = pg.transform.rotate(text_on_laptop, 32)
        self.board.blit(
            text_on_laptop,
            text_on_laptop.get_rect(bottomleft=(256, 394))
        )

        # Draw board to screen
        screen.blit(
            self.board,
            self.board.get_rect(center=self.board_position)
        )

        if update:
            self.update()


class Cutin_zap_zap_zap(Cutin_raster):
    # Cut-in of big black hole
    skill_name = 'Lightning'
    images = {
        'board' : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'cutin', 'board.png')), 0.2),
        'lightning' : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'lightning.png')), 0.12),
        1 : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'players', 'ball_emoticon_first.png')), 0.27),
        2 : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'players', 'ball_emoticon_second.png')), 0.27),
        3 : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'players', 'ball_emoticon_third.png')), 0.27),
        4 : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'players', 'ball_emoticon_fourth.png')), 0.27),
    }

    def draw(self, screen, update=True):
        # Draw board with name of skill and player
        # Draw player on board
        self.board = self.images['board'].copy()
        player = self.players_image[self.player_id].copy()
        # Draw emotion on player
        self.emotion_draw(player)

        self.board.blit(
            player,
            player.get_rect(center=(5 * self.board_width / 7, 5 * self.board_height / 6))
        )

        # Update text to show
        text = self.text()

        # Draw skill's name on board
        text_surface = self.fontLarge.render(text, 1, pg.Color('white'))
        self.board.blit(
            text_surface,
            (self.board_width / 11, 3 * self.board_height / 7)
        )

        text_on_laptop = self.fontSmall.render(text, 1, pg.Color('white'))
        text_on_laptop = pg.transform.rotate(text_on_laptop, 32)
        self.board.blit(
            text_on_laptop,
            text_on_laptop.get_rect(bottomleft=(256, 394))
        )

        # Draw lightning
        self.board.blit(
            self.images['lightning'],
            self.images['lightning'].get_rect(center=(self.board_width / 4, 4 * self.board_height / 5))
        )

        # Draw board to screen
        screen.blit(
            self.board,
            self.board.get_rect(center=self.board_position)
        )

        if update:
            self.update()


def init_cutin():
    Cutin_big_black_hole.init_convert()
    Cutin_zap_zap_zap.init_convert()
