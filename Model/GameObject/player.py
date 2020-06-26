import pygame as pg
import Const

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.last_being_attacked_by = -1
        self.last_being_attacked_time_elapsed = 0
        self.invincible_time = 0
        self.KO_amount = 0
        self.be_KO_amount = 0
        self.voltage = 0
        self.keep_item_id = -1
        self.position = pg.Vector2(Const.PLAYER_INIT_POSITION[player_id]) # is a pg.Vector2 (Const.PLAYER_INIT_POSITION is not update now!)
        self.velocity = pg.Vector2(Const.PLAYER_INIT_VELOCITY) # current velocity of user
        self.normal_speed = Const.PLAYER_NORMAL_SPEED # speed gain when players try to move left and right
        self.jump_speed =  Const.PLAYER_JUMP_SPEED # speed gain when players try to jump
        self.jump_quota = Const.PLAYER_JUMP_QUOTA

    def move_every_tick(self, platforms: list):
        # Move the player
        prev_position = pg.Vector2(self.position)
        self.position += self.velocity / Const.FPS

        # Modify the horizontal velocity
        if self.velocity.x > 0:
            self.velocity.x -= Const.HORIZONTAL_ACCELERATION / Const.FPS
            self.velocity.x = self.velocity.x if self.velocity.x > 0 else 0
        elif self.velocity.x < 0:
            self.velocity.x += Const.HORIZONTAL_ACCELERATION / Const.FPS
            self.velocity.x = self.velocity.x if self.velocity.x < 0 else 0

        # Modify the vertical velocity
        self.velocity.y += Const.GRAVITY_ACCELERATION / Const.FPS

        # Make sure that the player do not pass through the platform
        for platform in platforms:
            if platform.upper_left.x <= self.position.x <= platform.bottom_right.x:
                if prev_position.y <= platform.upper_left.y - Const.PLAYER_RADIUS <= self.position.y:
                    self.position.y = platform.upper_left.y - Const.PLAYER_RADIUS
                    self.velocity.y = 0
                    self.jump_quota = Const.PLAYER_JUMP_QUOTA
                    break

    def move_horizontal(self, direction: str):
        '''
        Add horizontal velocity to the player along the direction.
        '''
        self.velocity += self.normal_speed * Const.DIRECTION_TO_VEC2[direction]

    def jump(self):
        '''
        Add vertical velocity to the player.
        '''
        if self.jump_quota != 0:
            self.velocity = self.jump_speed * pg.Vector2(0, -1)
            self.jump_quota -= 1
    def be_attacked(self , unit):
        self.velocity += Const.BE_ATTACKED_ACCELERATION * unit/ Const.FPS
        self.position += self.velocity / Const.FPS
