from API.base import BaseAI

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_LEFT_JUMP   = 3
AI_DIR_RIGHT_JUMP  = 4
AI_DIR_ATTACK      = 5
AI_DIR_USE_ITEM    = 6
AI_DIR_STAY        = 7

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0]
    
    def decide(self):
        # add your code
