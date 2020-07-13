import pygame as pg
import os.path
from Events.EventManager import *
from Model.Model import GameEngine
import Const

class audio(object):
    pg.init()
    pg.mixer.music.load(os.path.join(Const.SOUND_PATH, 'Funky-Chiptune.wav'))
    effect_list = {
        'attack': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'shoot.wav')),
        'bomb_explode': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'bomb_explode.wav')),
        'blackhole': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'blackhole.wav')),
        'electric_shock': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'electric_shock.wav')),
        'pick_item': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'pickup_item.wav')),
        'menu_nevigate': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'menu_nevigate.wav')),
        'jump': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'jump.wav')),
        'gun_shot': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'Gun_Shot.wav')),
        'banana_peel': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'Banana_peel.wav')),
        'rainbow': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'rainbow.wav')),
        'Invincible': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'Invincibe.wav'))
    }
    def __init__(self, ev_manager: EventManager, model: GameEngine):
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
