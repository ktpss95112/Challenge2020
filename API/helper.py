import pygame as pg
import Const
from Model.GameObject.entity import *

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_LEFT_JUMP   = 3
AI_DIR_RIGHT_JUMP  = 4
AI_DIR_ATTACK      = 5
AI_DIR_USE_ITEM    = 6
AI_DIR_STAY        = 7

JUMP_CONST_DELAY   = 30


'''
When return timers or velocity, please use "second" as time unit.
'''
class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.player_id = index
        self.jump_delay = 0

    # get game information
    def get_game_left_time(self):
        return (Const.GAME_LENGTH - self.model.timer) / Const.FPS

    def get_game_stage(self):
        return self.model.stage

    def get_game_arena_boundary(self):
        # return top-left and bottom-right coordinate
        return ((0, 0), Const.ARENA_SIZE)

    def get_game_life_boundary(self):
        # return top-left and bottom-right
        return ((Const.LIFE_BOUNDARY[0], Const.LIFE_BOUNDARY[1]), (Const.LIFE_BOUNDARY[2], Const.LIFE_BOUNDARY[3]))

    def get_game_player_gravity_acceleration(self):
        return Const.GRAVITY_ACCELERATION / Const.FPS

    def get_game_item_gravity_acceleration(self):
        return Const.GRAVITY_ACCELERATION_FOR_ITEM / Const.FPS

    # get self information
    def get_self_id(self):
        return self.player_id
    
    def get_self_position(self):
        return tuple(self.model.players[self.player_id].position)

    def get_self_velocity(self):
        return tuple(self.model.players[self.player_id].velocity)

    def get_self_direction(self):
        return tuple(self.model.players[self.player_id].direction)

    def get_self_normal_speed(self):
        return self.model.players[self.player_id].normal_speed

    def get_self_jump_speed(self):
        return self.model.players[self.player_id].jump_speed

    def get_self_keep_item_id(self):
        return self.model.players[self.player_id].keep_item_id

    def get_self_voltage(self):
        return self.model.players[self.player_id].voltage

    def get_self_radius(self):
        return self.model.players[self.player_id].player_radius

    def get_self_attack_radius(self):
        return self.model.players[self.player_id].attack_radius

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

    def get_self_can_jump(self):
        return (self.get_self_jump_quota() > 0)

    def get_self_jump_quota(self):
        return self.model.players[self.player_id].jump_quota

    def get_self_jump_to_the_highest_time(self):
        return self.model.players[self.player_id].velocity.y / Const.GRAVITY_ACCELERATION

    def get_self_can_attack_time(self):
        return self.model.players[self.player_id].attack_cool_down_time / Const.FPS

    def get_self_can_attack(self):
        return self.model.players[self.player_id].can_attack

    def get_self_will_drop(self):
        self_position = self.get_self_position()
        self_radius = self.get_self_radius()
        platforms = self.get_platform_position()
        for platform in platforms:
            if platform[0][0] < self_position[0] < platform[1][0] and self_position[1] + self_radius <= platform[0][1]:
                return False
        return True
    
    # get all player information 
    def get_all_position(self):
        return [tuple(player.position) for player in self.model.players]

    def get_all_velocity(self):
        return [tuple(player.velocity) for player in self.model.players]

    def get_all_direction(self):
        return [tuple(player.direction) for player in self.model.players]

    def get_all_player_distance(self):
        return [self.get_distance(self.get_self_position(), self.get_other_position(i)) for i in range(Const.PLAYER_NUM)]

    def get_all_player_vector(self):
        return [self.get_vector(self.get_self_position(), self.get_other_position(i)) for i in range(Const.PLAYER_NUM)]

    def get_all_keep_item_id(self):
        return [player.keep_item_id for player in self.model.players]

    def get_all_voltage(self):
        return [player.voltage for player in self.model.players]

    def get_all_radius(self):
        return [player.player_radius for player in self.model.players]

    def get_all_attack_radius(self):
        return [player.attack_radius for player in self.model.players]

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
        return [player.velocity.y / Const.GRAVITY_ACCELERATION for player in self.model.players]
    
    def get_all_can_attack_time(self):
        return [player.attack_cool_down_time / Const.FPS for player in self.model.players]
    
    def get_all_can_attack(self):
        return [player.can_attack for player in self.model.players]
    
    # get other players information
    def get_other_position(self, index):
        return tuple(self.model.players[index].position)

    def get_other_velocity(self, index):
        return tuple(self.model.players[index].velocity)

    def get_other_direction(self, index):
        return tuple(self.model.players[index].direction)

    def get_other_vector(self, index):
        return self.get_vector(self.get_self_position(), self.get_other_position(index))

    def get_other_distance(self, index):
        return self.get_distance(self.get_self_position(), self.get_other_position(index))

    def get_other_keep_item_id(self, index):
        return self.model.players[index].keep_item_id

    def get_other_voltage(self, index):
        return self.model.players[index].voltage

    def get_other_radius(self, index):
        return self.model.players[index].player_radius

    def get_other_attack_radius(self, index):
        return self.model.players[index].attack_radius

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
        return self.model.players[index].velocity.y / Const.GRAVITY_ACCELERATION

    def get_other_can_attack_time(self, index):
        return self.model.players[index].attack_cool_down_time / Const.FPS

    def get_other_can_attack(self, index):
        return self.model.players[index].can_attack

    def get_other_will_drop(self, index):
        other_position = self.get_other_position(index)
        other_radius = self.get_other_radius(index)
        platforms = self.get_platform_position()
        for platform in platforms:
            if platform[0][0] < other_position[0] < platform[1][0] and other_position[1] + other_radius <= platform[0][1]:
                return False
        return True

    def get_live_player_num(self):
        lives = self.get_all_life()
        num = Const.PLAYER_NUM
        for life in lives:
            if life == 0:
                num = num - 1
        return num
    
    # get item information
    def item_exists(self):
        return (True if self.model.items else False)

    def get_nearest_item_position(self):
        player_pos = self.get_self_position()
        minimum_distance = 10000
        position = (0, 0)
        for item in self.model.items:
            distance = self.get_distance(player_pos, item.position)
            if distance < minimum_distance:
                minimum_distance = distance
                position = item.position
        return position
    
    def get_all_banana_pistol_position(self):
        return [tuple(item.position) for item in self.model.items if item.item_id == 1]
    
    def get_all_banana_pistol_velocity(self):
        return [tuple(item.velocity) for item in self.model.items if item.item_id == 1]
            
    def get_all_big_black_hole_position(self):
        return [tuple(item.position) for item in self.model.items if item.item_id == 2]
    
    def get_all_big_black_hole_velocity(self):
        return [tuple(item.velocity) for item in self.model.items if item.item_id == 2]
    
    def get_all_cancer_bomb_position(self):
        return [tuple(item.position) for item in self.model.items if item.item_id == 3]

    def get_all_cancer_bomb_velocity(self):
        return [tuple(item.velocity) for item in self.model.items if item.item_id == 3]

    def get_all_zap_zap_zap_position(self):
        return [tuple(item.position) for item in self.model.items if item.item_id == 4]

    def get_all_zap_zap_zap_velocity(self):
        return [tuple(item.velocity) for item in self.model.items if item.item_id == 4]

    def get_all_banana_peel_position(self):
        return [tuple(item.position) for item in self.model.items if item.item_id == 5]

    def get_all_banana_peel_velocity(self):
        return [tuple(item.velocity) for item in self.model.items if item.item_id == 5]

    def get_all_rainbow_grounder_position(self):
        return [tuple(item.position) for item in self.model.items if item.item_id == 6]

    def get_all_rainbow_grounder_velocity(self):
        return [tuple(item.velocity) for item in self.model.items if item.item_id == 6]

    def get_all_invincible_battery_position(self):
        return [tuple(item.position) for item in self.model.items if item.item_id == 7]

    def get_all_invincible_battery_velocity(self):
        return [tuple(item.velocity) for item in self.model.items if item.item_id == 7]
                
    def get_all_item_position(self):
        return [tuple(item.position) for item in self.model.items]
    
    # get platform information 
    def get_platform_position(self):
        return [(tuple(platform.upper_left), tuple(platform.bottom_right)) for platform in self.model.platforms]
    
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
            if player.player_id != self.player_id:
                if player.voltage > highest_voltage:
                    highest_voltage = player.voltage
                    highest_voltage_id = player.player_id
        return highest_voltage_id

    def get_highest_score_player(self):   # when the highest_score_player not only one?
        highest_score_id = 0
        highest_score = 0
        for player in self.model.players:
            if player.player_id != self.player_id:
                if player.score > highest_score:
                    highest_score = player.score
                    highest_score_id = player.player_id
        return highest_score_id

    def get_distance(self, p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def get_vector(self, p1, p2):
        # get vector from p1 to p2
        return ((p2[0] - p1[0]), (p2[1] - p1[1])) 

    def get_position_will_drop(self, pos):
        # Doesn't consider radius
        platforms = self.get_platform_position()
        for platform in platforms:
            if platform[0][0] < pos[0] < platform[1][0] and pos[1] <= platform[0][1]:
                return False
        return True

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
        if self.model.stage == Const.STAGE_1:
            for platform in self.model.platforms:
                if position[0] > platform.upper_left.x - 20 and position[0] < platform.bottom_right.x + 20 and position[1] <= platform.upper_left.y:
                    index = count
                count+=1
            if position[0] > self.model.platforms[2].upper_left.x - 20 and position[0] < self.model.platforms[2].bottom_right.x + 20 and position[1] < self.model.platforms[2].upper_left.y:
                index = 2
        elif self.model.stage == Const.STAGE_2:
            for platform in self.model.platforms:
                if position[0] > platform.upper_left.x - 20 and position[0] < platform.bottom_right.x + 20 and position[1] <= platform.upper_left.y and index < 0:
                    index = count
                count+=1
        elif self.model.stage == Const.STAGE_3:
            temp = [2,0,1,3,4,5]
            for i in range(0,6):
                if position[0] > self.model.platforms[temp[i]].upper_left.x - 20 and position[0] < self.model.platforms[temp[i]].bottom_right.x + 20 and position[1] <= self.model.platforms[temp[i]].upper_left.y:
                    index = temp[i]
        return index

    # get all entity information
    def entity_exists(self):
        return (True if self.model.entities else False)
    
    def get_all_drop_pistol_bullet_position(self):
        return [tuple(entity.position) for entity in self.model.entities if isinstance(entity, PistolBullet)]
    
    def get_all_drop_pistol_bullet_timer(self):
        return [entity.timer / Const.FPS for entity in self.model.entities if isinstance(entity, PistolBullet)]
    
    def get_all_pistol_bullet_velocity(self):
        return [tuple(entity.velocity) for entity in self.model.entities if isinstance(entity, PistolBullet)]
            
    def get_all_drop_banana_peel_position(self):
        return [tuple(entity.position) for entity in self.model.entities if isinstance(entity, BananaPeel)]
    
    def get_all_drop_banana_peel_timer(self):
        return [entity.timer / Const.FPS for entity in self.model.entities if isinstance(entity, BananaPeel)]
    
    def get_all_drop_cancer_bomb_position(self):
        return [tuple(entity.position) for entity in self.model.entities if isinstance(entity, CancerBomb)]

    def get_all_drop_cancer_bomb_timer(self):
        return [entity.timer / Const.FPS for entity in self.model.entities if isinstance(entity, CancerBomb)]
    
    def get_all_drop_big_black_hole_position(self):
        return [tuple(entity.position) for entity in self.model.entities if isinstance(entity, BigBlackHole)]

    def get_all_drop_big_black_hole_timer(self):
        return [entity.timer / Const.FPS for entity in self.model.entities if isinstance(entity, BigBlackHole)]

    def get_all_entity_position(self):
        return [tuple(entity.position) for entity in self.model.entities]
    
    def walk_to_position(self,target_position):
        player_position = tuple(self.model.players[self.player_id].position)
        player_above_which_land = self.get_above_which_land(player_position)
        target_above_which_land = self.get_above_which_land(target_position)
        command = AI_DIR_STAY        
        self_velocity = self.get_self_velocity()
        self_jump_quota = self.get_self_jump_quota()
        closest_land_vector = self.get_position_vector_to_closest_land()
        if self_velocity[1] > 0 and self_jump_quota == 0 :
            if closest_land_vector[0] < 0:
                command = AI_DIR_LEFT
            else:
                command = AI_DIR_RIGHT
        elif player_above_which_land == -1:
            if self_velocity[1] >= 0 and self_jump_quota > 0 and player_position[1] > target_position[1]:
                command = AI_DIR_JUMP
            elif player_position[0] > target_position[0]:
                command = AI_DIR_LEFT
            else:
                command = AI_DIR_RIGHT
        elif player_above_which_land == target_above_which_land or player_position[1] > target_position[1]:
            if self_velocity[1] >= 0 and self_jump_quota > 0 and abs(player_position[0] - target_position[0]) < 10 and abs(player_position[1] - target_position[1]) > Const.PLAYER_RADIUS*2:
                command = AI_DIR_JUMP
            elif player_position[0] > target_position[0]:
                command = AI_DIR_LEFT
            else:
                command = AI_DIR_RIGHT
        elif player_position[1] <= target_position[1]:
            if self.model.stage == Const.STAGE_1:
                if player_above_which_land == 2:
                    if player_position[0] < 680:
                        command = AI_DIR_LEFT
                    else:
                        command = AI_DIR_RIGHT 
                elif player_above_which_land == 1:
                    command = AI_DIR_RIGHT
                elif player_above_which_land == 3:
                    command = AI_DIR_LEFT
            elif self.model.stage == Const.STAGE_2:
                if player_position[0] < 680:
                    command = AI_DIR_RIGHT
                else:
                    command = AI_DIR_LEFT
            elif self.model.stage == Const.STAGE_3:
                if player_above_which_land == 4:
                    command = AI_DIR_RIGHT
                elif player_above_which_land == 5:
                    command = AI_DIR_LEFT
                elif player_above_which_land == 3 or player_above_which_land == 2:
                    if target_above_which_land == 2:
                        if player_position[0] < 680:
                            command = AI_DIR_LEFT
                        else:
                            command = AI_DIR_RIGHT
                    else:
                        if player_position[0] > target_position[0]:
                            command = AI_DIR_LEFT
                        else:
                            command = AI_DIR_RIGHT
                elif player_above_which_land == 0:
                    command = AI_DIR_RIGHT
                elif player_above_which_land == 1:
                    command = AI_DIR_LEFT
        return command
