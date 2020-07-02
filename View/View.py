import pygame as pg
import os.path
from Events.EventManager import *
from Model.Model import GameEngine
import View.staticobjects as view_staticobjects
import View.animations as view_animations
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
        self.clock = None
        self.last_update = 0
        

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        pg.init()
        pg.font.init()
        pg.display.set_caption(Const.WINDOW_CAPTION)
        self.screen = pg.display.set_mode(Const.WINDOW_SIZE, pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.is_initialized = True

        # convert images
        view_staticobjects.init_staticobjects()
        view_animations.init_animation()
        
        # animations
        self.animation_list = []

        # static objects
        self.scoreboard = view_staticobjects.View_scoreboard(self.model)
        self.players = view_staticobjects.View_players(self.model)
        self.platform = view_staticobjects.View_platform(self.model)
        self.items = view_staticobjects.View_items(self.model)
        self.timer = view_staticobjects.View_timer(self.model)
        self.entities = view_staticobjects.View_entities(self.model)
        self.menu = view_staticobjects.View_menu(self.model)
        self.stop = view_staticobjects.View_stop(self.model)
        self.endgame = view_staticobjects.View_endgame(self.model)


    def notify(self, event):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            self.display_fps()

            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU: self.render_menu()
            elif cur_state == Const.STATE_PLAY: self.render_play()
            elif cur_state == Const.STATE_STOP: self.render_stop()
            elif cur_state == Const.STATE_ENDGAME: self.render_endgame()
        
        elif isinstance(event, EventToggleFullScreen):
            self.toggle_fullscreen()

        elif isinstance(event, EventPlayerAttack):
            self.animation_list.append(view_animations.Animation_player_attack(self.model.players[event.player_id]))

    def display_fps(self):
        '''
        Display the current fps on the window caption.
        '''
        pg.display.set_caption(f'{Const.WINDOW_CAPTION} - FPS: {self.model.clock.get_fps():.2f}')

    def render_menu(self):
        # draw menu
        self.menu.draw(self.screen)
        pg.display.flip()

    def render_play(self):
        
        # draw platform
        self.platform.draw(self.screen)

        # draw players
        self.players.draw(self.screen)        
        
        # draw items
        self.items.draw(self.screen)

        # draw entities
        self.entities.draw(self.screen)
        
        # draw timer        
        self.timer.draw(self.screen)

        #draw scoreboard
        self.scoreboard.draw(self.screen)

        # draw animation
        for ani in self.animation_list:
            if ani.expired: self.animation_list.remove(ani)
            else          : ani.draw(self.screen)
        
        pg.display.flip()

    def render_stop(self):
        # draw stop menu
        self.stop.draw(self.screen)
        pg.display.flip()

    def render_endgame(self):
        
        # draw endgame menu
        self.endgame.draw(self.screen)
        pg.display.flip()

    def toggle_fullscreen(self):
        # save screen content before toggling
        screen = pg.display.get_surface()
        tmp = screen.convert()
        caption = pg.display.get_caption()
        cursor = pg.mouse.get_cursor()
        w, h = screen.get_width(), screen.get_height()
        flags = screen.get_flags()
        bits = screen.get_bitsize()

        pg.display.quit()
        pg.display.init()

        # toggle fullscreen
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            screen = pg.display.set_mode((w, h), pg.FULLSCREEN, bits)
        else:
            screen = pg.display.set_mode((w, h))

        # restore screen content
        screen.blit(tmp, (0, 0))
        pg.display.set_caption(*caption)
        
        pg.key.set_mods(0)
        pg.mouse.set_cursor(*cursor)

        self.screen = screen
