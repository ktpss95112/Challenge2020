import pygame as pg
import os.path
from Events.EventManager import *
from Model.Model import GameEngine
from View.utils import scaled_surface, load_image
import View.staticobjects
import View.animations
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
        self.stop_screen = None
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
        self.screen = pg.display.set_mode(Const.WINDOW_SIZE, pg.FULLSCREEN)
        self.stop_screen = pg.Surface(Const.WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.is_initialized = True

        # convert images
        View.staticobjects.init_staticobjects()
        View.animations.init_animation()

        # animations
        self.animation_list = []

        # static objects
        self.scoreboard = View.staticobjects.View_scoreboard(self.model)
        self.players = View.staticobjects.View_players(self.model)
        self.platform = View.staticobjects.View_platform(self.model)
        self.items = View.staticobjects.View_items(self.model)
        self.timer = View.staticobjects.View_timer(self.model)
        self.entities = View.staticobjects.View_entities(self.model)
        self.menu = View.staticobjects.View_menu(self.model)
        self.endgame = View.staticobjects.View_endgame(self.model)

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

        elif isinstance(event, EventContinue):
            self.current_stop_index = None

        elif isinstance(event, EventPlayerAttack):
            if self.model.players[event.player_id].player_radius / Const.PLAYER_RADIUS == 1:
                self.animation_list.append(View.animations.Animation_player_attack(self.model.players[event.player_id]))
            else:
                self.animation_list.append(View.animations.Animation_player_attack_big(self.model.players[event.player_id]))

        elif isinstance(event, EventStop):
            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU: self.render_menu(target=self.stop_screen, update=False)
            elif cur_state == Const.STATE_PLAY: self.render_play(target=self.stop_screen, update=False)
            elif cur_state == Const.STATE_ENDGAME: self.render_endgame(target=self.stop_screen, update=False)

        elif isinstance(event, EventBombExplode):
            self.animation_list.append(View.animations.Animation_Bomb_Explode(center=event.position))

        elif isinstance(event, EventUseZapZapZap):
            self.animation_list.append(View.animations.Animation_Lightning(event.player_position.x))

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

        # draw platform
        self.platform.draw(target)

        # draw players
        self.players.draw(target)

        # draw items
        self.items.draw(target)

        # draw entities
        self.entities.draw(target)

        # draw animation
        for ani in self.animation_list:
            if ani.expired: self.animation_list.remove(ani)
            else          : ani.draw(target, update)

        # draw scoreboard
        self.scoreboard.draw(target)

        # draw timer
        self.timer.draw(target)


        pg.display.flip()

    def render_stop(self):
        if self.current_stop_index == self.model.stop_screen_index:
            return
        
        self.current_stop_index = self.model.stop_screen_index

        self.stop_screen = scaled_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'pause', f'paused{self.current_stop_index}.png')),
            0.24
        )
        
        self.screen.blit(self.stop_screen, (0, 0))

        # font = pg.font.Font(os.path.join(Const.FONT_PATH, 'Noto', 'NotoSansCJK-Black.ttc'), 36)
        # text_surface = font.render("Press [space] to continue ...", 1, pg.Color('gray88'))
        # text_center = (Const.WINDOW_SIZE[0] / 2, Const.WINDOW_SIZE[1] / 2)
        # self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

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
        self.ev_manager.post(EventContinue())
