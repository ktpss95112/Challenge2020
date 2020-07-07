
from API.base import BaseAI

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_LEFT_JUMP   = 3
AI_DIR_RIGHT_JUMP  = 4
AI_DIR_ATTACK      = 5
AI_DIR_USE_ITEM    = 6

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
    def decide(self):
        
        my_pos = self.helper.get_self_position()
        my_radius = self.helper.get_self_radius()
        other_pos = self.helper.get_other_position(self.helper.get_nearest_player())
        if self.helper.get_other_is_invincible(self.helper.get_nearest_player()):
            other_pos = self.helper.get_other_position(self.helper.get_highest_score_player())
            
        if self.helper.get_self_keep_item_id() > 0:
            return AI_DIR_USE_ITEM

        pp = self.helper.get_platform_position()
        temp = pp[self.helper.get_above_which_land(other_pos)]
        ul = temp[0]
        br = temp[1]
        if (ul[0] + br[0]) / 2 - my_pos[0] > 0 and (ul[1] + br[1]) / 2 - my_pos[1] > 0:
            return AI_DIR_RIGHT_JUMP
        elif (ul[0] + br[0]) / 2 - my_pos[0] < 0 and (ul[1] + br[1]) / 2 - my_pos[1] > 0:
            return AI_DIR_LEFT_JUMP
        
        if other_pos[0] > my_pos[0] and abs(other_pos[0] - my_pos[0]) > 3.5 * my_radius:
            return AI_DIR_RIGHT
        elif other_pos[0] < my_pos[0] and abs(other_pos[0] - my_pos[0]) > 3.5 * my_radius:
            return AI_DIR_LEFT
        elif abs(other_pos[1] - my_pos[1]) > 3.5 * my_radius or other_pos[1] - my_pos[1] == 0:
            return AI_DIR_JUMP
        else:
            return AI_DIR_ATTACK
