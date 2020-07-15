import pygame as pg
import os.path
from Events.EventManager import *
from Model.Model import GameEngine
from Model.GameObject.entity import CancerBomb , PistolBullet, BananaPeel, BigBlackHole, DeathRain
from View import SOUND_ENABLE
import Const


if SOUND_ENABLE:
    class Audio(object):

        pg.mixer.init()
        pg.mixer.music.load(os.path.join(Const.SOUND_PATH, 'Funky-Chiptune.wav'))

        cutin_sound_list = []

        effect_list = {
            'attack': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'shoot.wav')),
            'bomb_explode': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'bomb_explode.wav')),
            'bomb_beep': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'bomb_beep.wav')),
            'bomb_beeps': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'bomb_beeps.wav')),
            'blackhole': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'blackhole.wav')),
            'electric_shock': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'electric_shock.wav')),
            'pick_item': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'pickup_item.wav')),
            'menu_nevigate': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'menu_nevigate.wav')),
            'jump': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'jump.wav')),
            'gun_shot': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'Gun_Shot.wav')),
            'banana_peel_slip': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'banana_peel_slip.wav')),
            'banana_peel': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'Banana_peel.wav')),
            'rainbow': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'rainbow.wav')),
            'Invincible': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'Invincibe.wav')),
            'Cutin_keyboard_typing': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'keyboard_typing_slow.wav'))
        }

        def __init__(self, ev_manager: EventManager, model: GameEngine):
            self.ev_manager = ev_manager
            self.model = model
            ev_manager.register_listener(self)
            self.effect_list['bomb_beep'].set_volume(0.3)
            self.effect_list['bomb_beeps'].set_volume(0.3)
            self.effect_list['banana_peel_slip'].set_volume(0.4)

        def notify(self, event):
            '''
            Called by EventManager when a event occurs.
            '''
            if isinstance(event, EventInitialize):
                pg.mixer.music.play()

            elif isinstance(event, EventEveryTick):
                cur_state = self.model.state_machine.peek()
                if cur_state == Const.STATE_PLAY:
                    for sound in self.cutin_sound_list:
                        self.effect_list[sound].play()
                        self.cutin_sound_list.remove(sound)
                    for entity in self.model.entities:
                        if isinstance(entity, CancerBomb):
                            if entity.timer == 60:
                                self.effect_list['bomb_beeps'].play()
                            elif entity.timer > 60 and (entity.timer % 18) == 0:
                                self.effect_list['bomb_beep'].play()

            elif isinstance(event, EventPlayerAttack):
                self.effect_list['attack'].play()

            elif isinstance(event, EventPlayerJump):
                self.effect_list['jump'].play()

            elif isinstance(event, EventPlayerPickItem):
                self.effect_list['pick_item'].play()

            elif not Const.HAS_CUT_IN[Const.ZAP_ZAP_ZAP] and isinstance(event, EventUseZapZapZap):
                self.effect_list['electric_shock'].play()

            elif not Const.HAS_CUT_IN[Const.RAINBOW_GROUNDER] and isinstance(event, EventUseRainbowGrounder):
                self.effect_list['rainbow'].play()

            elif not Const.HAS_CUT_IN[Const.BIG_BLACK_HOLE] and isinstance(event, EventUseBigBlackHole):
                self.effect_list['blackhole'].play()

            elif not Const.HAS_CUT_IN[Const.BANANA_PEEL] and isinstance(event, EventUseBananaPeel):
                self.effect_list['banana_peel'].play()

            elif isinstance(event, EventSlipOnBananaPeelSound):
                self.effect_list['banana_peel_slip'].play()

            elif not Const.HAS_CUT_IN[Const.INVINCIBLE_BATTERY] and isinstance(event, EventUseInvincibleBattery):
                self.effect_list['Invincible'].play()

            elif not Const.HAS_CUT_IN[Const.CANCER_BOMB] and isinstance(event, EventUseCancerBomb):
                pass

            elif isinstance(event, EventBombExplode):
                self.effect_list['bomb_explode'].play()

            elif not Const.HAS_CUT_IN[Const.BANANA_PISTOL] and isinstance(event, EventUseBananaPistol):
                self.effect_list['gun_shot'].play()

            elif isinstance(event, EventCutInStart):
                #self.effect_list['Cutin_keyboard_typing'].play()
                if event.item_id == Const.BIG_BLACK_HOLE:
                    self.cutin_sound_list.append('blackhole')
                elif event.item_id == Const.ZAP_ZAP_ZAP:
                    self.cutin_sound_list.append('electric_shock')

            elif isinstance(event, EventTextType):
                self.effect_list['Cutin_keyboard_typing'].play()

            elif isinstance(event, EventContinue):
                pg.mixer.music.unpause()

            elif isinstance(event, EventStop):
                pg.mixer.music.pause()


else:
    class Audio(object):
        def __init__(self, ev_manager):
            pass
