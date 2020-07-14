import pygame as pg
import random
from Events.EventManager import *
from Model.Model import GameEngine
import Const


class Controller:
    '''
    Handles the control input. Either from keyboard or from AI.
    '''

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        '''
        This function is called when the Controller is created.
        For more specific objects related to a game instance
            , they should be initialized in Controller.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.model = model

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        pass

    def notify(self, event: BaseEvent):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            key_down_events = []
            # Called once per game tick. We check our keyboard presses here.
            for event_pg in pg.event.get():
                # handle window manager closing our window
                if event_pg.type == pg.QUIT:
                    self.ev_manager.post(EventQuit())
                if event_pg.type == pg.KEYDOWN:
                    key_down_events.append(event_pg)

            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU: self.ctrl_menu(key_down_events)
            if cur_state == Const.STATE_PLAY: self.ctrl_play(key_down_events)
            if cur_state == Const.STATE_STOP: self.ctrl_stop(key_down_events)
            if cur_state == Const.STATE_ENDGAME: self.ctrl_endgame(key_down_events)

    def check_screen_keys(self, key):
        '''
        check the keys that should be caught regardless of game state
        for example: FULL_SCREEN_KEY
        TODO: change volume
        '''
        if key == Const.GAME_FULLSCREEN_KEY:
            self.ev_manager.post(EventToggleFullScreen())

    def ctrl_menu(self, key_down_events):
        for event_pg in key_down_events:
            try:
                Const.menu_keys[event_pg.key](self)
            except KeyError:
                pass
            if self.model.stage != Const.NO_STAGE and self.model.random_stage_timer == 0:
                if event_pg.type == pg.KEYDOWN and event_pg.key == pg.K_SPACE:
                    self.ev_manager.post(EventPlay())
            self.check_screen_keys(event_pg.key)

    def ctrl_play(self, key_down_events):
        keys = pg.key.get_pressed()
        for k, v in Const.PLAYER_MOVE_KEYS.items():
            if keys[k]:
                self.ev_manager.post(EventPlayerMove(*v))

        for event_pg in key_down_events:
            try:
                Const.handle_keys[event_pg.key](self, self.model)
            except KeyError:
                pass
            # detect stop event
            if event_pg.key == Const.GAME_STOP_KEY:
                self.ev_manager.post(EventStop())
            else:
                self.check_screen_keys(event_pg.key)

    def ctrl_stop(self, key_down_events):
        # detect continue event
        for event_pg in key_down_events:
            if event_pg.key == Const.GAME_CONTINUE_KEY:
                self.ev_manager.post(EventContinue())
            else:
                self.check_screen_keys(event_pg.key)

    def ctrl_endgame(self, key_down_events):
        # detect restart event
        for event_pg in key_down_events:
            if event_pg.key == Const.GAME_RESTART_KEY:
                self.model.ev_manager.post(EventRestart())
            else:
                self.check_screen_keys(event_pg.key)

