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
        radius = self.helper.get_self_radius()
        return self.helper.walk_to_position(self.helper.get_other_position(3))
        '''
        if my_pos[0] > 500:
            return AI_DIR_LEFT
        elif my_pos[0] < 300:
            return AI_DIR_RIGHT
        else:
            return AI_DIR_JUMP 
        '''
