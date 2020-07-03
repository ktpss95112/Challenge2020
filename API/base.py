"""
const of AI code use.
"""

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_ATTACK      = 3
AI_DIR_PICK_ITEM   = 4
AI_DIR_USE_ITEM    = 5

"""
a base of AI.
"""
class BaseAI:
    def __init__( self , helper ):
        self.helper = helper

    def decide(self):
        pass
