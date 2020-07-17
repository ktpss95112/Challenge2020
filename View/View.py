import pygame as pg
import os.path
from Events.EventManager import *
from Model.Model import GameEngine
from View.utils import scaled_surface, load_image
import View.staticobjects
import View.animations
import View.cutins
import View.sounds
import Const


class GraphicalView:
    '''
    Draws the state of GameEngine onto the screen.
    '''
    background = pg.Surface(Const.ARENA_SIZE)
    fullscreen = True

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        '''
        This function is called when the GraphicalView is created.
        For more specific objects related to a game instance
            , they should be initialized in GraphicalView.initialize()
        '''

        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.model = model
        self.is_initialized = False
        self.screen = None
        self.stop_background = None
        self.cutin_screen = None
        self.clock = None
        self.last_update = 0
        self.current_stop_index = None

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        pg.init()
        pg.font.init()
        pg.display.set_caption(Const.WINDOW_CAPTION)
        if not self.is_initialized:
            try:
                self.screen = pg.display.set_mode(Const.WINDOW_SIZE, pg.FULLSCREEN)
                self.low_resolution = False
            except pg.error:
                self.low_resolution = True
                self.real_window_size = (Const.WINDOW_SIZE[0] * 2 // 3, Const.WINDOW_SIZE[1] * 2 // 3)
                self.real_screen = pg.display.set_mode(self.real_window_size, pg.FULLSCREEN)
                self.screen = pg.Surface(Const.WINDOW_SIZE)
        self.cutin_screen = pg.Surface(Const.WINDOW_SIZE)
        self.stop_background = pg.Surface(Const.WINDOW_SIZE)
        self.clock = pg.time.Clock()

        # convert images
        if not self.is_initialized:
            View.staticobjects.init_staticobjects()
            View.animations.init_animation()
            View.cutins.init_cutin()

        # animations
        self.animation_list = []
        self.animation_black_hole_list = [] # should be rendered lastly

        # cut-ins
        self.cutin_list = []

        # static objects
        self.scoreboard = View.staticobjects.View_scoreboard(self.model)
        self.players = View.staticobjects.View_players(self.model)
        self.platform = View.staticobjects.View_platform(self.model)
        self.items = View.staticobjects.View_items(self.model)
        self.timer = View.staticobjects.View_timer(self.model)
        self.entities = View.staticobjects.View_entities(self.model)
        self.menu = View.staticobjects.View_menu(self.model)
        self.endgame = View.staticobjects.View_endgame(self.model)
        self.stop = View.staticobjects.View_stop(self.model)
        self.stage = View.staticobjects.View_stage(self.model)

        self.is_initialized = True

    def notify(self, event):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        if isinstance(event, EventRestart):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            self.display_fps()

            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU: self.render_menu()
            elif cur_state == Const.STATE_PLAY: self.render_play()
            elif cur_state == Const.STATE_STOP: self.render_stop()
            elif cur_state == Const.STATE_CUTIN: self.render_cutin()
            elif cur_state == Const.STATE_ENDGAME: self.render_endgame()

            if self.low_resolution:
                self.real_screen.blit(pg.transform.smoothscale(self.screen, self.real_window_size), (0, 0))
                pg.display.flip()

        elif isinstance(event, EventToggleFullScreen):
            self.toggle_fullscreen()

        elif isinstance(event, EventContinue):
            self.current_stop_index = None

        elif isinstance(event, EventPlayerAttack):
            if self.model.players[event.player_id].player_radius / Const.PLAYER_RADIUS == 1:
                self.animation_list.append(View.animations.Animation_player_attack(self.model.players[event.player_id]))
            else:
                self.animation_list.append(View.animations.Animation_player_attack_big(self.model.players[event.player_id]))

        elif isinstance(event, EventStop):
            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU: self.render_menu(target=self.stop_background, update=False)
            elif cur_state == Const.STATE_PLAY: self.render_play(target=self.stop_background, update=False)
            elif cur_state == Const.STATE_ENDGAME: self.render_endgame(target=self.stop_background, update=False)

        elif isinstance(event, EventBombExplode):
            self.animation_list.append(View.animations.Animation_Bomb_Explode(center=event.position))

        elif isinstance(event, EventCutInStart):
            self.render_play(self.cutin_screen)
            if event.item_id == Const.BIG_BLACK_HOLE:
                self.cutin_list.append(View.cutins.Cutin_big_black_hole(event.player_id, self.model.players, self.ev_manager))
            elif event.item_id == Const.ZAP_ZAP_ZAP:
                self.cutin_list.append(View.cutins.Cutin_zap_zap_zap(event.player_id, self.model.players, self.ev_manager))

        elif isinstance(event, EventUseZapZapZap):
            self.animation_list.append(View.animations.Animation_Lightning(event.player_position.x))

        elif isinstance(event, EventUseRainbowGrounder):
            self.animation_list.append(View.animations.Animation_Rainbow(center=event.player_position))

        elif isinstance(event, EventDeathRainTrigger):
            self.animation_list.append(View.animations.Animation_Gift_Explode(center=event.position))

        elif isinstance(event, EventUseBigBlackHole):
            self.animation_black_hole_list.append(View.animations.Animation_Black_Hole(event.black_hole_position))

    def display_fps(self):
        '''
        Display the current fps on the window caption.
        '''
        pg.display.set_caption(f'{Const.WINDOW_CAPTION} - FPS: {self.model.clock.get_fps():.2f}')

    def render_menu(self, target=None, update=True):
        if target is None:
            target = self.screen

        # draw menu
        self.menu.draw(target)
        pg.display.flip()

    def render_play(self, target=None, update=True):
        if target is None:
            target = self.screen

        # draw
        self.stage.draw(target)
        self.platform.draw(target)
        self.players.draw(target)
        self.items.draw(target)
        self.entities.draw(target)

        for ani in self.animation_list:
            if ani.expired and isinstance(ani, View.animations.Animation_Gift_Explode):
                self.ev_manager.post(EventDeathRainStart())
            if ani.expired: self.animation_list.remove(ani)
            else          : ani.draw(target, update)

        for ani in self.animation_black_hole_list:
            if ani.expired: self.animation_black_hole_list.remove(ani)
            else          : ani.draw(target, update)

        self.scoreboard.draw(target)
        self.timer.draw(target)

        pg.display.flip()

    def render_stop(self, target=None, update=True):
        if target is None:
            target = self.screen

        if self.current_stop_index == self.model.stop_screen_index:
            return

        self.current_stop_index = self.model.stop_screen_index

        self.stop.draw(target)

        pg.display.flip()

    def render_cutin(self, target=None, update=True):
        if target is None:
            target = self.screen
        # self.render_play()
        target.blit(self.cutin_screen, (0, 0))
        if not self.cutin_list:
            self.ev_manager.post(EventCutInEnd())
            return

        if self.cutin_list[0].expired: self.cutin_list.pop(0)
        else:                          self.cutin_list[0].draw(target, True)

        pg.display.flip()

    def render_endgame(self, target=None, update=True):
        if target is None:
            target = self.screen

        # draw endgame menu
        self.endgame.draw(target)
        pg.display.flip()

    def toggle_fullscreen(self):
        self.ev_manager.post(EventStop())
        # save screen content before toggling
        _screen = pg.display.get_surface()
        tmp = _screen.convert()
        caption = pg.display.get_caption()
        cursor = pg.mouse.get_cursor()
        w, h = _screen.get_width(), _screen.get_height()
        flags = _screen.get_flags()
        bits = _screen.get_bitsize()

        pg.display.quit()
        pg.display.init()

        # toggle fullscreen
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            _screen = pg.display.set_mode((w, h), pg.FULLSCREEN, bits)
        else:
            _screen = pg.display.set_mode((w, h))

        # restore _screen content
        _screen.blit(tmp, (0, 0))
        pg.display.set_caption(*caption)

        pg.key.set_mods(0)
        pg.mouse.set_cursor(*cursor)

        if self.low_resolution:
            self.real_screen = _screen
        else:
            self.screen = _screen
        self.ev_manager.post(EventContinue())
