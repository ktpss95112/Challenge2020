'''
* "Static" object means that it is rendered every tick!
* The term "static" is designed compared to "animation", which is dynamic.
'''
import pygame as pg
import os.path
import math

import Model.GameObject.item as model_item
import View.utils as view_utils
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
    # background = view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'background.png')), 1)
    # priced_market = view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'market.png')), 0.3)

    @classmethod
    def init_convert(cls):
        # cls.background = cls.background.convert()
        # cls.priced_market = cls.priced_market.convert()
        pass

    def draw(self, screen):
        screen.fill(Const.BACKGROUND_COLOR)
        for platform in self.model.platforms:
            pg.draw.rect(screen, pg.Color('white'), (*platform.upper_left, *map(lambda x, y: x - y, platform.bottom_right, platform.upper_left)))

class View_menu(__Object_base):
    # menu = view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'menu.png')), 1)
    # base = view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'base.png')), 0.5)

    @classmethod
    def init_convert(cls):
        # cls.menu = cls.menu.convert()
        # cls.base = cls.base.convert_alpha()
        pass

    def draw(self, screen):
        # screen.blit(self.menu, (0, 0))
        # screen.blit(self.base, (10, 645))
        screen.fill(Const.BACKGROUND_COLOR)

        titlefont = pg.font.Font(os.path.join(Const.FONT_PATH, 'digitalt', 'Digitalt.ttf'), 125)
        titlesmallfont = pg.font.Font(os.path.join(Const.FONT_PATH, 'Noto', 'NotoSansCJK-Black.ttc'), 20)

        words_1 = titlefont.render     ('Electroshock', True, pg.Color('white'))
        words_2 = titlesmallfont.render('presented by 2020 NTU CSIE CAMP', True, pg.Color('white'))
        words_3 = titlesmallfont.render('press [space] to start game', True, pg.Color('white'))
        (size_x_1, size_y_1) = words_1.get_size()
        (size_x_2, size_y_2) = words_2.get_size()
        (size_x_3, size_y_3) = words_3.get_size()
        pos_x_1 = (Const.WINDOW_SIZE[0] - size_x_1) / 2
        pos_y_1 = (Const.WINDOW_SIZE[1] - size_y_1 - 450) / 2
        pos_x_2 = (Const.WINDOW_SIZE[0] - size_x_2) / 2
        pos_y_2 = (Const.WINDOW_SIZE[1] - size_y_2) / 2
        pos_x_3 = (Const.WINDOW_SIZE[0] - size_x_3) / 2
        pos_y_3 = (Const.WINDOW_SIZE[1] - size_y_3 + 50) / 2
        screen.blit(words_1, (pos_x_1, pos_y_1))
        screen.blit(words_2, (pos_x_2, pos_y_2))
        screen.blit(words_3, (pos_x_3, pos_y_3))


class View_stop(__Object_base):
    @classmethod
    def init_convert(cls):
        # cls.menu = cls.menu.convert()
        # cls.base = cls.base.convert_alpha()
        pass

    def draw(self, screen):
        font = pg.font.Font(os.path.join(Const.FONT_PATH, 'Noto', 'NotoSansCJK-Black.ttc'), 36)
        text_surface = font.render("Press [space] to continue ...", 1, pg.Color('gray88'))
        text_center = (Const.WINDOW_SIZE[0] / 2, Const.WINDOW_SIZE[1] / 2)
        screen.blit(text_surface, text_surface.get_rect(center = text_center))


class View_endgame(__Object_base):
    @classmethod
    def init_convert(cls):
        # cls.menu = cls.menu.convert()
        # cls.base = cls.base.convert_alpha()
        pass

    def draw(self, screen):
        # draw background
        screen.fill(Const.BACKGROUND_COLOR)
        # draw text
        font = pg.font.Font(os.path.join(Const.FONT_PATH, 'Noto', 'NotoSansCJK-Black.ttc'), 36)
        text_surface = font.render("Press [space] to restart ...", 1, pg.Color('gray88'))
        text_center = (Const.WINDOW_SIZE[0] / 2, Const.WINDOW_SIZE[1] / 2)
        screen.blit(text_surface, text_surface.get_rect(center = text_center))


class View_characters(__Object_base):
    # images = tuple(
    #     view_utils.scaled_surface(
    #         pg.image.load(os.path.join(Const.IMAGE_PATH, f'move_{_index}.png')),
    #         0.6
    #     )
    #     for _index in map(str, range(1, 8))
    # )
    # image_oil = view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'oil_black.png')),0.4)

    @classmethod
    def init_convert(cls):
        # cls.images = tuple( _image.convert_alpha() for _image in cls.images )
        # cls.image_oil = pg.Surface.convert_alpha( cls.image_oil )
        pass

    def __init__(self, model):
        # self.model = model
        # self.picture_switch = (0, 1, 2, 1, 2, 1, 2, 1, 2, 3, 4, 5, 4, 5, 4, 5, 4, 5, 6)
        # self.position_switch = (130, 240, 350, 460, 570, 680, 790, 900, 1010,
        #                         1010, 900, 790, 680, 570, 460, 350, 240, 130, 120)
        # self.index = 0
        # self.counter = 0
        pass

    def draw(self, screen):
        # image = self.images[self.picture_switch[self.index]]
        # screen.blit(image, [self.position_switch[self.index], 520])
        # if self.index < 10:
        #     screen.blit(self.image_oil, (1220, 700))
        # if self.counter == 20:
        #     self.index += 1
        #     self.index %= 19
        # self.counter %= 20
        # self.counter += 1
        pass


