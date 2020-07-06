from API.base import BaseAI

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_ATTACK      = 3
AI_DIR_USE_ITEM    = 4

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
    def decide(self):
        my_pos = self.helper.get_self_position()
        my_radius = self.helper.get_self_radius()
        other_pos = self.helper.get_other_position(self.helper.get_nearest_player())
        if self.helper.get_self_keep_item_id() > 0:
            return AI_DIR_USE_ITEM

        if my_pos[0] < 300:
            return AI_DIR_RIGHT
        elif my_pos[0] > 500:
            return AI_DIR_LEFT 

        if other_pos[0] > my_pos[0] and abs(other_pos[0] - my_pos[0]) > 3.5 * my_radius:
            return AI_DIR_RIGHT
        elif other_pos[0] < my_pos[0] and abs(other_pos[0] - my_pos[0]) > 3.5 * my_radius:
            return AI_DIR_LEFT
        elif abs(other_pos[1] - my_pos[1]) > 3.5 * my_radius or other_pos[1] - my_pos[1] == 0:
            return AI_DIR_JUMP
        else:
            return AI_DIR_ATTACK
        
