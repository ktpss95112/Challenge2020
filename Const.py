import pygame as pg
from Events.EventManager import *
import os.path

# model-game
FPS = 60 # frame per second
GAME_LENGTH = 180 * FPS

# model-player
PLAYER_RADIUS = 25
VALID_KO_TIME = 3 * FPS
PLAYER_LIFE = 5
PLAYER_INIT_VELOCITY = pg.Vector2(0, 0)
PLAYER_INIT_SPEED = 150
PLAYER_FINAL_SPEED = 300
PLAYER_SPEED_PARAMETER = (PLAYER_INIT_SPEED - PLAYER_FINAL_SPEED) / GAME_LENGTH ** 2
PLAYER_JUMP_SPEED = 900
DIRECTION_TO_VEC2 = {
    'left': pg.Vector2(-1, 0),
    'right': pg.Vector2(1, 0),
}
PLAYER_JUMP_QUOTA = 3

ATTACK_RADIUS = 12 * PLAYER_RADIUS
ATTACK_COOL_DOWN_TIME = 1.5 * FPS
VOLTAGE_INCREASE_CONST = 300

# model-stage setting
NO_STAGE = -2
RANDOM_STAGE = -1
RANDOM_STAGE_TIME = 1 * FPS
STAGE_NUMBER = 3
STAGE_1 = 0
STAGE_2 = 1
STAGE_3 = 2

LIFE_BOUNDARY = pg.Rect(-700, -2000, 2200, 3500)

