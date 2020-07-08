import Const

class Platform(object):
    __slots__ = ('upper_left', 'bottom_right')
    
    def __init__(self, upper_left, bottom_right):
        self.upper_left = upper_left
        self.bottom_right = bottom_right