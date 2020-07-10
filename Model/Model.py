import pygame as pg
import numpy as np
import random
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
    __slots__ = ('statestack',)

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


class GameEngine(object):
    '''
    The main game engine. The main loop of the game is in GameEngine.run()
    '''
    __slots__ = ('ev_manager', 'state_machine', 'AI_names',\
                'clock', 'timer', 'item_amount', 'random_stage_timer', 'stage', 'players',\
                'platforms', 'platforms', 'items', 'entities',\
                'running')

    def __init__(self, ev_manager: EventManager, AI_names: list):
        '''
        This function is called when the GameEngine is created.
        For more specific objects related to a game instance
            , they should be initialized in GameEngine.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.state_machine = StateMachine()
        self.AI_names = AI_names
        while len(self.AI_names) < 4:
            self.AI_names.append("m")
        check_probability()

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        self.clock = pg.time.Clock()
        self.timer = Const.GAME_LENGTH
        self.item_amount = Const.ITEMS_INIT_AMOUNT
        self.init_players()
        # menu
        self.random_stage_timer = 0
        self.stage = Const.NO_STAGE
        # stop
        self.stop_screen_timer = 1.5 * Const.FPS # set to 2 seconds
        self.stop_screen_index = 0
        self.state_machine.push(Const.STATE_MENU)

    def init_players(self):
        self.players = [ Player(i, 'manual', False) if name == 'm' else Player(i, name, True) for name, i in zip(self.AI_names, range(4)) ]

    def init_stage(self):
        for player in self.players:
            player.set_position(Const.PLAYER_INIT_POSITION[self.stage][player.player_id])
        self.platforms = [Platform(position[0], position[1]) for position in Const.PLATFORM_INIT_POSITION[self.stage]]
        self.items = []
        self.entities = []

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
                self.update_variable()
                self.timer -= 1
                # check if game ends
                cnt = sum(player.is_alive() for player in self.players)
                if self.timer == 0 or cnt <= 1:
                    self.ev_manager.post(EventTimesUp())
            elif cur_state == Const.STATE_STOP:
                self.update_stop()
            elif cur_state == Const.STATE_ENDGAME:
                self.update_endgame()

        elif isinstance(event, EventPlay):
            self.init_stage()
            self.state_machine.push(Const.STATE_PLAY)

        elif isinstance(event, EventStop):
            self.stop_screen_timer = 1.5 * Const.FPS
            self.stop_screen_index = 0
            self.state_machine.push(Const.STATE_STOP)

        elif isinstance(event, EventContinue):
            if self.state_machine.peek() == Const.STATE_STOP:
                self.state_machine.pop()

        elif isinstance(event, EventTimesUp):
            scores = []
            for player in self.players:
                scores.append(player.score)
            sorted_score = sorted(scores)
            sorted_score.reverse()
            for player in self.players:
                for i in range(len(sorted_score)):
                    if player.score == sorted_score[i]:
                        player.rank = i + 1
                        break
                
            self.state_machine.push(Const.STATE_ENDGAME)

        elif isinstance(event, EventRestart):
            self.state_machine.clear()
            self.initialize()

        elif isinstance(event, EventQuit):
            self.running = False

        elif isinstance(event, EventPlayerMove):
            player = self.players[event.player_id]
            if player.is_alive() and player.is_controllable() :
                player.add_horizontal_velocity(event.direction)

        elif isinstance(event, EventPlayerJump):
            if self.players[event.player_id].is_alive():
                self.players[event.player_id].jump()

        elif isinstance(event, EventPlayerAttack):
            attacker = self.players[event.player_id]
            if attacker.is_alive() and attacker.can_attack():
                attacker.attack(self.players, self.timer)

        elif isinstance(event, EventPlayerRespawn):
            self.players[event.player_id].respawn(Const.PLAYER_RESPAWN_POSITION[self.stage][event.player_id])

        elif isinstance(event, EventPlayerDied):
            self.players[event.player_id].die(self.players, self.timer)
            if self.players[event.player_id].is_alive():
                self.ev_manager.post(EventPlayerRespawn(event.player_id))

        elif isinstance(event, EventPlayerItem):
            player = self.players[event.player_id]
            if player.is_alive() and player.has_item():
                item_id = self.players[event.player_id].keep_item_id
                entities = self.players[event.player_id].use_item(self.players, self.timer)
                peel_position, bullet_position, black_hole_position, bomb_position = None, None, None, None
                for entity in entities:
                    if isinstance(entity, PistolBullet):
                        bullet_position = entity.position
                    elif isinstance(entity, BigBlackHole):
                        black_hole_position = entity.position
                    elif isinstance(entity, CancerBomb):
                        bomb_position = entity.position
                    elif isinstance(entity, BananaPeel):
                        peel_position = entity.position
                    self.entities.append(entity)
                if item_id == Const.BANANA_PISTOL:
                    self.ev_manager.post(EventUseBananaPistol(peel_position, bullet_position, self.timer))
                elif item_id == Const.BIG_BLACK_HOLE:
                    self.ev_manager.post(EventUseBigBlackHole(black_hole_position, self.timer))
                elif item_id == Const.CANCER_BOMB:
                    self.ev_manager.post(EventUseCancerBomb(bomb_position, self.timer))
                elif item_id == Const.ZAP_ZAP_ZAP:
                    self.ev_manager.post(EventUseZapZapZap(player.position, self.timer))
                elif item_id == Const.BANANA_PEEL:
                    self.ev_manager.post(EventUseBananaPeel(peel_position, self.timer))
                elif item_id == Const.RAINBOW_GROUNDER:
                    self.ev_manager.post(EventUseRainbowGrounder(player.position, self.timer))
                elif item_id == Const.INVINCIBLE_BATTERY:
                    self.ev_manager.post(EventUseInvincibleBattery(player.position, self.timer))

        elif isinstance(event, EventPickArena):
            if self.stage == event.stage:
                self.stage = Const.NO_STAGE
            elif event.stage != Const.RANDOM_STAGE:
                self.stage = event.stage
            else:
                self.random_stage_timer = Const.RANDOM_STAGE_TIME
                self.stage = random.randrange(Const.STAGE_NUMBER)
                
    def item_amount_function(self, time):
        return Const.ITEMS_AMOUNT_PARAMETER * time ** 2 + Const.ITEMS_FINAL_AMOUNT

    def update_menu(self):
        '''
        Update stage
        '''
        if self.random_stage_timer > 0:
            self.random_stage_timer -= 1
            if self.random_stage_timer > 1.5 * Const.FPS:
                if self.random_stage_timer % 2 == 0:
                    self.stage = (self.stage + 1) % Const.STAGE_NUMBER
            elif self.random_stage_timer > 1 * Const.FPS:
                if self.random_stage_timer % 4 == 0:
                    self.stage = (self.stage + 1) % Const.STAGE_NUMBER
            else:
                if self.random_stage_timer % 8 == 0:
                    self.stage = (self.stage + 1) % Const.STAGE_NUMBER

    def update_variable(self):
        self.item_amount = self.item_amount_function(self.timer)

    def update_players(self):
        '''
        Update information of users
        For example: position, remaining time of item used and score
        '''
        self.overlap_detect()
        self.players_collision_detect()
        highest_KO_amount = max(player.KO_amount for player in self.players)
        for player in self.players:
            if player.is_alive():
                # maintain position, velocity and timer
                player.update_every_tick(self.platforms, self.timer)

                # maintain items
                if not player.has_item():
                    item = player.find_item_every_tick(self.items) # item is ref to an item in self.items
                    if not item is None:
                        player.pick_item(item.item_id)
                        self.ev_manager.post(EventPlayerPickItem(player.player_id, item.item_id))
                        self.items.remove(item)
                        
                # maintain scores
                player.maintain_score_every_tick(highest_KO_amount)

                # maintain lifes
                if not Const.LIFE_BOUNDARY.collidepoint(player.position):
                    self.ev_manager.post(EventPlayerDied(player.player_id))

    def update_objects(self):
        '''
        Update the objects not controlled by user.
        For example: obstacles, items, special effects, platform
        '''
        self.generate_item()

        for item in self.items:
            item.update_every_tick(self.platforms)
            if not Const.LIFE_BOUNDARY.collidepoint(item.position):
                self.items.remove(item)

        for entity in self.entities:
            if entity.update_every_tick(self.players, self.items, self.platforms, self.timer) == False :
                # tell view to draw explosion animation
                if isinstance(entity, CancerBomb):
                    self.ev_manager.post(EventBombExplode(entity.position))
                self.entities.remove(entity)

    def update_stop(self):
        if self.stop_screen_timer == 0:
            self.stop_screen_index = (self.stop_screen_index + 1) % 3
            self.stop_screen_timer = 1.5 * Const.FPS
        else:
            self.stop_screen_timer -= 1

    def update_endgame(self):
        '''
        Update the objects in endgame scene.
        For example: scoreboard
        '''
        pass

    def overlap_detect(self):
        '''
        Bad implemetation of detecting overlap.
        Only use when players_collision_detect(self) doesn't work
        '''
        overlap = True
        count = 0
        while overlap:
            overlap = False
            count += 1
            for i in self.players:
                if not i.is_alive():
                    continue
                for j in self.players:
                    if not j.is_alive():
                        continue
                    if i.player_id < j.player_id and i.overlap_resolved(j):
                        overlap = True
            if count == 4:
                break

    def players_collision_detect(self):
        origin_fps = -2
        player1, player2, collision_fps = self.first_collision(origin_fps)
        while collision_fps <= 1:
            if player2 == -1:
                self.players[player1].bounce_reliable(collision_fps)
            else:
                self.players[player1].collision_reliable(self.players[player2], collision_fps)
            origin_fps = collision_fps
            player1, player2, collision_fps = self.first_collision(origin_fps)

    def first_collision(self, origin_fps):
        # Find first collision after origin_fps
        p1, p2 = 0, 0
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
                if collision_time < 0 and distance.magnitude() > collision_distance:
                    continue
                if origin_fps < collision_time <= min_collision_time:
                    min_collision_time = collision_time
                    p1, p2 = i, j

            # Collision: ball <=> platform
            for j in self.platforms:
                distance = j.upper_left.y - self.players[i].position.y - self.players[i].player_radius
                if self.players[i].velocity.y > 0:
                    if j.upper_left.x <= self.players[i].position.x + (self.players[i].velocity.x / self.players[i].velocity.y) * distance <= j.bottom_right.x:
                        collision_time = distance / (self.players[i].velocity.y / Const.FPS)
                        if collision_time < 0 and abs(distance) > j.bottom_right.y - j.upper_left.y:
                            continue
                        if origin_fps <= collision_time <= min_collision_time:
                            min_collision_time = collision_time
                            p1, p2 = i, -1

        return p1, p2, min_collision_time

    def generate_item(self):
        # In every tick, if item is less than item_amount, it MAY generate one item
        if len(self.items) < int(self.item_amount) and random.random() < Const.GENERATE_ITEM_PROBABILITY:
            enabled_items, p = [], []
            for item_id in Const.ITEM_ENABLED.keys():
                if Const.ITEM_ENABLED[item_id]:
                    enabled_items.append(item_id)
                    p.append(Const.ITEM_PROBABILITY[item_id])
            p = np.array(p)
            new_item = np.random.choice(enabled_items, p = p / np.sum(p))
            find_position = False
            while not find_position:
                find_position = True
                pos = pg.Vector2(random.randint(50, Const.ARENA_SIZE[0]), random.randint(0, 600))
                for item in self.items:
                    if abs(item.position.x - pos.x) < Const.PLAYER_RADIUS * 2 + Const.ITEM_RADIUS[new_item - 1] + item.item_radius:
                        find_position = False
            self.items.append(Item(new_item, pos, Const.ITEM_RADIUS[new_item - 1], Const.ITEM_DRAG[new_item - 1]))

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

def check_probability():
    if abs(sum(Const.ITEM_PROBABILITY.values()) - 1) > 1e-5:
        print('Warning: Sum of Const.ITEM_PROBABILITY does not equal to 1')


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


