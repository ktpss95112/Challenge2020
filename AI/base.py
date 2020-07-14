"""        
base class of TeamAI.      
"""

class BaseAI(object):
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0, 0]
    
    def decide(self):
        pass