import pygame as pg

# model
FPS = 60 # frame per second
GAME_LENGTH = 300 * FPS
PLAYER_INIT_POSITION = [
    pg.Vector2(100, 700),
    pg.Vector2(300, 700),
    pg.Vector2(500, 700),
    pg.Vector2(700, 700)
]
PLAYER_RADIUS = 20
PLAYER_INIT_VELOCITY = pg.Vector2(0, 0)
PLAYER_NORMAL_SPEED = 150
PLAYER_JUMP_SPEED = 1200
DIRECTION_TO_VEC2 = {
    'left': pg.Vector2(-1, 0),
    'right': pg.Vector2(1, 0),
}
PLATFORM_INIT_POSITION = [
    [pg.Vector2(100, 730), pg.Vector2(700, 740)],
    [pg.Vector2(100, 500), pg.Vector2(400, 510)]
]
PLAYER_JUMP_QUOTA = 3
LIFE_BOUNDARY = pg.Rect(-700, -2000, 2200, 3500)
PLAYER_RESTART_POSITION = [
    pg.Vector2(700, 200),
    pg.Vector2(700, 200),
    pg.Vector2(700, 200),
    pg.Vector2(700, 200)
]
GRAVITY_ACCELERATION = 70 * FPS
DRAG_COEFFICIENT = 0.00005
ATTENUATION_COEFFICIENT = 0.5
VERTICAL_SPEED_MINIMUM = 500
HORIZONTAL_SPEED_MINIMUM = 20
BE_ATTACKED_ACCELERATION = 1200 * FPS * 35
BE_ATTACKED_MAX_ACCELERATION_DISTANCE = 20

# State machine constants
STATE_POP = 0 # for convenience, not really a state which we can be in
STATE_MENU = 1
STATE_PLAY = 2
STATE_STOP = 3
STATE_ENDGAME = 4


# view
WINDOW_CAPTION = 'Challenge 2020'
WINDOW_SIZE = (1200, 800)
ARENA_SIZE = (800, 800)
BACKGROUND_COLOR = pg.Color('black')
PLAYER_COLOR = [pg.Color('green'), pg.Color('magenta'), pg.Color('orange'), pg.Color('red')]

# item
ITEM_SPECIES = 7
NO_ITEM = 0
BANANA_PISTOL = 1
BIG_BLACK_HOLE = 2
CANCER_BOMB = 3
ZAP_ZAP_ZAP = 4
BANANA_PEEL = 5
RAINBOW_GROUNDER = 6
INVINCIBLE_BATTERY = 7

ITEMS_MAX_AMOUNT=6
ITEM_RADIUS=[4, 4, 4, 4, 4, 4, 4]
ITEM_INIT_HEIGHT=10
ITEM_MAX_SPECIFIES=7

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
    pg.K_RCTRL: 3,
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
