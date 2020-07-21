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

"""
When return timers or velocity, please use "second" as time unit.
document: https://hackmd.io/c7plwdAjS6yX-37Kh7PXaw?view
"""
class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.player_id = index

    # get game information
    def get_game_left_time(self):
        return (Const.GAME_LENGTH - self.model.timer) / Const.FPS

    def get_game_stage(self):
        return self.model.stage

    def get_game_arena_boundary(self):
        # return upper-left and bottom-right coordinate of arena boundary
        return ((0, 0), Const.ARENA_SIZE)

    def get_game_life_boundary(self):
        # return upper-left and bottom-right coordinate of life boundary
        return ((Const.LIFE_BOUNDARY[0], Const.LIFE_BOUNDARY[1]), (Const.LIFE_BOUNDARY[0] + Const.LIFE_BOUNDARY[2], Const.LIFE_BOUNDARY[1] + Const.LIFE_BOUNDARY[3]))

    def get_game_gravity_acceleration(self):
        return Const.GRAVITY_ACCELERATION / Const.FPS

    def get_live_player_num(self):
        return sum(1 if player.life > 0 else 0 for player in self.model.players)
    
    # get self information
    def get_self_id(self):
        return self.player_id
    
    def get_self_position(self):
        return tuple(self.model.players[self.player_id].position) if self.model.players[self.player_id].is_alive() else None

    def get_self_velocity(self):
        return tuple(self.model.players[self.player_id].velocity) if self.model.players[self.player_id].is_alive() else None

    def get_self_direction(self):
        return tuple(self.model.players[self.player_id].direction) if self.model.players[self.player_id].is_alive() else None

    def get_self_normal_speed(self):
        return self.model.players[self.player_id].normal_speed if self.model.players[self.player_id].is_alive() else None

    def get_self_jump_speed(self):
        return self.model.players[self.player_id].jump_speed if self.model.players[self.player_id].is_alive() else None

    def get_self_keep_item_id(self):
        return self.model.players[self.player_id].keep_item_id if self.model.players[self.player_id].is_alive() else None

    def get_self_voltage(self):
        return self.model.players[self.player_id].voltage if self.model.players[self.player_id].is_alive() else None

    def get_self_radius(self):
        return self.model.players[self.player_id].player_radius if self.model.players[self.player_id].is_alive() else None

    def get_self_attack_radius(self):
        return self.model.players[self.player_id].attack_radius if self.model.players[self.player_id].is_alive() else None

    def get_self_is_invincible(self):
        return self.model.players[self.player_id].is_invincible() if self.model.players[self.player_id].is_alive() else None
    
    def get_self_invincible_time(self):
        return self.model.players[self.player_id].invincible_time / Const.FPS if self.model.players[self.player_id].is_alive() else None

    def get_self_is_controllable(self):
        return self.model.players[self.player_id].uncontrollable_time <= 0 if self.model.players[self.player_id].is_alive() else None

    def get_self_uncontrollable_time(self):
        return self.model.players[self.player_id].uncontrollable_time / Const.FPS if self.model.players[self.player_id].is_alive() else None

    def get_self_can_attack(self):
        return self.model.players[self.player_id].can_attack() if self.model.players[self.player_id].is_alive() else None

    def get_self_can_attack_time(self):
        return self.model.players[self.player_id].attack_cool_down_time / Const.FPS if self.model.players[self.player_id].is_alive() else None

    def get_self_can_jump(self):
        return (self.get_self_jump_quota() > 0) if self.model.players[self.player_id].is_alive() else None

    def get_self_jump_quota(self):
        return self.model.players[self.player_id].jump_quota if self.model.players[self.player_id].is_alive() else None

    def get_self_life(self):
        return self.model.players[self.player_id].life

    def get_self_score(self):
        return self.model.players[self.player_id].score

    def get_self_jump_to_the_highest_time(self):
        return (-self.model.players[self.player_id].velocity.y / Const.GRAVITY_ACCELERATION if self.model.players[self.player_id].velocity.y < 0 else 0)\
                if self.model.players[self.player_id].is_alive() else None

    def get_self_have_platform_below(self):
        if not self.model.players[self.player_id].is_alive():
            return None
        self_position = self.get_self_position()
        self_radius = self.get_self_radius()
        platforms = self.get_platform_position()
        for platform in platforms:
            if platform[0][0] < self_position[0] < platform[1][0] and self_position[1] + self_radius <= platform[0][1]:
                return True
        return False
    
    # get all player information 
    def get_all_position(self):
        return [tuple(player.position) if player.is_alive() else None for player in self.model.players]

    def get_all_velocity(self):
        return [tuple(player.velocity) if player.is_alive() else None for player in self.model.players]

    def get_all_direction(self):
        return [tuple(player.direction) if player.is_alive() else None for player in self.model.players]

    def get_all_normal_speed(self):
        return [player.normal_speed if player.is_alive() else None for player in self.model.players]

    def get_all_jump_speed(self):
        return [player.jump_speed if player.is_alive() else None for player in self.model.players]
    
    def get_all_keep_item_id(self):
        return [player.keep_item_id if player.is_alive() else None for player in self.model.players]

    def get_all_voltage(self):
        return [player.voltage if player.is_alive() else None for player in self.model.players]

    def get_all_radius(self):
        return [player.player_radius if player.is_alive() else None for player in self.model.players]

    def get_all_attack_radius(self):
        return [player.attack_radius if player.is_alive() else None for player in self.model.players]

    def get_all_is_invincible(self):
        return [player.is_invincible() if player.is_alive() else None for player in self.model.players]
    
    def get_all_invincible_time(self):
        return [player.invincible_time / Const.FPS if player.is_alive() else None for player in self.model.players]

    def get_all_is_controllable(self):
        return [player.uncontrollable_time <= 0 if player.is_alive() else None for player in self.model.players]

    def get_all_uncontrollable_time(self):
        return [player.uncontrollable_time / Const.FPS if player.is_alive() else None for player in self.model.players]
    
    def get_all_can_attack(self):
        return [player.can_attack() if player.is_alive() else None for player in self.model.players]

    def get_all_can_attack_time(self):
        return [player.attack_cool_down_time / Const.FPS if player.is_alive() else None for player in self.model.players]

    def get_all_can_jump(self):
        return [player.jump_quota > 0 if player.is_alive() else None for player in self.model.players]

    def get_all_jump_quota(self):
        return [player.jump_quota if player.is_alive() else None for player in self.model.players]

    def get_all_life(self):
        return [player.life for player in self.model.players]

    def get_all_score(self):
        return [player.score for player in self.model.players]

    def get_all_jump_to_the_highest_time(self):
        return [(-player.velocity.y / Const.GRAVITY_ACCELERATION if player.velocity.y < 0 else 0) if player.is_alive() else None\
                for player in self.model.players]
    
    def get_all_player_vector(self):
        return [self.get_vector(self.get_self_position(), player.position) if player.is_alive() else None\
                for player in self.model.players]
    
    def get_all_player_distance(self):
        return [self.get_distance(self.get_self_position(), player.position) if player.is_alive() else None\
                for player in self.model.players]

    # get other players information
    def get_other_position(self, index):
        return tuple(self.model.players[index].position) if self.model.players[index].is_alive() else None

    def get_other_velocity(self, index):
        return tuple(self.model.players[index].velocity) if self.model.players[index].is_alive() else None

    def get_other_direction(self, index):
        return tuple(self.model.players[index].direction) if self.model.players[index].is_alive() else None

    def get_other_normal_speed(self, index):
        return self.model.players[index].normal_speed if self.model.players[index].is_alive() else None

    def get_other_jump_speed(self, index):
        return self.model.players[index].jump_speed if self.model.players[index].is_alive() else None

    def get_other_keep_item_id(self, index):
        return self.model.players[index].keep_item_id if self.model.players[index].is_alive() else None

    def get_other_voltage(self, index):
        return self.model.players[index].voltage if self.model.players[index].is_alive() else None

    def get_other_radius(self, index):
        return self.model.players[index].player_radius if self.model.players[index].is_alive() else None

    def get_other_attack_radius(self, index):
        return self.model.players[index].attack_radius if self.model.players[index].is_alive() else None

    def get_other_is_invincible(self, index):
        return (self.model.players[index].is_invincible()) if self.model.players[index].is_alive() else None
    
    def get_other_invincible_time(self, index):
        return self.model.players[index].invincible_time / Const.FPS if self.model.players[index].is_alive() else None

    def get_other_is_controllable(self, index):
        return self.model.players[index].uncontrollable_time <= 0 if self.model.players[index].is_alive() else None

    def get_other_uncontrollable_time(self, index):
        return self.model.players[index].uncontrollable_time / Const.FPS if self.model.players[index].is_alive() else None
    
    def get_other_can_jump(self, index):
        return (self.model.players[index].jump_quota > 0) if self.model.players[index].is_alive() else None

    def get_other_jump_quota(self, index):
        return self.model.players[index].jump_quota if self.model.players[index].is_alive() else None

    def get_other_can_attack(self, index):
        return self.model.players[index].can_attack() if self.model.players[index].is_alive() else None

    def get_other_can_attack_time(self, index):
        return self.model.players[index].attack_cool_down_time / Const.FPS if self.model.players[index].is_alive() else None

    def get_other_life(self, index):
        return self.model.players[index].life

    def get_other_score(self, index):
        return self.model.players[index].score

    def get_other_jump_to_the_highest_time(self, index):
        return (-self.model.players[index].velocity.y / Const.GRAVITY_ACCELERATION if self.model.players[index].velocity.y < 0 else 0)\
                if self.model.players[index].is_alive() else None

    def get_other_have_platform_below(self, index):
        if not self.model.players[index].is_alive():
            return None
        other_position = self.get_other_position(index)
        other_radius = self.get_other_radius(index)
        platforms = self.get_platform_position()
        for platform in platforms:
            if platform[0][0] < other_position[0] < platform[1][0] and other_position[1] + other_radius <= platform[0][1]:
                return True
        return False

    def get_other_player_vector(self, index):
        return self.get_vector(self.get_self_position(), self.get_other_position(index))\
                if self.model.players[index].is_alive() else None

    def get_other_player_distance(self, index):
        return self.get_distance(self.get_self_position(), self.get_other_position(index))\
                if self.model.players[index].is_alive() else None

    # get platform information 
    def get_platform_position(self):
        return [(tuple(platform.upper_left), tuple(platform.bottom_right)) for platform in self.model.platforms]
    
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

    def get_above_which_platform(self, position):
        index = -1
        current_platform_y = 10000
        for i, platform in enumerate(self.get_platform_position()):
            if platform[0][0] - 20 <= position[0] <= platform[1][0] + 20 and\
                position[1] <= platform[0][1] <= current_platform_y:
                index, current_platform_y = i, platform[0][1]
        return index

    # get item information
    def item_exists(self):
        return (True if self.model.items else False)

    def get_nearest_item_position(self):
        nearest_pos, minimum_distance = None, 10000 ** 2 
        for item in self.model.items:
            distance = self.get_distance(self.get_self_position(), item.position)
            if distance < minimum_distance:
                minimum_distance, nearest_pos = distance, tuple(item.position)
        return nearest_pos

    def get_all_item_position(self):
        return [tuple(item.position) for item in self.model.items]

    def get_nearest_specific_item_position(self,items_id):
        nearest_pos, minimum_distance = None , 10000**2
        specific_items = [item for item in self.model.items if item.item_id == items_id]
        for item in specific_items:
            distance = self.get_distance(self.get_self_position(), item.position)
            if distance < minimum_distance:
                minimum_distance, nearest_pos = distance , tuple(item.position)
        return nearest_pos
    
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

    # get all entity information
    def entity_exists(self):
        return (True if self.model.entities else False)

    def get_all_entity_position(self):
        return [tuple(entity.position) for entity in self.model.entities] 
    
    def get_all_drop_pistol_bullet_position(self):
        return [tuple(entity.position) for entity in self.model.entities if isinstance(entity, PistolBullet)]

    def get_nearest_drop_pistol_bullet_position(self):
        nearest_pos, minimum_distance = None , 10000**2
        bullets = [entity for entity in self.model.entities if isinstance(entity, PistolBullet)]
        for bullet in bullets:
            distance = self.get_distance(self.get_self_position(), bullet.position)
            if distance < minimum_distance:
                minimum_distance, nearest_pos = distance , tuple(bullet.position)
        return nearest_pos
    
    def get_all_drop_pistol_bullet_timer(self):
        return [entity.timer / Const.FPS for entity in self.model.entities if isinstance(entity, PistolBullet)]
    
    def get_all_pistol_bullet_velocity(self):
        return [tuple(entity.velocity) for entity in self.model.entities if isinstance(entity, PistolBullet)]
            
    def get_all_drop_banana_peel_position(self):
        return [tuple(entity.position) for entity in self.model.entities if isinstance(entity, BananaPeel)]
    
    def get_nearest_drop_banana_peel_position(self):
        nearest_pos, minimum_distance = None , 10000**2
        peels = [entity for entity in self.model.entities if isinstance(entity, BananaPeel)]
        for peel in peels:
            distance = self.get_distance(self.get_self_position(), peel.position)
            if distance < minimum_distance:
                minimum_distance, nearest_pos = distance , tuple(peel.position)
        return nearest_pos
    
    def get_all_drop_banana_peel_timer(self):
        return [entity.timer / Const.FPS for entity in self.model.entities if isinstance(entity, BananaPeel)]
    
    def get_all_drop_cancer_bomb_position(self):
        return [tuple(entity.position) for entity in self.model.entities if isinstance(entity, CancerBomb)]

    def get_nearest_drop_cancer_bomb_position(self):
        nearest_pos, minimum_distance = None , 10000**2
        bombs = [entity for entity in self.model.entities if isinstance(entity, CancerBomb)]
        for bomb in bombs:
            distance = self.get_distance(self.get_self_position(), bomb.position)
            if distance < minimum_distance:
                minimum_distance, nearest_pos = distance , tuple(bomb.position)
        return nearest_pos

    def get_all_drop_cancer_bomb_timer(self):
        return [entity.timer / Const.FPS for entity in self.model.entities if isinstance(entity, CancerBomb)]
    
    def get_all_drop_big_black_hole_position(self):
        return [tuple(entity.position) for entity in self.model.entities if isinstance(entity, BigBlackHole)]

    def get_nearest_drop_big_black_hole_position(self):
        nearest_pos, minimum_distance = None , 10000**2
        holes = [entity for entity in self.model.entities if isinstance(entity, BigBlackHole)]
        for hole in holes:
            distance = self.get_distance(self.get_self_position(), hole.position)
            if distance < minimum_distance:
                minimum_distance, nearest_pos = distance , tuple(hole.position)
        return nearest_pos

    def get_all_drop_big_black_hole_timer(self):
        return [entity.timer / Const.FPS for entity in self.model.entities if isinstance(entity, BigBlackHole)]

    def get_black_hole_effect_radius(self):
        return Const.BLACK_HOLE_EFFECT_RADIUS
    
    def get_cancer_bomb_effect_radius(self):
        return Const.BOMB_EXPLODE_RADIUS

    def get_zap_zap_zap_effect_range(self):
        return Const.ZAP_ZAP_ZAP_RANGE

    # get special information
    def get_nearest_player(self):
        index, minimum_distance = None, 10000 ** 2 
        for player in self.model.players:
            distance = self.get_distance(self.get_self_position(), player.position)
            if player.player_id != self.player_id and player.is_alive() and distance < minimum_distance:
                minimum_distance, index = distance, player.player_id
        return index
    
    def get_nearest_player_position(self):      
         nearest_player = self.get_nearest_player()     
         if nearest_player is not None:     
             return self.get_other_position(nearest_player)     
         else:      
             return None

    def get_highest_voltage_player(self):
        index, highest_voltage = None, -1
        for player in self.model.players:
            if player.player_id != self.player_id and player.is_alive() and\
                player.voltage > highest_voltage:
                highest_voltage, index = player.voltage, player.player_id
        return index

    def get_highest_score_player(self):
        index, highest_score = None, 0
        for player in self.model.players:
            if player.player_id != self.player_id and player.is_alive() and\
                player.score > highest_score:
                highest_score, index = player.score, player.player_id
        return index

    def get_gift_position(self):
        for entity in self.model.entities:
            if isinstance(entity, DeathRain):
                return tuple(entity.position)
        return None

    def get_gift_velocity(self):
        for entity in self.model.entities:
            if isinstance(entity, DeathRain):
                return tuple(entity.velocity)
        return None

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

    # friendly
    def walk_to_position(self, target_position):
        player_position = tuple(self.model.players[self.player_id].position)
        #取得目標與玩家分別在哪個平台之上
        player_above_which_land = self.get_above_which_platform(player_position)
        target_above_which_land = self.get_above_which_platform(target_position)

        command = AI_DIR_STAY # 預設指令       
        self_velocity = self.get_self_velocity() #獲取自身速度
        self_jump_quota = self.get_self_jump_quota() #獲取剩餘跳躍次數
        closest_land_vector = self.get_position_vector_to_closest_land() #離最近的平台的向量

        #如果我正在往下掉、沒有任何跳躍次數、且我下方沒有任何平台時，靠近離我最近的平台
        if self_velocity[1] > 0 and self_jump_quota == 0 and player_above_which_land == -1:
            if closest_land_vector[0] < 0:
                command = AI_DIR_LEFT
            else:
                command = AI_DIR_RIGHT

        #如果我正在往下掉、沒有任何跳躍次數、且我下方有平台時，走到平台的正中心
        elif self_velocity[1] > 0 and self_jump_quota == 0 and player_above_which_land != -1:
            if (self.model.platforms[player_above_which_land].upper_left.x + self.model.platforms[player_above_which_land].bottom_right.x) / 2 - player_position[0] > 0 :
                command = AI_DIR_RIGHT
            else:
                command = AI_DIR_LEFT

        #如果我下方沒有平台時
        elif player_above_which_land == -1:
            #如果我正在往下掉、有跳躍次數、且我的位置比目標還低，則跳躍
            if self_velocity[1] >= 0 and self_jump_quota > 0 and player_position[1] > target_position[1]:
                command = AI_DIR_JUMP
            #x座標上的靠近
            elif player_position[0] > target_position[0]:
                command = AI_DIR_LEFT
            else:
                command = AI_DIR_RIGHT
        #如果我與目標在一樣的平台上 or 我的位置比目標還低
        elif player_above_which_land == target_above_which_land or player_position[1] > target_position[1]:
            #如果我正在往下掉、有跳躍次數、且x,y座標差都在一定的誤差之外，則跳躍
            if self_velocity[1] >= 0 and self_jump_quota > 0 and abs(player_position[0] - target_position[0]) < 10 and abs(player_position[1] - target_position[1]) > Const.PLAYER_RADIUS*2:
                command = AI_DIR_JUMP
            #x座標上的靠近
            elif player_position[0] > target_position[0]:
                command = AI_DIR_LEFT
            else:
                command = AI_DIR_RIGHT
        #如果目標位置比我的位置還低的時候(這裡寫法是在以知道所有平台相對位置的前提去寫的，所以閱讀此段程式碼前，推薦先把Const裡面的各個stage的平台座標看過一次)
        elif player_position[1] <= target_position[1]:
            #stage1的情況
            if self.model.stage == Const.STAGE_1:
                #如果在中間最高的平台上時，靠左走左，靠右走右
                if player_above_which_land == 2:
                    if player_position[0] < 680:
                        command = AI_DIR_LEFT
                    else:
                        command = AI_DIR_RIGHT 
                #如果在中間左邊的平台上時，一律向右
                elif player_above_which_land == 1:
                    command = AI_DIR_RIGHT
                #如果在中間右邊的平台上時，一律向左
                elif player_above_which_land == 3:
                    command = AI_DIR_LEFT
            #stage2的情況
            elif self.model.stage == Const.STAGE_2:
                #如果你的x座標小於587則向右，大於587則向左
                if player_position[0] < 587:
                    command = AI_DIR_RIGHT
                else:
                    command = AI_DIR_LEFT
            #stage3的情況
            elif self.model.stage == Const.STAGE_3:
                #如果你在左上平台則向右
                if player_above_which_land == 4:
                    command = AI_DIR_RIGHT
                #如果你在左下平台則向左
                elif player_above_which_land == 5:
                    command = AI_DIR_LEFT
                #如果你在中間的那兩個平台時
                elif player_above_which_land == 3 or player_above_which_land == 2:
                    #如果目標在中間偏下的平台時(意味著我在中間偏上的平台)，則靠左走左，靠右走右
                    if target_above_which_land == 2:
                        if player_position[0] < 680:
                            command = AI_DIR_LEFT
                        else:
                            command = AI_DIR_RIGHT
                    #其他情況(回過頭看好像也沒什麼例外情況?)，則盡可能在x座標上靠近
                    else:
                        if player_position[0] > target_position[0]:
                            command = AI_DIR_LEFT
                        else:
                            command = AI_DIR_RIGHT
                #如果你在左下方的平台則向右
                elif player_above_which_land == 0:
                    command = AI_DIR_RIGHT
                #如果你在右下方的平台則向左
                elif player_above_which_land == 1:
                    command = AI_DIR_LEFT
        return command
