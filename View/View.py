import pygame as pg
import os.path
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

        self.screen = pg.display.set_mode(Const.WINDOW_SIZE, pg.FULLSCREEN)
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

        # draw timer        
        font = pg.font.Font(None, 36)
        timer_surface = font.render(f"time left: {self.model.timer / Const.FPS:.2f}", 1, pg.Color('white'))
        timer_pos = (Const.ARENA_SIZE[0] * 29 / 30, Const.ARENA_SIZE[1] * 1 / 30)
        self.screen.blit(timer_surface, timer_surface.get_rect(center = timer_pos))    

        #draw dashboard
        fontsize = 24
        posX = (Const.WINDOW_SIZE[0] * 7 / 8)
        posY = (Const.WINDOW_SIZE[1] * 1 / 32)
        font = pg.font.Font(None, fontsize)
        heart_image = pg.image.load(os.path.join(Const.IMAGE_PATH, 'heart.png')).convert_alpha()
        heart_image = pg.transform.scale(heart_image, (16, 16))
        
        for player_id in range(1, 5):
            heartposX = posX + 40
            heartposY = posY + (fontsize + 9)
            position = posX, posY
            voltage = round(self.model.players[player_id - 1].voltage, 2)
            item = self.model.players[player_id - 1].keep_item_id
            text = [f"Player {player_id}", "Life:", f"Voltage: {voltage}", f"Item: {item}", "Score:"]
            label = []

            for line in text: 
                label.append(font.render(line, True, pg.Color('white')))
            for line in range(len(label)):
                self.screen.blit(label[line], (position[0], position[1] + (line * (fontsize + 10))))
            for i in range(3):
                self.screen.blit(heart_image, (heartposX, heartposY))
                heartposX += 20
                
            posY += (len(label) - 1) * (fontsize + 15) + (fontsize + 20)
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
        # draw text
        font = pg.font.Font(None, 36)
        text_surface = font.render("Press [space] to restart ...", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center = text_center))

        pg.display.flip()