X_OFFSET = 34.5
Y_OFFSET = 31.85
PLATFORM_INIT_POSITION = [
    [ # stage 1
        [pg.Vector2(150 + X_OFFSET, 570 + Y_OFFSET), pg.Vector2(982 + X_OFFSET, 580 + Y_OFFSET)],
        [pg.Vector2(100 + X_OFFSET, 440 + Y_OFFSET), pg.Vector2(400 + X_OFFSET, 450 + Y_OFFSET)],
        [pg.Vector2(350 + X_OFFSET, 270 + Y_OFFSET), pg.Vector2(782 + X_OFFSET, 280 + Y_OFFSET)],
        [pg.Vector2(732 + X_OFFSET, 440 + Y_OFFSET), pg.Vector2(1032 + X_OFFSET, 450 + Y_OFFSET)]
    ],
    [ # stage 2
        [pg.Vector2(0 + X_OFFSET, 100 + Y_OFFSET), pg.Vector2(180 + X_OFFSET, 110 + Y_OFFSET)],
        [pg.Vector2(0 + X_OFFSET, 250 + Y_OFFSET), pg.Vector2(210 + X_OFFSET, 260 + Y_OFFSET)],
        [pg.Vector2(0 + X_OFFSET, 400 + Y_OFFSET), pg.Vector2(300 + X_OFFSET, 410 + Y_OFFSET)],
        [pg.Vector2(0 + X_OFFSET, 570 + Y_OFFSET), pg.Vector2(420 + X_OFFSET, 580 + Y_OFFSET)],
        [pg.Vector2(952 + X_OFFSET, 100 + Y_OFFSET), pg.Vector2(1132 + X_OFFSET, 110 + Y_OFFSET)],
        [pg.Vector2(922 + X_OFFSET, 250 + Y_OFFSET), pg.Vector2(1132 + X_OFFSET, 260 + Y_OFFSET)],
        [pg.Vector2(832 + X_OFFSET, 400 + Y_OFFSET), pg.Vector2(1132 + X_OFFSET, 410 + Y_OFFSET)],
        [pg.Vector2(712 + X_OFFSET, 570 + Y_OFFSET), pg.Vector2(1132 + X_OFFSET, 580 + Y_OFFSET)]
    ],
    [ # stage 3
        [pg.Vector2(0 + X_OFFSET, 532 + Y_OFFSET), pg.Vector2(230 + X_OFFSET, 542 + Y_OFFSET)],
        [pg.Vector2(892 + X_OFFSET, 532 + Y_OFFSET), pg.Vector2(1132 + X_OFFSET, 542 + Y_OFFSET)],
        [pg.Vector2(380 + X_OFFSET, 602 + Y_OFFSET), pg.Vector2(752 + X_OFFSET, 612 + Y_OFFSET)],
        [pg.Vector2(330 + X_OFFSET, 342 + Y_OFFSET), pg.Vector2(802 + X_OFFSET, 352 + Y_OFFSET)],
        [pg.Vector2(0 + X_OFFSET, 232 + Y_OFFSET), pg.Vector2(200 + X_OFFSET, 242 + Y_OFFSET)],
        [pg.Vector2(932 + X_OFFSET, 232 + Y_OFFSET), pg.Vector2(1132 + X_OFFSET, 242 + Y_OFFSET)],

    ],
]
PLAYER_INIT_POSITION = [
    [ # stage 1
        pg.Vector2(150 + X_OFFSET, 545 + Y_OFFSET),
        pg.Vector2(420 + X_OFFSET, 545 + Y_OFFSET),
        pg.Vector2(690 + X_OFFSET, 545 + Y_OFFSET),
        pg.Vector2(982 + X_OFFSET, 545 + Y_OFFSET)
    ],
    [ # stage 2
        pg.Vector2(100 + X_OFFSET, 75 + Y_OFFSET),
        pg.Vector2(100 + X_OFFSET, 545 + Y_OFFSET),
        pg.Vector2(1042 + X_OFFSET, 75 + Y_OFFSET),
        pg.Vector2(1042 + X_OFFSET, 545 + Y_OFFSET)
    ],
    [ # stage 3
        pg.Vector2(100 + X_OFFSET, 507 + Y_OFFSET),
        pg.Vector2(405 + X_OFFSET, 577 + Y_OFFSET),
        pg.Vector2(732 + X_OFFSET, 577 + Y_OFFSET),
        pg.Vector2(1032 + X_OFFSET, 507 + Y_OFFSET)
    ],
]
PLAYER_RESPAWN_POSITION = [
    [ # stage 1
        pg.Vector2(150 + X_OFFSET, 545 + Y_OFFSET),
        pg.Vector2(420 + X_OFFSET, 545 + Y_OFFSET),
        pg.Vector2(690 + X_OFFSET, 545 + Y_OFFSET),
        pg.Vector2(982 + X_OFFSET, 545 + Y_OFFSET)
    ],
    [ # stage 2
        pg.Vector2(100 + X_OFFSET, 75 + Y_OFFSET),
        pg.Vector2(100 + X_OFFSET, 545 + Y_OFFSET),
        pg.Vector2(1042 + X_OFFSET, 75 + Y_OFFSET),
        pg.Vector2(1042 + X_OFFSET, 545 + Y_OFFSET)
    ],
    [ # stage 3
        pg.Vector2(100 + X_OFFSET, 507 + Y_OFFSET),
        pg.Vector2(405 + X_OFFSET, 577 + Y_OFFSET),
        pg.Vector2(732 + X_OFFSET, 577 + Y_OFFSET),
        pg.Vector2(1032 + X_OFFSET, 507 + Y_OFFSET)
    ]
]

# model-physics
GRAVITY_ACCELERATION = 70 * FPS
GRAVITY_ACCELERATION_FOR_ITEM = 40 * FPS
DRAG_CRITICAL_SPEED = 464
DRAG_COEFFICIENT = 0.00005
VERTICAL_DRAG_EMERGE_SPEED = -1500
ATTENUATION_COEFFICIENT = 0.5
VERTICAL_SPEED_MINIMUM = 500
HORIZONTAL_SPEED_MINIMUM = 100
BE_ATTACKED_ACCELERATION = 1200 * FPS
BE_ATTACKED_MAX_ACCELERATION_DISTANCE = 20

# model-state machine constants
STATE_POP = 0 # for convenience, not really a state which we can be in
STATE_MENU = 1
STATE_PLAY = 2
STATE_STOP = 3
STATE_ENDGAME = 4 # show score board and handle restart

# model-item
ITEM_SPECIES = 7
NO_ITEM = 0
BANANA_PISTOL = 1
BIG_BLACK_HOLE = 2
CANCER_BOMB = 3
ZAP_ZAP_ZAP = 4
BANANA_PEEL = 5
RAINBOW_GROUNDER = 6
INVINCIBLE_BATTERY = 7

