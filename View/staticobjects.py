'''
* "Static" object means that it is rendered every tick!
* The term "static" is designed compared to "animation", which is dynamic.
'''
import pygame as pg
import os.path
import math

import Model.GameObject.item as model_item
from Model.GameObject.entity import CancerBomb , PistolBullet, BananaPeel
from View.utils import scaled_surface, load_image
import Const

'''
VERY IMPORTANT !!!
VERY IMPORTANT !!!
VERY IMPORTANT !!!

Once you add a new class in this module, you have to add CLASS.init_convert()
in the init_otherobjects() function!
'''


class __Object_base():
    images = tuple()

    @classmethod
    def init_convert(cls):
        cls.images = tuple( _image.convert_alpha() for _image in cls.images )

    def __init__(self, model):
        self.model = model


class View_platform(__Object_base):
    def draw(self, screen):
        screen.fill(Const.BACKGROUND_COLOR)
        for platform in self.model.platforms:
            # TODO: refactor the below line to be cleaner
            pg.draw.rect(screen, pg.Color('white'), (*platform.upper_left, *map(lambda x, y: x - y, platform.bottom_right, platform.upper_left)))


class View_menu(__Object_base):
    background = scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'menu.png')), 0.24)

    @classmethod
    def init_convert(cls):
        cls.background = cls.background.convert()

    def draw(self, screen):
        # screen.blit(self.menu, (0, 0))
        # screen.blit(self.base, (10, 645))
        screen.fill(Const.BACKGROUND_COLOR)
        screen.blit(self.background, (0, 0))

        if self.model.stage == Const.NO_STAGE or self.model.random_stage_timer > 0:
            pg.draw.rect(screen, Const.BACKGROUND_COLOR, (466, 692, 267, 42))

        if self.model.stage == Const.STAGE_1:
            highlight = scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'stage_1.png')), 0.24)
            screen.blit(highlight, (219, 389))

        elif self.model.stage == Const.STAGE_2:
            highlight = scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'stage_2.png')), 0.24)
            screen.blit(highlight, (487, 389))

        elif self.model.stage == Const.STAGE_3:
            highlight = scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'stage_3.png')), 0.24)
            screen.blit(highlight, (755, 389))


class View_endgame(__Object_base):
    images = {
        'Background': scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'endgame', 'background.png')), 0.24),
        0: scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'endgame', 'first.png')), 0.24),
        1: scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'endgame', 'second.png')), 0.24),
        2: scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'endgame', 'third.png')), 0.24)
    }

    @classmethod
    def init_convert(cls):
        # TODO: use View.utils.PureText to render static words
        cls.font = pg.font.Font(os.path.join(Const.FONT_PATH, 'bitter', 'Bitter-Bold.ttf'), 28)
        cls.score_font = pg.font.Font(os.path.join(Const.FONT_PATH, 'bitter', 'Bitter-Bold.ttf'), 22)
        # cls.menu = cls.menu.convert()
        # cls.base = cls.base.convert_alpha()
        pass

    def draw(self, screen):
        # draw background
        screen.blit(self.images['Background'], (0, 0))

        for player_id in range(4):
            name_surface = self.font.render(self.model.players[player_id].player_name, 1, pg.Color('white'))
            name_rect = name_surface.get_rect(center=(600 + (player_id - 1.5) * 200, 390))
            screen.blit(name_surface, name_rect)

            score_surface = self.score_font.render(f"{self.model.players[player_id].score}", 1, pg.Color('white'))
            score_rect = score_surface.get_rect(center=(600 + (player_id - 1.5) * 200, 430))
            screen.blit(score_surface, score_rect)

            if 1 <= self.model.players[player_id].rank and self.model.players[player_id].rank <= 3:
                medal_surface = self.images[self.model.players[player_id].rank - 1]
                medal_rect = medal_surface.get_rect(center=(675 + (player_id - 1.5) * 200, 340))
                screen.blit(medal_surface, medal_rect)


