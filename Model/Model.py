import random

import pygame as pg
import math

from Events.EventManager import *
from Model.GameObject.player import Player
from Model.GameObject.item import Item
from Model.GameObject.entity import *
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
        self.entities = []
        self.platforms = [ Platform(position[0], position[1]) for position in Const.PLATFORM_INIT_POSITION ]
        self.timer = Const.GAME_LENGTH

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
                # check alive player
                cnt = 0
                for player in self.players:
                    if player.is_alive():
                        cnt += 1
                if cnt <= 1:
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
            if self.players[event.player_id].is_alive() and self.players[event.player_id].can_not_control_time <= 0 :
                self.players[event.player_id].add_horizontal_velocity(event.direction)
                if(event.direction == 'left'):
                    self.players[event.player_id].direction = pg.Vector2(-1,0)
                elif (event.direction == 'right'):
                    self.players[event.player_id].direction = pg.Vector2(1,0)

        elif isinstance(event, EventPlayerJump):
            if self.players[event.player_id].is_alive():
                self.players[event.player_id].jump()

        elif isinstance(event, EventTimesUp):
            self.state_machine.push(Const.STATE_ENDGAME)

        elif isinstance(event, EventPlayerAttack):
            v = event.player_id
            if not self.players[v].is_alive():
                return
            for i in range(4):
                magnitude = (self.players[i].position - self.players[v].position).magnitude()
                if i != v and magnitude < Const.ATTACK_RADIUS_MULTIPLE_CONSTANT * Const.PLAYER_RADIUS and self.players[i].is_alive():
                    unit = (self.players[i].position - self.players[v].position).normalize()
                    self.players[i].be_attacked(unit, magnitude)
                    # record
                    self.players[i].last_being_attacked_by = v
                    self.players[i].last_being_attacked_time_elapsed = self.timer
                            
        elif isinstance(event, EventPlayerRespawn):
            self.players[event.player_id].respawn()

        elif isinstance(event, EventPlayerDied):
            # update KO amount
            die_id = event.player_id
            if not self.players[die_id].is_alive():
                return
            atk_id = self.players[die_id].last_being_attacked_by
            t = self.players[die_id].last_being_attacked_time_elapsed
            if atk_id != -1 and t - self.timer < Const.VALID_KO_TIME:
                self.players[die_id].be_KO_amount += 1
                self.players[atk_id].KO_amount += 1
                
            self.players[die_id].keep_item_id = Const.NO_ITEM
            self.players[die_id].life -= 1
            if self.players[die_id].life > 0:
                self.ev_manager.post(EventPlayerRespawn(die_id))
        
        elif isinstance(event, EventPlayerItem):
            player = self.players[event.player_id]
            if not player.is_alive():
                return
            if player.keep_item_id > 0:
                self.players[event.player_id].use_item(self.players, self.entities)
                self.ev_manager.post(EventPlayerUseItem(player, player.keep_item_id))
            else:
                for item in self.items:
                    distance = (item.position - player.position).magnitude()
                    if distance <= item.item_radius + player.player_radius:
                        self.players[event.player_id].keep_item_id = item.item_id
                        self.items.remove(item)
                        self.ev_manager.post(EventPlayerPickItem(player, item.item_id))

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
        self.players_collision_detect()
        for player in self.players:
            player.can_not_control_time -= 1/Const.FPS
            player.move_every_tick(self.platforms)
            if not Const.LIFE_BOUNDARY.collidepoint(player.position):
                self.ev_manager.post(EventPlayerDied(player.player_id))
        highest_KO_amount = 0
        for player in self.players:
            if player.KO_amount > highest_KO_amount:
                highest_KO_amount = player.KO_amount
        for player in self.players:
            player.score = player.KO_amount * 30 - player.be_KO_amount * 15
            if player.be_KO_amount == 0:
                player.score += 100
            if player.KO_amount == highest_KO_amount:
                player.score += 50

        
    def update_objects(self):
        '''
        Update the objects not controlled by user.
        For example: obstacles, items, special effects, platform
        '''
        self.generate_item()
       
        for item in self.items:
            item.move_every_tick(self.platforms)
            if not Const.LIFE_BOUNDARY.collidepoint(item.position):
                self.items.remove(item)

        for entity in self.entities:
            if entity.update_every_tick(self.players, self.platforms) == False :
                self.entities.remove(entity)
           
    def update_endgame(self):
        '''
        Update the objects in endgame scene.
        For example: scoreboard
        '''
        pass
            
    def players_collision_detect(self):
        # More reliable
        origin_fps = -2
        player1, player2, collision_fps = self.first_collision(origin_fps)
        while collision_fps <= 1:
            if player2 == -1:
                self.players[player1].bounce_reliable(collision_fps)
            else:
                self.players[player1].collision_reliable(self.players[player2], collision_fps)
            origin_fps = collision_fps
            player1, player2, collision_fps = self.first_collision(origin_fps)

        # Less reliable
        '''
        for i in range(len(self.players)):
            for j in range(i + 1, len(self.players)):
                if self.players[i].is_alive() and self.players[j].is_alive():
                    self.players[i].collision(self.players[j], self.platforms)
        '''

    def first_collision(self, origin_fps):
        # Find first collision after origin_fps
        p1 = 0
        p2 = 0
        min_collision_time = 2
        for i in range(len(self.players)):
            if not self.players[i].is_alive():
                continue
            # Collision: ball <=> ball
            for j in range(i + 1, len(self.players)):
                if not self.players[j].is_alive():
                    continue
                distance = self.players[i].position - self.players[j].position
                rel_velocity = self.players[j].velocity - self.players[i].velocity
                if distance.dot(rel_velocity) <= 0:
                    continue
                normal_vector = pg.Vector2(-rel_velocity.y, rel_velocity.x)
                min_distance = (normal_vector.dot(self.players[i].position) - normal_vector.dot(self.players[j].position)) / normal_vector.magnitude()
                collision_distance = self.players[i].player_radius + self.players[j].player_radius
                if abs(min_distance) >= abs(collision_distance):
                    continue
                collision_time = (math.sqrt(distance * distance - min_distance * min_distance) - math.sqrt(collision_distance * collision_distance - min_distance * min_distance)) / (rel_velocity / Const.FPS).magnitude()
                if origin_fps < collision_time <= min_collision_time:
                    min_collision_time = collision_time
                    p1, p2 = i, j
            # Collision: ball <=> platform
            for j in self.platforms:
                distance = j.upper_left.y - self.players[i].position.y - self.players[i].player_radius
                if self.players[i].velocity.y > 0:
                    if j.upper_left.x <= self.players[i].position.x + (self.players[i].velocity.x / self.players[i].velocity.y) * distance <= j.bottom_right.x:
                        collision_time = distance / (self.players[i].velocity.y / Const.FPS)
                        if origin_fps <= collision_time <= min_collision_time:
                            min_collision_time = collision_time
                            p1, p2 = i, -1

        return p1, p2, min_collision_time

    def generate_item(self):
        # In every tick, if item is less than ITEMS_MAX_AMOUNT, it MAY generate one item
        if len(self.items) < Const.ITEMS_MAX_AMOUNT and  random.randint(1, 1000) > 985 : 
            new_item = random.randint(1, Const.ITEM_MAX_SPECIFIES)
            find_position = False
            while not find_position:
                find_position = True
                pos = pg.Vector2(random.randint(50, Const.ARENA_SIZE[0]), random.randint(0, 600))
                for item in self.items:
                    if abs(item.position.x - pos.x) < Const.PLAYER_RADIUS * 2 + Const.ITEM_RADIUS[new_item - 1] + item.item_radius:
                        find_position = False
            self.items.append(Item(new_item, pos, Const.ITEM_RADIUS[new_item-1], Const.ITEM_DRAG[new_item - 1]))
            
    def run(self):
        '''
        The main loop of the game is in this function.
        This function activates the GameEngine.
        '''
        self.running = True
        self.ev_manager.post(EventInitialize())
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
velocity; (there is no acceleration variable because acceleration is instant)
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
        