ZAP_ZAP_ZAP_RANGE = 5 * PLAYER_RADIUS
ZAP_ZAP_ZAP_SELF_VOLTAGE_UP = 10
ZAP_ZAP_ZAP_OTHERS_VOLTAGE_UP = 50
ZAP_ZAP_ZAP_VERTICAL_ACCELERATION = 800
ZAP_ZAP_ZAP_HORIZONTAL_ACCELERATION = 1000
RAINBOW_GROUNDER_VOLTAGE_DOWN = 10
INVINCIBLE_BATTERY_PLAYER_RADIUS = 2 * PLAYER_RADIUS
INVINCIBLE_BATTERY_ATTACK_RADIUS = 2 * ATTACK_RADIUS
INVINCIBLE_BATTERY_TIME = 5 * FPS
RESPAWN_INVINCIBLE_TIME = 2 * FPS

ITEMS_INIT_AMOUNT = 6
ITEMS_FINAL_AMOUNT = 10
ITEMS_AMOUNT_PARAMETER = (ITEMS_INIT_AMOUNT - ITEMS_FINAL_AMOUNT) / GAME_LENGTH ** 2
ITEM_RADIUS = [7, 7, 7, 7, 7, 7, 7]
ITEM_DRAG = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
ITEM_INIT_HEIGHT = 10
'''
if item is enabled, then its probability is (its item_probability / sum of item_probability of all enabled items)
if item is disabled, then its probability is 0
'''
ITEM_ENABLED = {
    BANANA_PISTOL: 1,
    BIG_BLACK_HOLE: 1,
    CANCER_BOMB: 1,
    ZAP_ZAP_ZAP: 1,
    BANANA_PEEL: 1,
    RAINBOW_GROUNDER: 1,
    INVINCIBLE_BATTERY: 1,
}
ITEM_PROBABILITY = {
    BANANA_PISTOL: 0.2,
    BIG_BLACK_HOLE: 0.05,
    CANCER_BOMB: 0.2,
    ZAP_ZAP_ZAP: 0.05,
    BANANA_PEEL: 0.2,
    RAINBOW_GROUNDER: 0.2,
    INVINCIBLE_BATTERY: 0.1,
}
GENERATE_ITEM_PROBABILITY = 0.015

# model-entities
BULLET_TIME = 5 * FPS
BULLET_VELOCITY = 30 * FPS
BULLET_RADIUS = 5

BANANA_PEEL_TIME = 15 * FPS
BANANA_PEEL_RADIUS = 8
BANANA_PEEL_AFFECT_TIME = 1 * FPS

BOMB_TIME = 3 * FPS
BOMB_EXPLODE_RADIUS = 16 * PLAYER_RADIUS
BOMB_ATK = 50
BOMB_MINIMUM_DISTANCE = 30
BOMB_SCREEN_VIBRATION_RADIUS = 15
BOMB_SCREEN_VIBRATION_DURATION = 15

BLACK_HOLE_TIME = 5 * FPS
BLACK_HOLE_RADIUS = 10
BLACK_HOLE_EFFECT_RADIUS = 10 * PLAYER_RADIUS
BLACK_HOLE_FLOATING_VELOCITY = 5
BLACK_HOLE_GRAVITY_ACCELERATION = 500 * FPS

# view
WINDOW_CAPTION = 'Challenge 2020'
WINDOW_SIZE = (1200, 800)
ARENA_SIZE = (800, 800)
BACKGROUND_COLOR = pg.Color(0x23, 0x23, 0x23)
PLAYER_COLOR = [pg.Color('green'), pg.Color('magenta'), pg.Color('orange'), pg.Color('red')]
PLAYER_PIC = ['player1_0.png', 'player1_1.png', 'player1_2.png', 'player1_3.png', 'player1_4.png',
              'player2_0.png', 'player2_2.png', 'player2_4.png', 'player2_1.png', 'player2_3.png',
              'player3_3.png', 'player3_1.png', 'player3_2.png', 'player3_4.png', 'player3_0.png',
              'player4_1.png', 'player4_4.png', 'player4_3.png', 'player4_0.png', 'player4_2.png',
              'player1_0.png', 'player1_1.png', 'player1_2.png', 'player1_3.png', 'player1_4.png',
              'player2_0.png', 'player2_2.png', 'player2_4.png', 'player2_1.png', 'player2_3.png',
              'player3_3.png', 'player3_1.png', 'player3_2.png', 'player3_4.png', 'player3_0.png',
              'player4_1.png', 'player4_4.png', 'player4_3.png', 'player4_0.png', 'player4_2.png',
             ]
