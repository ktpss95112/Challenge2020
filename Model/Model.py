import random

import pygame as pg

from Events.EventManager import *
from Model.GameObject.player import Player
from Model.GameObject.item import Item
from Model.GameObject.platform import Platform
import Const


class StateMachine(object):
    '''
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.
    '''
    def __init__(self):
        self.statestack = []

    def peek(self):
        '''
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        '''
        try:
            return self.statestack[-1]
        except IndexError:
            # empty stack
            return None

    def pop(self):
        '''
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        '''
        try:
            return self.statestack.pop()
        except IndexError:
            # empty stack
            return None

    def push(self, state):
        '''
        Push a new state onto the stack.
        Returns the pushed value.
        '''
        self.statestack.append(state)
        return state

    def clear(self):
        '''
        Clear the stack.
        '''
        self.statestack = []


class GameEngine:
    '''
    The main game engine. The main loop of the game is in GameEngine.run()
    '''

    def __init__(self, ev_manager: EventManager):
        '''
        This function is called when the GameEngine is created.
        For more specific objects related to a game instance
            , they should be initialized in GameEngine.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.state_machine = StateMachine()

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        self.clock = pg.time.Clock()
        self.state_machine.push(Const.STATE_MENU)
        self.players = [Player(0), Player(1), Player(2), Player(3)]
        self.items = []
        self.platforms = [ Platform(position[0], position[1]) for position in Const.PLATFORM_INIT_POSITION ]

    def notify(self, event: BaseEvent):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            cur_state = self.state_machine.peek()
            if cur_state == Const.STATE_MENU:
                self.update_menu()
            elif cur_state == Const.STATE_PLAY:
                self.update_players()
                self.update_objects()

                self.timer -= 1
                if self.timer == 0:
                    self.ev_manager.post(EventTimesUp())
            elif cur_state == Const.STATE_ENDGAME:
                self.update_endgame()

        elif isinstance(event, EventStateChange):
            if event.state == Const.STATE_POP:
                if self.state_machine.pop() is None:
                    self.ev_manager.post(EventQuit())
            else:
                self.state_machine.push(event.state)

        elif isinstance(event, EventQuit):
            self.running = False

        elif isinstance(event, EventPlayerMove):
            self.players[event.player_id].move_horizontal(event.direction)

        elif isinstance(event, EventPlayerJump):
            self.players[event.player_id].jump()

        elif isinstance(event, EventTimesUp):
            self.state_machine.push(Const.STATE_ENDGAME)

        elif isinstance(event, EventPlayerAttack):
            keys = pg.key.get_pressed()
            for k,v in Const.PLAYER_ATTACK_KEYS.items():
                if keys[k]:
                    for i in range(4):
                        magnitude = ((self.players[i].position.x - self.players[v].position.x)**2 +(self.players[i].position.y - self.players[v].position.y)**2)**0.5
                        if i != v and magnitude < 3 * Const.PLAYER_RADIUS:
                            unitx = (self.players[i].position.x - self.players[v].position.x) / magnitude
                            unity = (self.players[i].position.y - self.players[v].position.y) / magnitude
                            self.players[i].be_attacked(unitx , unity)
                            print(i)
                            
            pass
        
        elif isinstance(event, EventPlayerRespawn):
            pass

        elif isinstance(event, EventPlayerDied):
            pass
        
        elif isinstance(event, EventPlayerItem):
            pass

        elif isinstance(event, EventPlayerPickItem):
            pass

        elif isinstance(event, EventPlayerUseItem):
            pass


    def update_menu(self):
        '''
        Update the objects in welcome scene.
        For example: game title, hint text
        '''
        pass

    def update_players(self):
        '''
        Update information of users
        For example: position, remaining time of item used
        '''
        for player in self.players:
            player.move_every_tick(self.platforms)

    def update_objects(self):
        '''
        Update the objects not controlled by user.
        For example: obstacles, items, special effects, platform
        '''
        self.generate_item()

    def update_endgame(self):
        '''
        Update the objects in endgame scene.
        For example: scoreboard
        '''
        pass
    def generate_item(self):
        # In every tick,if item is less than ITEMS_MAX_AMOUNT,it MAY generate one item
        if len(self.items) < Const.ITEMS_MAX_AMOUNT and  random.randint(1,1000) > 990 : 
            the_platform = random.choice( self.platforms )
            platform_len = the_platform.bottom_right.x - the_platform.upper_left.x 
            new_item = random.randint(1,7) # assume there are 7 types of item

            pos = ( random.uniform( 0 , platform_len ) , Const.ITEM_RADIUS[new_item-1] ) + the_platform.upper_left

            self.items.append( Item( new_item , pos , Const.ITEM_RADIUS[new_item-1] ) )

    def run(self):
        '''
        The main loop of the game is in this function.
        This function activates the GameEngine.
        '''
        self.running = True
        self.ev_manager.post(EventInitialize())
        self.timer = Const.GAME_LENGTH
        while self.running:
            self.ev_manager.post(EventEveryTick())
            self.clock.tick(Const.FPS)


""" Events that model.py should handle. 

EventInitialize{
    initiate all players;
    respawn all players;   
    initiate timer
}   
EventStateChange{
    pass
}
EventEveryTick{

}
EventTimesUp{
    maintain item spawn time
    maintain player respawn time
    maintain [layer last-being-attacked-time-elapsed;
}
EventPlayerMove
EventPlayerAttack
EventPlayerRespawn
EventPlayerDied
EventPlayerPickItem
EventPlayerUseItem

"""

"""
class player's varible

player-id; (1-indexed):int
last-being-attacked-by:int
last-being-attacked-time-elapsed:int
respawn-time-elapsed:int 
is-invincible; (is true when respawn-time-elapsed < t):int
KO time:int
has-item:int
be KOed time:int
voltage:int
position:vec2
velosity; (there is no acceleration variable because acceleration is instant)
:vec2
"""

""" 
class item's varible
item-id (0-indexed)
postition
"""

"""
class platform
upper-left
bottom-right
"""
