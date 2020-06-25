import pygame as pg

# model
FPS = 60 # frame per second
GAME_LENGTH = 30 * FPS
PLAYER_INIT_POSITION = [
    pg.Vector2(100, 700),
    pg.Vector2(300, 700),
    pg.Vector2(500, 700),
    pg.Vector2(700, 700)
]
PLAYER_RADIUS = 30
PLAYER_INIT_VELOCITY = pg.Vector2(0, 0)
PLAYER_NORMAL_SPEED = 8000
PLAYER_JUMP_SPEED = 80000
DIRECTION_TO_VEC2 = {
    'up': pg.Vector2(0, -1),
    'left': pg.Vector2(-1, 0),
    'down': pg.Vector2(0, 1),
    'right': pg.Vector2(1, 0),
}
PLATFORM_INIT_POSITION = [
    [pg.Vector2(100, 730), pg.Vector2(700, 740)]
]
PLAYER_JUMP_QUOTA = 3
GRAVITY_ACCELERATION = 60
HORIZONTAL_ACCELERATION = 100

# State machine constants
STATE_POP = 0 # for convenience, not really a state which we can be in
STATE_MENU = 1
STATE_PLAY = 2
STATE_STOP = 3 # not implemented yet
STATE_ENDGAME = 4


# view
WINDOW_CAPTION = 'Challenge 2020'
WINDOW_SIZE = (1200, 800)
ARENA_SIZE = (800, 800)
BACKGROUND_COLOR = pg.Color('black')
PLAYER_COLOR = [pg.Color('green'), pg.Color('magenta'), pg.Color('orange'), pg.Color('red')]

# item
NO_ITEM = 0
BANANA_PISTOL = 1
BIG_BLACK_HOLE = 2
CANCER_BOMB = 3
ZAP_ZAP_ZAP = 4
BANANA_PEEL = 5
RAINBOW_GROUNDER = 6
INVINCIBLE_BATTERY = 7


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