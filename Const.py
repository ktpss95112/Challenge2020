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
PLAYER_NORMAL_SPEED = 150
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
STAGE_RANDOM = -1
STAGE_NUMBER = 2
STAGE_0 = 0
STAGE_1 = 1

LIFE_BOUNDARY = pg.Rect(-700, -2000, 2200, 3500)
PLATFORM_INIT_POSITION = [
    [ # stage 0
        [pg.Vector2(100, 700), pg.Vector2(700, 710)],
        [pg.Vector2(100, 550), pg.Vector2(300, 560)],
        [pg.Vector2(300, 450), pg.Vector2(500, 460)],
        [pg.Vector2(500, 550), pg.Vector2(700, 560)]
    ],
    [ # stage 1
        [pg.Vector2(0, 150), pg.Vector2(100, 160)],
        [pg.Vector2(0, 350), pg.Vector2(130, 360)],
        [pg.Vector2(0, 550), pg.Vector2(190, 560)],
        [pg.Vector2(0, 750), pg.Vector2(280, 760)],
        [pg.Vector2(700, 150), pg.Vector2(800, 160)],
        [pg.Vector2(670, 350), pg.Vector2(800, 360)],
        [pg.Vector2(610, 550), pg.Vector2(800, 560)],
        [pg.Vector2(520, 750), pg.Vector2(800, 760)]
    ]
]
PLAYER_INIT_POSITION = [
    [ # stage 0
        pg.Vector2(100, 650),
        pg.Vector2(300, 650),
        pg.Vector2(500, 650),
        pg.Vector2(700, 650)
    ],
    [ # stage 1
        pg.Vector2(100, 300),
        pg.Vector2(100, 700),
        pg.Vector2(700, 300),
        pg.Vector2(700, 700)
    ]
]
PLAYER_RESPAWN_POSITION = [
    [ # stage 0
        pg.Vector2(100, 650),
        pg.Vector2(300, 650),
        pg.Vector2(500, 650),
        pg.Vector2(700, 650)
    ],
    [ # stage 1
        pg.Vector2(100, 300),
        pg.Vector2(100, 700),
        pg.Vector2(700, 300),
        pg.Vector2(700, 700)
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

ITEMS_MAX_AMOUNT = 6
ITEM_RADIUS = [7, 7, 7, 7, 7, 7, 7]
ITEM_DRAG = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
ITEM_INIT_HEIGHT = 10
ITEM_PROBABILITY = [0.2, 0.05, 0.2, 0.05, 0.2, 0.2, 0.1] # make sure sum = 1

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

BLACK_HOLE_TIME = 5 * FPS
BLACK_HOLE_RADIUS = 10
BLACK_HOLE_EFFECT_RADIUS = 10 * PLAYER_RADIUS
BLACK_HOLE_FLOATING_VELOCITY = 5
BLACK_HOLE_GRAVITY_ACCELERATION = 500 * FPS

# view
WINDOW_CAPTION = 'Challenge 2020'
WINDOW_SIZE = (1200, 800)
ARENA_SIZE = (800, 800)
BACKGROUND_COLOR = pg.Color('black')
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

handle_keys = {
    pg.K_UP: lambda self : self.ev_manager.post(EventPlayerJump(3)),
    pg.K_i: lambda self : self.ev_manager.post(EventPlayerJump(2)),
    pg.K_t: lambda self : self.ev_manager.post(EventPlayerJump(1)),
    pg.K_w: lambda self : self.ev_manager.post(EventPlayerJump(0)),
    pg.K_DOWN: lambda self : self.ev_manager.post(EventPlayerAttack(3)),
    pg.K_k: lambda self : self.ev_manager.post(EventPlayerAttack(2)),
    pg.K_g: lambda self : self.ev_manager.post(EventPlayerAttack(1)),
    pg.K_s: lambda self : self.ev_manager.post(EventPlayerAttack(0)),
    pg.K_RSHIFT: lambda self : self.ev_manager.post(EventPlayerItem(3)),
    pg.K_u: lambda self : self.ev_manager.post(EventPlayerItem(2)),
    pg.K_r: lambda self : self.ev_manager.post(EventPlayerItem(1)),
    pg.K_q: lambda self : self.ev_manager.post(EventPlayerItem(0))
}

# Path
IMAGE_PATH = os.path.join('View', 'img')
SOUND_PATH = os.path.join('View', 'sound')
VIDEO_PATH = os.path.join('View', 'video')
FONT_PATH = os.path.join('View', 'fonts')
