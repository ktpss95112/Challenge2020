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
        self.position = Const.PLAYER_INIT_POSITION[player_id] # is a pg.Vector2 (Const.PLAYER_INIT_POSITION is not update now!)
        self.speed = Const.SPEED_ATTACK if player_id == 1 else Const.SPEED_DEFENSE

    def move_direction(self, direction: str):
        '''
        Move the player along the direction by its speed.
        Will automatically clip the position so no need to worry out-of-bound moving.
        '''
        self.position += self.speed / Const.FPS * Const.DIRECTION_TO_VEC2[direction]

        # clipping
        self.position.x = max(0, min(Const.ARENA_SIZE[0], self.position.x))
        self.position.y = max(0, min(Const.ARENA_SIZE[1], self.position.y))