ATTACK_ERROR = 2.8
ITEM_COLOR = [pg.Color('white'), pg.Color('yellow'), pg.Color('deepskyblue'), pg.Color('gray'), pg.Color('mediumpurple'), pg.Color('darkgreen'), pg.Color('tan'), pg.Color('olivedrab')]
FLOATING_RADIUS = 4
FLOATING_THETA = 0.06

# controller
PLAYER_MOVE_KEYS = {
    pg.K_LEFT: (3, 'left'),
    pg.K_RIGHT: (3, 'right'),
    pg.K_j: (2, 'left'),
    pg.K_l: (2, 'right'),
    pg.K_f: (1, 'left'),
    pg.K_h: (1, 'right'),
    pg.K_a: (0, 'left'),
    pg.K_d: (0, 'right'),
}

GAME_STOP_KEY = pg.K_SPACE
GAME_CONTINUE_KEY = pg.K_SPACE
GAME_RESTART_KEY = pg.K_SPACE
GAME_FULLSCREEN_KEY = pg.K_F11

menu_keys = {
    pg.K_1: lambda self : self.ev_manager.post(EventPickArena(STAGE_1)),
    pg.K_2: lambda self : self.ev_manager.post(EventPickArena(STAGE_2)),
    pg.K_3: lambda self : self.ev_manager.post(EventPickArena(STAGE_3)),
    pg.K_r: lambda self : self.ev_manager.post(EventPickArena(RANDOM_STAGE)),
}

handle_keys = {
    pg.K_UP: lambda self, model : self.ev_manager.post(EventPlayerJump(3)),
    pg.K_i: lambda self, model : self.ev_manager.post(EventPlayerJump(2)),
    pg.K_t: lambda self, model : self.ev_manager.post(EventPlayerJump(1)),
    pg.K_w: lambda self, model : self.ev_manager.post(EventPlayerJump(0)),
    pg.K_DOWN: lambda self, model : self.ev_manager.post(EventPlayerAttack(3)) if self.model.players[3].can_attack() else None,
    pg.K_k: lambda self, model : self.ev_manager.post(EventPlayerAttack(2)) if self.model.players[2].can_attack() else None,
    pg.K_g: lambda self, model : self.ev_manager.post(EventPlayerAttack(1)) if self.model.players[1].can_attack() else None,
    pg.K_s: lambda self, model : self.ev_manager.post(EventPlayerAttack(0)) if self.model.players[0].can_attack() else None,
    pg.K_RSHIFT: lambda self, model : self.ev_manager.post(EventPlayerItem(3)),
    pg.K_u: lambda self, model : self.ev_manager.post(EventPlayerItem(2)),
    pg.K_r: lambda self, model : self.ev_manager.post(EventPlayerItem(1)),
    pg.K_q: lambda self, model : self.ev_manager.post(EventPlayerItem(0))
}

# Path
IMAGE_PATH = os.path.join('View', 'img')
SOUND_PATH = os.path.join('View', 'sound')
VIDEO_PATH = os.path.join('View', 'video')
FONT_PATH = os.path.join('View', 'fonts')

# Enhancement
ATTACK_RADIUS_ENHANCEMENT_INDEX = 0
SPEED_ENHANCEMENT_INDEX = 1
JUMP_ENHANCEMENT_INDEX = 2

ATTACK_RADIUS_ENHANCEMENT = 0.01
SPEED_ENHANCEMENT = 0.01
JUMP_ENHANCEMENT = 0.01