class View_players(__Object_base):
    images = tuple(
        scaled_surface(
            load_image(os.path.join(Const.IMAGE_PATH, Const.PLAYER_PIC[_i])),
            0.075 if _i < 20 else 0.15
        )
        for _i in range(0, 40)
    )

    @classmethod
    def init_convert(cls):
        cls.font = pg.font.Font(os.path.join(Const.FONT_PATH, 'Noto', 'NotoSansCJK-Black.ttc'), 15)
        cls.images = tuple( _frame.convert_alpha() for _frame in cls.images )

    def draw(self, screen):
        # draw players
        img_shining_period = (int)(self.model.timer / 7 ) % 5
        for player in self.model.players:
            if player.invincible_time > 0:
                pass

            img_play_state = player.player_id * 5 + img_shining_period + (int)( player.player_radius / Const.PLAYER_RADIUS - 1) * 20
            screen.blit(self.images[img_play_state], self.images[img_play_state].get_rect(center=player.position))

            # temp voltage monitor
            # TODO: create a class MutableText() similar to PureText()
            voltage_surface = self.font.render(f"V = {player.voltage:.0f}", 1, pg.Color('white'))
            voltage_pos = player.position
            screen.blit(voltage_surface, voltage_surface.get_rect(center=voltage_pos))


class View_entities(__Object_base):
    images = {
        'bomber_normal'      : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'entity_bomber.png')), 0.15),
        'bomber_red'  : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'entity_bomber_red.png')), 0.15),
        'banana_bullet': scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'entity_banana_pulp.png')), 0.15),
        'banana_peel' : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'entity_banana_peel.png')), 0.04 * 0.7)
    }

    @classmethod
    def init_convert(cls):
        cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }

    def draw(self, screen):
        # draw players
        for entity in self.model.entities:
            if isinstance(entity, CancerBomb):
                img_bomb = 'bomber_red' if (entity.timer <= 60 or (int)(entity.timer / 9)  % 2 == 0) else 'bomber_normal'
                screen.blit(self.images[img_bomb], self.images[img_bomb].get_rect(center=entity.position))

            elif isinstance(entity, PistolBullet):
                screen.blit(self.images['banana_bullet'], self.images['banana_bullet'].get_rect(center=entity.position))

            elif isinstance(entity, BananaPeel):
                screen.blit(self.images['banana_peel'], self.images['banana_peel'].get_rect(center=entity.position))

            else:
                center = (int(entity.position.x),int(entity.position.y))
                pg.draw.circle(screen, Const.ITEM_COLOR[2], center, 10)


class View_scoreboard(__Object_base):
    images = {
        'Background': scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'scoreboard.png')), 0.24),
        Const.BANANA_PISTOL     : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_bananaGun.png')), 0.04 * 0.7),
        Const.BIG_BLACK_HOLE    : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_blackHole.png')), 0.05 * 0.7),
        Const.CANCER_BOMB       : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_bomber.png')), 0.055 * 0.7),
        Const.ZAP_ZAP_ZAP       : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_lightning.png')), 0.06 * 0.7),
        Const.BANANA_PEEL       : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_bananaPeel.png')), 0.04 * 0.7),
        Const.RAINBOW_GROUNDER  : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_rainbowGrounder.png')), 0.05 * 0.7),
        Const.INVINCIBLE_BATTERY: scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_battery.png')), 0.05 * 0.7)
    }

    @classmethod
    def init_convert(cls):
        cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }
        cls.namefont = pg.font.Font(os.path.join(Const.FONT_PATH, 'bitter', 'Bitter-Bold.ttf'), 15)
        cls.numfont = pg.font.Font(os.path.join(Const.FONT_PATH, 'bitter', 'Bitter-Bold.ttf'), 16)

    def draw(self, screen):
        background = self.images['Background']
        screen.blit(background, (0, 0))

        name_posx = [44, 303, 700, 959]
        voltage_posx = name_posx
        item_posx = name_posx
        live_posx = name_posx
        for player_id in range(4):
            name_surface = self.namefont.render(self.model.players[player_id].player_name, 1, pg.Color('white'))
            screen.blit(name_surface, (name_posx[player_id], 683))

            voltage_surface = self.numfont.render(f"{self.model.players[player_id].voltage:.1f}", 1, pg.Color('white'))
            voltage_rect = voltage_surface.get_rect()
            voltage_rect.topright = (voltage_posx[player_id] + 136, 713)
            screen.blit(voltage_surface, voltage_rect)

            score_surface = self.numfont.render(f"{self.model.players[player_id].score}", 1, pg.Color('white'))
            score_rect = score_surface.get_rect()
            score_rect.topright = (voltage_posx[player_id] + 136, 739)
            screen.blit(score_surface, score_rect)

            if self.model.players[player_id].keep_item_id != Const.NO_ITEM:
                screen.blit(
                    self.images[self.model.players[player_id].keep_item_id],
                    self.images[self.model.players[player_id].keep_item_id].get_rect(center=(item_posx[player_id] + 177, 742))
                )

            lives = self.model.players[player_id].life
            pg.draw.rect(screen, Const.BACKGROUND_COLOR, (live_posx[player_id] + 118, 686, 18 * (5 - lives), 15))



        # fontsize = 24
        # posX = (Const.WINDOW_SIZE[0] * 7 / 8)
        # posY = (Const.WINDOW_SIZE[1] * 1 / 32)
        # heart_image = self.images['Heart']
        # for player_id in range(1, 5):
        #     heartposX = posX + 43
        #     heartposY = posY + (fontsize + 14)
        #     position = posX, posY
        #     # TODO: f'Voltage: {voltage:.2f}'
        #     voltage = round(self.model.players[player_id - 1].voltage, 2)
        #     item = self.model.players[player_id - 1].keep_item_id
        #     score = self.model.players[player_id - 1].score
        #     text = [f"Player {player_id}", "Life: ", f"Voltage: {voltage}", f"Item: {item}", f"Score: {score}"]
        #     # TODO: no need to use a list to store the labels
        #     label = []

        #     # TODO: merge the for loop with the following one
        #     for line in text:
        #         label.append(self.namefont.render(line, True, pg.Color('white')))

        #     # TODO: merge the for loop with the previous one
        #     # draw words
        #     for line in range(len(label)):
        #         screen.blit(label[line], (position[0], position[1] + (line * (fontsize + 10))))

        #     # draw heart
        #     lives = self.model.players[player_id - 1].life
        #     for i in range(lives):
        #         screen.blit(heart_image, (heartposX, heartposY))
        #         heartposX += 20
        #     posY += (len(label) - 1) * (fontsize + 15) + (fontsize + 20)


