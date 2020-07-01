import pygame as pg

from Events.EventManager import *
from Model.Model import GameEngine
import Const


class GraphicalView:
    '''
    Draws the state of GameEngine onto the screen.
    '''
    background = pg.Surface(Const.ARENA_SIZE)

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        '''
        This function is called when the GraphicalView is created.
        For more specific objects related to a game instance
            , they should be initialized in GraphicalView.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.model = model

        self.screen = pg.display.set_mode(Const.WINDOW_SIZE)
        pg.display.set_caption(Const.WINDOW_CAPTION)
        self.background.fill(Const.BACKGROUND_COLOR)

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        pass

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

    def display_fps(self):
        '''
        Display the current fps on the window caption.
        '''
        pg.display.set_caption(f'{Const.WINDOW_CAPTION} - FPS: {self.model.clock.get_fps():.2f}')

    def render_menu(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # draw text
        font = pg.font.Font(None, 36)
        text_surface = font.render("Press [space] to start ...", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center = text_center))

        pg.display.flip()

    def render_play(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # draw players
        for player in self.model.players:
            if not player.is_alive():
                continue
            if player.invincible_time > 0:
                pass
            center = list(map(int, player.position))
            pg.draw.circle(self.screen, Const.PLAYER_COLOR[player.player_id], center, player.player_radius)
            # temp voltage monitor
            font = pg.font.Font(None, 20)
            voltage_surface = font.render(f"V = {player.voltage:.0f}", 1, pg.Color('white'))
            voltage_pos = player.position
            self.screen.blit(voltage_surface, voltage_surface.get_rect(center = voltage_pos))    

        # draw platforms
        for platform in self.model.platforms:
            pg.draw.rect(self.screen, pg.Color('white'), (*platform.upper_left, *map(lambda x, y: x - y, platform.bottom_right, platform.upper_left)))
        
        # draw items
        for item in self.model.items:
            center = list(map(int, item.position))
            pg.draw.circle(self.screen, Const.ITEM_COLOR[item.item_id], center, item.item_radius)
            # temp item id monitor
            font = pg.font.Font(None, 15)
            item_surface = font.render(f"{item.item_id:d}", 1, pg.Color('black'))
            item_pos = item.position
            self.screen.blit(item_surface, item_surface.get_rect(center = item_pos))

        # draw entities
        for entity in self.model.entities:
            center = list(map(int, entity.position))
            pg.draw.circle(self.screen, Const.ITEM_COLOR[2], center, 10)
        
        # draw temp score board 
        font = pg.font.Font(None, 36)
        for player in self.model.players:
            player_surface = font.render(f"player{player.player_id :d}:", 1, Const.PLAYER_COLOR[player.player_id])
            player_pos = (Const.WINDOW_SIZE[0] * 5 / 6, Const.WINDOW_SIZE[1] * (1 + 4 * player.player_id) / 30)
            self.screen.blit(player_surface, player_surface.get_rect(center = player_pos))
            lives_surface = font.render(f"                lives left: {player.life :d}", 1, Const.PLAYER_COLOR[player.player_id])
            lives_pos = (Const.WINDOW_SIZE[0] * 5 / 6, Const.WINDOW_SIZE[1] * (2 + 4 * player.player_id) / 30)
            self.screen.blit(lives_surface, lives_surface.get_rect(center = lives_pos))
            KO_surface = font.render(f"                KO: {player.KO_amount :d}", 1, Const.PLAYER_COLOR[player.player_id])
            KO_pos = (Const.WINDOW_SIZE[0] * 5 / 6, Const.WINDOW_SIZE[1] * (3 + 4 * player.player_id) / 30)
            self.screen.blit(KO_surface, KO_surface.get_rect(center = KO_pos))
            be_KO_surface = font.render(f"                be KO: {player.be_KO_amount :d}", 1, Const.PLAYER_COLOR[player.player_id])
            be_KO_pos = (Const.WINDOW_SIZE[0] * 5 / 6, Const.WINDOW_SIZE[1] * (4 + 4 * player.player_id) / 30)
            self.screen.blit(be_KO_surface, be_KO_surface.get_rect(center = be_KO_pos))
            
        # draw timer        
        font = pg.font.Font(None, 36)
        timer_surface = font.render(f"time left: {self.model.timer / Const.FPS:.2f}", 1, pg.Color('white'))
        timer_pos = (Const.ARENA_SIZE[0] * 29 / 30, Const.ARENA_SIZE[1] * 1 / 30)
        self.screen.blit(timer_surface, timer_surface.get_rect(center = timer_pos))
        
        pg.display.flip()

    def render_stop(self):
        # draw text
        font = pg.font.Font(None, 36)
        text_surface = font.render("Press [space] to continue ...", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center = text_center))
        
        pg.display.flip()

    def render_endgame(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)
        
        # draw score board
        font = pg.font.Font(None, 36)
        for player in self.model.players:
            player_surface = font.render(f"player{player.player_id :d}:", 1, Const.PLAYER_COLOR[player.player_id])
            player_pos = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] * (1 + 4 * player.player_id) / 25)
            self.screen.blit(player_surface, player_surface.get_rect(center = player_pos))
            lives_surface = font.render(f"                lives left: {player.life :d}", 1, Const.PLAYER_COLOR[player.player_id])
            lives_pos = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] * (2 + 4 * player.player_id) / 25)
            self.screen.blit(lives_surface, lives_surface.get_rect(center = lives_pos))
            KO_surface = font.render(f"                KO: {player.KO_amount :d}", 1, Const.PLAYER_COLOR[player.player_id])
            KO_pos = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] * (3 + 4 * player.player_id) / 25)
            self.screen.blit(KO_surface, KO_surface.get_rect(center = KO_pos))
            be_KO_surface = font.render(f"                be KO: {player.be_KO_amount :d}", 1, Const.PLAYER_COLOR[player.player_id])
            be_KO_pos = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] * (4 + 4 * player.player_id) / 25)
            self.screen.blit(be_KO_surface, be_KO_surface.get_rect(center = be_KO_pos))


        # draw text
        text_surface = font.render("Press [space] to restart ...", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 10 * 8)
        self.screen.blit(text_surface, text_surface.get_rect(center = text_center))

        pg.display.flip()
