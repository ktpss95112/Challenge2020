from API.base import BaseAI

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_ATTACK      = 3
AI_DIR_PICK_ITEM   = 4
AI_DIR_USE_ITEM    = 5

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
    def decide(self):
        my_pos = self.helper.get_self_position()
        radius = self.helper.get_self_radius()
        other_pos = self.helper.get_other_position(self.helper.get_nearest_player())
        if other_pos[0] > my_pos[0] and abs(other_pos[0] - my_pos[0]) > self.helper.attack_radius:
            return AI_DIR_RIGHT
        elif other_pos[0] < my_pos[0] and abs(other_pos[0] - my_pos[0]) > self.helper.attack_radius:
            return AI_DIR_LEFT
        elif abs(other_pos[1] - my_pos[1]) > self.helper.attack_radius:
            return AI_DIR_JUMP
        else:
            return AI_DIR_ATTACK
        
