import pygame as pg

import Const

from Model.GameObject.entity import *

'''
AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_LEFT_JUMP   = 3
AI_DIR_RIGHT_JUMP  = 4
AI_DIR_ATTACK      = 5
AI_DIR_USE_ITEM    = 6


JUMP_CONST_DELAY   = 30
'''

'''
When return timers or velocity, please use "second" as time unit.
'''
class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.player_id = index
        self.player_radius = Const.PLAYER_RADIUS
        self.player_normal_speed = Const.PLAYER_NORMAL_SPEED
        self.player_jump_speed = Const.PLAYER_JUMP_SPEED
        self.player_respawn_position = Const.PLAYER_RESPAWN_POSITION
        self.player_gravity_acceleration = Const.GRAVITY_ACCELERATION
        self.attack_radius = Const.ATTACK_RADIUS
        self.be_attacked_acceleration = Const.BE_ATTACKED_ACCELERATION
        self.drag_critical_speed = Const.DRAG_CRITICAL_SPEED
        self.drag_coefficient = Const.DRAG_COEFFICIENT
        self.arena_size = Const.ARENA_SIZE
        self.life_boundary = tuple(Const.LIFE_BOUNDARY)
        self.jump_delay = 0
        
    # get self information
    def get_self_id(self):
        return self.player_id
    
    def get_self_position(self):
        return tuple(self.model.players[self.player_id].position)

    def get_self_velocity(self):
        return tuple(self.model.players[self.player_id].velocity)

    def get_self_direction(self):
        return tuple(self.model.players[self.player_id].direction)

    def get_self_keep_item_id(self):
        return self.model.players[self.player_id].keep_item_id

    def get_self_voltage(self):
        return self.model.players[self.player_id].voltage

    def get_self_radius(self):
        return self.model.players[self.player_id].player_radius

    def get_self_is_invincible(self):
        return (self.model.players[self.player_id].is_invincible())
    
    def get_self_invincible_time(self):
        return self.model.players[self.player_id].invincible_time / Const.FPS

    def get_self_uncontrollable_time(self):
        return self.model.players[self.player_id].uncontrollable_time / Const.FPS
    
    def get_self_life(self):
        return self.model.players[self.player_id].life

    def get_self_score(self):
        return self.model.players[self.player_id].score

    def get_self_jump_quota(self):
        return self.model.players[self.player_id].jump_quota

    def get_self_jump_to_the_highest_time(self):
        return self.model.players[self.player_id].velocity.y / self.player_gravity_acceleration

    def get_self_can_attack_time(self):
        return self.model.players[self.player_id].attack_cool_down_time / Const.FPS

    # get all player information    
    def get_all_position(self):
        return [tuple(player.position) for player in self.model.players]

    def get_all_velocity(self):
        return [tuple(player.velocity) for player in self.model.players]

    def get_all_direction(self):
        return [tuple(player.direction) for player in self.model.players]

    def get_all_keep_item_id(self):
        return [player.keep_item_id for player in self.model.players]

    def get_all_voltage(self):
        return [player.voltage for player in self.model.players]

    def get_all_radius(self):
        return [player.player_radius for player in self.model.players]

    def get_all_is_invincible(self):
        return [player.is_invincible() for player in self.model.players]
    
    def get_all_invincible_time(self):
        return [player.invincible_time / Const.FPS for player in self.model.players]

    def get_all_uncontrollable_time(self):
        return [player.uncontrollable_time / Const.FPS for player in self.model.players]
    
    def get_all_life(self):
        return [player.life for player in self.model.players]

    def get_all_score(self):
        return [player.score for player in self.model.players]

    def get_all_jump_quota(self):
        return [player.jump_quota for player in self.model.players]

    def get_all_jump_to_the_highest_time(self):
        return [player.velocity.y / self.player_gravity_acceleration for player in self.model.players]
    
    def get_all_can_attack_time(self):
        return [player.attack_cool_down_time / Const.FPS for player in self.model.players]
    
    # get other players information
    def get_other_position(self, index):
        return tuple(self.model.players[index].position)

    def get_other_velocity(self, index):
        return tuple(self.model.players[index].velocity)

    def get_other_direction(self, index):
        return tuple(self.model.players[index].direction)

    def get_other_keep_item_id(self, index):
        return self.model.players[index].keep_item_id

    def get_other_voltage(self, index):
        return self.model.players[index].voltage

    def get_other_radius(self, index):
        return self.model.players[index].player_radius

    def get_other_is_invincible(self, index):
        return (self.model.players[index].is_invincible())
    
    def get_other_invincible_time(self, index):
        return self.model.players[index].invincible_time / Const.FPS

    def get_other_uncontrollable_time(self, index):
        return self.model.players[index].uncontrollable_time / Const.FPS
    
    def get_other_life(self, index):
        return self.model.players[index].life

    def get_other_score(self, index):
        return self.model.players[index].score

    def get_other_jump_quota(self, index):
        return self.model.players[index].jump_quota

    def get_other_jump_to_the_highest_time(self, index):
        return self.model.players[index].velocity.y / self.player_gravity_acceleration

    def get_other_can_attack_time(self, index):
        return self.model.players[index].attack_cool_down_time / Const.FPS

    # get item information
    def get_all_item_position(self):
        itemlist = [ [] for i in range(Const.ITEM_SPECIES + 1) ]
        for item in self.model.items:
            itemlist[item.item_id].append(tuple(item.position))
        return itemlist

    # get platform information 
    def get_platform_position(self):
        return [(tuple(platform.upper_left), tuple(platform.bottom_right)) for platform in self.model.platforms]

    # get which map is used
    def get_which_map(self):
        return self.model.stage
    
    # get special information
    def get_nearest_player(self):  # when the nearest_player not only one?
        nearest_id = 0
        minimum_distance = 10000 ** 2 
        for player in self.model.players:
            if player.player_id != self.player_id:
                current_distance = (self.model.players[self.player_id].position - player.position).magnitude() 
                if current_distance < minimum_distance:
                    minimum_distance = current_distance
                    nearest_id = player.player_id
        return nearest_id
    
    def get_highest_voltage_player(self):    # when the highest_voltage_player not only one?
        highest_voltage_id = 0
        highest_voltage = 0
        for player in self.model.players:
            if player.voltage > highest_voltage:
                highest_voltage = player.voltage
                highest_voltage_id = player.player_id
        return highest_voltage_id

    def get_highest_score_player(self):   # when the highest_score_player not only one?
        highest_score_id = 0
        highest_score = 0
        for player in self.model.players:
            if player.score > highest_score:
                highest_score = player.score
                highest_score_id = player.player_id
        return highest_score_id

    def get_distance(self, p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def get_distance_to_closest_land(self):
        minimum_distance = 10000 ** 2
        distance = 0
        for platform in self.model.platforms:
            if self.model.players[self.player_id].position.x > platform.upper_left.x and self.model.players[self.player_id].position.x < platform.bottom_right.x:
                distance =  abs(self.model.players[self.player_id].position.y - platform.upper_left.y)
            else:
                distance = min(self.get_distance(self.model.players[self.player_id].position, platform.upper_left), self.get_distance(self.model.players[self.player_id].position, platform.bottom_right))
            if distance < minimum_distance:
                minimum_distance = distance
        return minimum_distance
    
    def get_position_vector_to_closest_land(self):
        minimum_distance = 10000 ** 2
        distance = 0
        minimum_vector = (10000, 10000)
        vector = (0, 0)
        for platform in self.model.platforms:
            if self.model.players[self.player_id].position.x > platform.upper_left.x and self.model.players[self.player_id].position.x < platform.bottom_right.x:
                distance =  abs(self.model.players[self.player_id].position.y - platform.upper_left.y)
                vector = (0, platform.upper_left.y - self.model.players[self.player_id].position.y)
            else:
                if self.get_distance(self.model.players[self.player_id].position, platform.upper_left) > self.get_distance(self.model.players[self.player_id].position, platform.bottom_right):
                    distance = self.get_distance(self.model.players[self.player_id].position, platform.bottom_right)
                    vector = tuple(platform.bottom_right - self.model.players[self.player_id].position)
                else:
                    distance = self.get_distance(self.model.players[self.player_id].position, platform.upper_left)
                    vector = tuple(platform.upper_left - self.model.players[self.player_id].position)
            if distance < minimum_distance:
                minimum_distance = distance
                minimum_vector = vector
        return minimum_vector
        def get_above_which_land(self, position):
            index = -1
            count = 0
            if self.model.stage == Const.STAGE_0:
                for platform in self.model.platforms:
                    if position[0] > platform.upper_left.x - 15 and position[0] < platform.bottom_right.x + 15 and position[1] < platform.upper_left.y:
                        index = count
                    count+=1
                if position[0] > self.model.platforms[2].upper_left.x - 15 and position[0] < self.model.platforms[2].bottom_right.x + 15 and position[1] < self.model.platforms[2].upper_left.y:
                    index = 2
            if self.model.stage == Const.STAGE_1:
                for platform in self.model.platforms:
                    if position[0] > platform.upper_left.x - 15 and position[0] < platform.bottom_right.x + 15 and position[1] < platform.upper_left.y and index < 0:
                        index = count
                    count+=1
            return index

    
    # get all entity information
    def entity_exists(self):
        return (True if self.model.entites else False)
    
    def get_all_pistol_bullet_position(self):
        return [entity.position for entity in self.model.entities if isinstance(entity, PistolBullet)]
    
    def get_all_pistol_bullet_timer(self):
        return [entity.timer / Const.FPS for entity in self.model.entities if isinstance(entity, PistolBullet)]
    
    def get_all_pistol_bullet_velocity(self):
        return [tuple(entity.velocity) for entity in self.model.entities if isinstance(entity, PistolBullet)]
            
    def get_all_banana_peel_position(self):
        return [entity.position for entity in self.model.entities if isinstance(entity, BananaPeel)]
    
    def get_all_banana_peel_timer(self):
        return [entity.timer / Const.FPS for entity in self.model.entities if isinstance(entity, BananaPeel)]
    
    def get_all_cancer_bomb_position(self):
        return [entity.position for entity in self.model.entities if isinstance(entity, CancerBomb)]

    def get_all_cancer_bomb_timer(self):
        return [entity.timer / Const.FPS for entity in self.model.entities if isinstance(entity, CancerBomb)]
    
    def get_all_big_black_hole_position(self):
        return [entity.position for entity in self.model.entities if isinstance(entity, BigBlackHole)]

    def get_all_big_black_hole_timer(self):
        return [entity.timer / Const.FPS for entity in self.model.entities if isinstance(entity, BigBlackHole)]

    def walk_to_position(self,target_position):
        player_position = tuple(self.model.players[self.player_id].position)
        player_above_which_land = self.get_above_which_land(player_position)
        target_above_which_land = self.get_above_which_land(target_position)
        command = AI_DIR_ATTACK
        if self.model.stage == Const.STAGE_0:
            if player_above_which_land == -1:
                if self.jump_delay == 0:
                    self.jump_delay = JUMP_CONST_DELAY
                    command = AI_DIR_JUMP
                elif player_position[0] > target_position[0]:
                    command = AI_DIR_LEFT
                else:
                    command = AI_DIR_RIGHT   
            elif player_above_which_land == target_above_which_land:
                if abs(player_position[0] - target_position[0]) < 10 and self.jump_delay == 0 and self.model.players[self.player_id].jump_quota > 0 and abs(player_position[1] - target_position[1]) > Const.PLAYER_RADIUS*2:
                    self.jump_delay = JUMP_CONST_DELAY
                    command = AI_DIR_JUMP
                elif player_position[0] < target_position[0]:
                    command = AI_DIR_RIGHT
                elif player_position[0] > target_position[0]:
                    command = AI_DIR_LEFT
            elif target_above_which_land == 0:
                if player_above_which_land == 1:
                    command = AI_DIR_RIGHT
                elif player_above_which_land == 3:
                    command = AI_DIR_LEFT
                elif player_above_which_land == 2:
                    closest_land_vector = self.get_position_vector_to_closest_land()
                    if closest_land_vector[0] >= 0:
                        command = AI_DIR_RIGHT
                    elif closest_land_vector[0] < 0:
                        command = AI_DIR_LEFT
            elif target_above_which_land == 1:
                if player_above_which_land == 0:
                    if abs(player_position[0] - target_position[0]) < 10 and self.jump_delay == 0 and self.model.players[self.player_id].jump_quota > 0:
                        self.jump_delay = JUMP_CONST_DELAY
                        command = AI_DIR_JUMP
                    elif player_position[0] < target_position[0]:
                        command = AI_DIR_RIGHT
                    elif player_position[0] > target_position[0]:
                        command = AI_DIR_LEFT
                elif player_above_which_land == 3:
                    command = AI_DIR_LEFT
                elif player_above_which_land == 2:
                    command = AI_DIR_LEFT
            elif target_above_which_land == 3:
                if player_above_which_land == 0:
                    if abs(player_position[0] - target_position[0]) < 10 and self.jump_delay == 0 and self.model.players[self.player_id].jump_quota > 0:
                        self.jump_delay = JUMP_CONST_DELAY
                        command = AI_DIR_JUMP
                    elif player_position[0] < target_position[0]:
                        command = AI_DIR_RIGHT
                    elif player_position[0] > target_position[0]:
                        command = AI_DIR_LEFT
                elif player_above_which_land == 1:
                    command = AI_DIR_RIGHT
                elif player_above_which_land == 2:
                    command = AI_DIR_RIGHT
            elif target_above_which_land == 2:
                if abs(player_position[0] - target_position[0]) < 10 and self.jump_delay == 0 and self.model.players[self.player_id].jump_quota > 0:
                    self.jump_delay = JUMP_CONST_DELAY
                    command = AI_DIR_JUMP
                elif player_position[0] < target_position[0]:
                    command = AI_DIR_RIGHT
                elif player_position[0] > target_position[0]:
                    command = AI_DIR_LEFT
        elif self.model.stage == Const.STAGE_1:
            if player_above_which_land == -1:
                if self.jump_delay == 0:
                    self.jump_delay = JUMP_CONST_DELAY
                    command = AI_DIR_JUMP
                elif player_position[0] > target_position[0]:
                    command = AI_DIR_LEFT
                else:
                    command = AI_DIR_RIGHT
            elif player_above_which_land == target_above_which_land:
                if abs(player_position[0] - target_position[0]) < 10 and self.jump_delay == 0 and self.model.players[self.player_id].jump_quota > 0 and abs(player_position[1] - target_position[1]) > Const.PLAYER_RADIUS*2:
                    self.jump_delay = JUMP_CONST_DELAY
                    command = AI_DIR_JUMP
                elif player_position[0] < target_position[0]:
                    command = AI_DIR_RIGHT
                elif player_position[0] > target_position[0]:
                    command = AI_DIR_LEFT
            elif player_above_which_land <= 3 and target_above_which_land <= 3:
                if player_above_which_land > target_above_which_land:
                    if abs(player_position[0] - target_position[0]) < 10 and self.jump_delay == 0 and self.model.players[self.player_id].jump_quota > 0 and abs(player_position[1] - target_position[1]) > Const.PLAYER_RADIUS*2:
                        self.jump_delay = JUMP_CONST_DELAY
                        command = AI_DIR_JUMP
                    elif player_position[0] < target_position[0]:
                        command = AI_DIR_RIGHT
                    elif player_position[0] > target_position[0]:
                        command = AI_DIR_LEFT
                else:
                    command = AI_DIR_RIGHT
            elif player_above_which_land >= 4 and target_above_which_land >= 4:
                if player_above_which_land > target_above_which_land:
                    if abs(player_position[0] - target_position[0]) < 10 and self.jump_delay == 0 and self.model.players[self.player_id].jump_quota > 0 and abs(player_position[1] - target_position[1]) > Const.PLAYER_RADIUS*2:
                        self.jump_delay = JUMP_CONST_DELAY
                        command = AI_DIR_JUMP
                    elif player_position[0] < target_position[0]:
                        command = AI_DIR_RIGHT
                    elif player_position[0] > target_position[0]:
                        command = AI_DIR_LEFT
                else:
                    command = AI_DIR_LEFT
            else:
                if abs(player_position[0] - target_position[0]) < 10 and self.jump_delay == 0 and self.model.players[self.player_id].jump_quota > 0 and abs(player_position[1] - target_position[1]) > Const.PLAYER_RADIUS*2:
                        self.jump_delay = JUMP_CONST_DELAY
                        command = AI_DIR_JUMP
                elif player_position[0] < target_position[0]:
                    command = AI_DIR_RIGHT
                elif player_position[0] > target_position[0]:
                    command = AI_DIR_LEFT
        if(self.jump_delay > 0):
            self.jump_delay-=1
        return command
