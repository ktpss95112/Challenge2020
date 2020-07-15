import pygame as pg
import os.path
from Events.EventManager import *
from View import SOUND_ENABLE
import Const


if SOUND_ENABLE:
    class Audio(object):

        pg.mixer.init()
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
            'Invincible': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'Invincibe.wav')),
            'Cutin_keyboard_typing': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'keyboard_typing_slow.wav'))
        }

        def __init__(self, ev_manager: EventManager):
            self.ev_manager = ev_manager
            ev_manager.register_listener(self)

        def notify(self, event):
            '''
            Called by EventManager when a event occurs.
            '''
            if isinstance(event, EventInitialize):
                pg.mixer.music.play()

            elif isinstance(event, EventPlayerAttack):
                self.effect_list['attack'].play()

            elif isinstance(event, EventPlayerJump):
                self.effect_list['jump'].play()

            elif isinstance(event, EventPlayerPickItem):
                self.effect_list['pick_item'].play()

            elif isinstance(event, EventUseZapZapZap):
                self.effect_list['electric_shock'].play()

            elif isinstance(event, EventUseRainbowGrounder):
                self.effect_list['rainbow'].play()

            elif isinstance(event, EventUseBigBlackHole):
                self.effect_list['blackhole'].play()

            elif isinstance(event, EventUseBananaPeel):
                self.effect_list['banana_peel'].play()

            elif isinstance(event, EventUseInvincibleBattery):
                self.effect_list['Invincible'].play()

            elif isinstance(event, EventUseCancerBomb):
                self.effect_list['bomb_explode'].play()

            elif isinstance(event, EventUseBananaPistol):
                self.effect_list['gun_shot'].play()

            elif isinstance(event, EventCutInStart):
                self.effect_list['Cutin_keyboard_typing'].play()

            elif isinstance(event, EventContinue):
                pg.mixer.music.unpause()

            elif isinstance(event, EventStop):
                pg.mixer.music.pause()


else:
    class Audio(object):
        def __init__(self, ev_manager):
            pass
