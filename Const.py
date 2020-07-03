import pygame as pg
import os.path

# model-game
FPS = 60 # frame per second
GAME_LENGTH = 300 * FPS

# model-player
PLAYER_RADIUS = 20
VALID_KO_TIME = 3 * FPS
PLAYER_LIFE = 5
PLAYER_INIT_POSITION = [
    pg.Vector2(100, 700),
    pg.Vector2(300, 700),
    pg.Vector2(500, 700),
    pg.Vector2(700, 700)
]
PLAYER_INIT_VELOCITY = pg.Vector2(0, 0)
PLAYER_NORMAL_SPEED = 150
PLAYER_JUMP_SPEED = 1200
DIRECTION_TO_VEC2 = {
    'left': pg.Vector2(-1, 0),
    'right': pg.Vector2(1, 0),
}
PLAYER_JUMP_QUOTA = 3
PLAYER_RESPAWN_POSITION = [
    pg.Vector2(600, 200),
    pg.Vector2(600, 200),
    pg.Vector2(600, 200),
    pg.Vector2(600, 200)
]
ATTACK_RADIUS = 3.5 * PLAYER_RADIUS
VOLTAGE_INCREASE_CONST = 300

# model-platform and boundary
PLATFORM_INIT_POSITION = [
    [pg.Vector2(100, 730), pg.Vector2(700, 740)],
    [pg.Vector2(100, 500), pg.Vector2(400, 510)]
]
LIFE_BOUNDARY = pg.Rect(-700, -2000, 2200, 3500)

# model-physics
GRAVITY_ACCELERATION = 70 * FPS
GRAVITY_ACCELERATION_FOR_ITEM = 40 * FPS
DRAG_CRITICAL_SPEED = 464
DRAG_COEFFICIENT = 0.00005
VERTICAL_DRAG_EMERGE_SPEED = -1500
ATTENUATION_COEFFICIENT = 0.5
VERTICAL_SPEED_MINIMUM = 500
HORIZONTAL_SPEED_MINIMUM = 20
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

ITEMS_MAX_AMOUNT = 6
ITEM_RADIUS = [7, 7, 7, 7, 7, 7, 7]
ITEM_DRAG = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
ITEM_INIT_HEIGHT = 10
ITEM_PROBABILITY = [0.2, 0.05, 0.2, 0.05, 0.2, 0.2, 0.1]

# model-entities
BULLET_TIME = 5 * FPS
BULLET_VELOCITY = 30 * FPS
BULLET_RADIUS = 5

BANANA_PEEL_TIME = 15 * FPS
BANANA_PEEL_RADIUS = 8
BANANA_PEEL_AFFECT_TIME = 1

BOMB_TIME = 3 * FPS
BOMB_EXPLODE_RADIUS = 50
BOMB_ATK = 50

BLACK_HOLE_TIME = 5 * FPS
BLACK_HOLE_RADIUS = 10
BLACK_HOLE_EFFECT_RADIUS = 2 * PLAYER_RADIUS
BLACK_HOLE_FLOATING_VELOCITY = 5
BLACK_HOLE_GRAVITY_ACCELERATION = 500 * FPS

ZAP_ZAP_ZAP_RANGE = 5

# view
WINDOW_CAPTION = 'Challenge 2020'
WINDOW_SIZE = (1200, 800)
ARENA_SIZE = (800, 800)
BACKGROUND_COLOR = pg.Color('black')
PLAYER_COLOR = [pg.Color('green'), pg.Color('magenta'), pg.Color('orange'), pg.Color('red')]
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
PLAYER_JUMP_KEYS = {
    pg.K_UP: 3,
    pg.K_i: 2,
    pg.K_t: 1,
    pg.K_w: 0
}
PLAYER_ITEM_KEYS = {
    pg.K_RSHIFT: 3,
    pg.K_u: 2,
    pg.K_r: 1,
    pg.K_q: 0
}
PLAYER_ATTACK_KEYS = {
    pg.K_DOWN: 3,
    pg.K_k: 2,
    pg.K_g: 1,
    pg.K_s: 0
}
GAME_STOP_KEY = pg.K_SPACE
GAME_CONTINUE_KEY = pg.K_SPACE
GAME_RESTART_KEY = pg.K_SPACE
GAME_FULLSCREEN_KEY = pg.K_F11

# Path
IMAGE_PATH = os.path.join('View', 'img')
SOUND_PATH = os.path.join('View', 'sound')
VIDEO_PATH = os.path.join('View', 'video')
FONT_PATH = os.path.join('View', 'fonts')