class View_items(__Object_base):
    images = {
        Const.BANANA_PISTOL     : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_bananaGun.png')), 0.04),
        Const.BIG_BLACK_HOLE    : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_blackHole.png')), 0.05),
        Const.CANCER_BOMB       : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_bomber.png')), 0.055),
        Const.ZAP_ZAP_ZAP       : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_lightning.png')), 0.06),
        Const.BANANA_PEEL       : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_bananaPeel.png')), 0.04),
        Const.RAINBOW_GROUNDER  : scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_rainbowGrounder.png')), 0.05),
        Const.INVINCIBLE_BATTERY: scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'item_battery.png')), 0.05)
    }

    @classmethod
    def init_convert(cls):
        cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }

    def draw(self, screen):
        # for market in self.model.priced_market_list:
        #     if market.item:
        #         screen.blit(self.images[market.item.name], self.images[market.item.name].get_rect(center=(401, 398)))
        floating = (0, Const.FLOATING_RADIUS * math.sin(Const.FLOATING_THETA*self.model.timer))
        for item in self.model.items:
            screen.blit(self.images[item.item_id], self.images[item.item_id].get_rect(center=item.position + floating))
            #pg.draw.circle(screen, Const.ITEM_COLOR[item.item_id], center, item.item_radius)
            #font = pg.font.Font(None, 15)
            #item_surface = font.render(f"{item.item_id:d}", 1, pg.Color('black'))
            #item_pos = item.position
            #screen.blit(item_surface, item_surface.get_rect(center = item_pos))

class View_stop(__Object_base):
    images = {
        'Background0': scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'pause', 'paused0.png')), 0.24),
        'Background1': scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'pause', 'paused1.png')), 0.24),
        'Background2': scaled_surface(load_image(os.path.join(Const.IMAGE_PATH, 'pause', 'paused2.png')), 0.24)
    }

    @classmethod
    def init_convert(cls):
        cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }

    def draw(self, screen):
        screen.blit(self.images[f'Background{self.model.stop_screen_index}'], (0, 0))


class View_timer(__Object_base):

    @classmethod
    def init_convert(cls):
        #cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }
        cls.font = pg.font.Font(os.path.join(Const.FONT_PATH, 'bitter', 'Bitter-Bold.ttf'), 18)

    def draw(self, screen):
        # for market in self.model.priced_market_list:
        #     if market.item:
        #         screen.blit(self.images[market.item.name], self.images[market.item.name].get_rect(center=(401, 398)))
        # TODO: create a class MutableText() similar to PureText()
        timer_surface = self.font.render(f"{self.model.timer / Const.FPS:.0f}", 1, pg.Color('white'))
        timer_rect = timer_surface.get_rect()
        timer_rect.midright = (642, 752)
        screen.blit(timer_surface, timer_rect)


def init_staticobjects():
    View_platform.init_convert()
    View_endgame.init_convert()
    View_players.init_convert()
    View_items.init_convert()
    View_entities.init_convert()
    View_scoreboard.init_convert()
    View_menu.init_convert()
    View_timer.init_convert()
    View_stop.init_convert()