class View_players(__Object_base):
    @classmethod
    def init_convert(cls):
        pass

    def __init__(self, model):
        self.model = model
    def set_theworld_player(self, player_index):
        pass

    def draw(self, screen):
        # draw players
        for player in self.model.players:
            if player.invincible_time > 0:
                pass
            center = list(map(int, player.position))
            pg.draw.circle(screen, Const.PLAYER_COLOR[player.player_id], center, player.player_radius)
            # temp voltage monitor
            font = pg.font.Font(None, 20)
            voltage_surface = font.render(f"V = {player.voltage:.0f}", 1, pg.Color('white'))
            voltage_pos = player.position
            screen.blit(voltage_surface, voltage_surface.get_rect(center = voltage_pos))
        pass


class View_entities(__Object_base):
    @classmethod
    def init_convert(cls):
        pass
    def __init__(self, model):
        self.model = model
    def set_theworld_player(self, player_index):
        pass
    def draw(self, screen):
        # draw players
        for entity in self.model.entities:
            center = list(map(int, entity.position))
            pg.draw.circle(screen, Const.ITEM_COLOR[2], center, 10)
        pass

class View_scoreboard(__Object_base):
    images = {
        'Heart'       :view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'heart.png')), 0.03125)
    }

    @classmethod
    def init_convert(cls):
        cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }
        cls.namefont = pg.font.Font(os.path.join(Const.FONT_PATH, 'Noto', 'NotoSansCJK-Black.ttc'), 18)
        cls.numfont = pg.font.Font(os.path.join(Const.FONT_PATH, 'Noto', 'NotoSansCJK-Black.ttc'), 25)

    def draw(self, screen):
        fontsize = 24
        posX = (Const.WINDOW_SIZE[0] * 7 / 8)
        posY = (Const.WINDOW_SIZE[1] * 1 / 32)
        heart_image = self.images['Heart']
        for player_id in range(1, 5):
            heartposX = posX + 43
            heartposY = posY + (fontsize + 14)
            position = posX, posY
            voltage = round(self.model.players[player_id - 1].voltage, 2)
            item = self.model.players[player_id - 1].keep_item_id
            text = [f"Player {player_id}", "Life:", f"Voltage: {voltage}", f"Item: {item}", "Score:"]
            label = []

            for line in text:
                label.append(self.namefont.render(line, True, pg.Color('white')))
            for line in range(len(label)):
                screen.blit(label[line], (position[0], position[1] + (line * (fontsize + 10))))
            for i in range(3):
                screen.blit(heart_image, (heartposX, heartposY))
                heartposX += 20
            posY += (len(label) - 1) * (fontsize + 15) + (fontsize + 20)


class View_items(__Object_base):
    images = {
        1: view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'item_bananaGun.png')), 0.1),
        2: view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'item_blackHole.png')), 0.2),
        3: view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'item_bomber.png')), 0.1),
        4: view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'item_lightning.png')), 0.2),
        5: view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'item_bananaPeel.png')), 0.15),
        6: view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'heart.png')), 0.05),
        7: view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'item_battery.png')), 0.02)
    }

    @classmethod
    def init_convert(cls):
        cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }

    def draw(self, screen):
        # for market in self.model.priced_market_list:
        #     if market.item:
        #         screen.blit(self.images[market.item.name], self.images[market.item.name].get_rect(center=(401, 398)))
        for item in self.model.items:
            screen.blit(self.images[item.item_id], self.images[item.item_id].get_rect(center=item.position))
            #pg.draw.circle(screen, Const.ITEM_COLOR[item.item_id], center, item.item_radius)
            #font = pg.font.Font(None, 15)
            #item_surface = font.render(f"{item.item_id:d}", 1, pg.Color('black'))
            #item_pos = item.position
            #screen.blit(item_surface, item_surface.get_rect(center = item_pos))


class View_timer(__Object_base):
    images = {
        'Heart' : view_utils.scaled_surface(pg.image.load(os.path.join(Const.IMAGE_PATH, 'heart.png')), 0.2)
    }

    @classmethod
    def init_convert(cls):
        #cls.images = { _name: cls.images[_name].convert_alpha() for _name in cls.images }
        pass

    def draw(self, screen):
        # for market in self.model.priced_market_list:
        #     if market.item:
        #         screen.blit(self.images[market.item.name], self.images[market.item.name].get_rect(center=(401, 398)))
        font = pg.font.Font(None, 36)
        timer_surface = font.render(f"time left: {self.model.timer / Const.FPS:.2f}", 1, pg.Color('white'))
        timer_pos = (Const.WINDOW_SIZE[0] * 1 / 10, Const.WINDOW_SIZE[1] * 1 / 10)
        screen.blit(timer_surface, timer_surface.get_rect(center = timer_pos))


def init_staticobjects():
    View_platform.init_convert()
    View_players.init_convert()
    View_items.init_convert()
    View_entities.init_convert()
    View_scoreboard.init_convert()
    View_menu.init_convert()
    View_characters.init_convert()
    View_timer.init_convert()
