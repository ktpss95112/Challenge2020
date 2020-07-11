from API.base import BaseAI
import random
import math

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
        self.enhancement = [0, 0, 0, 0]
        self.last_position = (0, 0)
        self.stack = [random.randint(0, 4), random.randint(0, 4)]

    def get_position_vector_to_closest_land(self, my_pos, lands):
        min_dis = 10000 ** 2
        min_vec = (0, 0)
        for platform in lands:
            dis = self.helper.get_distance(my_pos, ((platform[0][0] + platform[1][0]) / 2, platform[0][1]))
            if dis < min_dis:
                min_dis = dis
                min_vec = ((platform[0][0] + platform[1][0]) / 2 - my_pos[0], platform[0][1] - my_pos[1])
        return min_vec
    
    def decide(self):

        my_pos = self.helper.get_self_position()
        my_radius = self.helper.get_self_radius()
        my_speed = self.helper.get_self_velocity()
        other_id = self.helper.get_nearest_player()
        if self.helper.get_other_is_invincible(other_id):
            other_id = self.helper.get_highest_voltage_player()
        elif self.helper.get_other_is_invincible(other_id):
            other_id = self.helper.get_highest_score_player()
        other_pos = self.helper.get_other_position(other_id)
        bound = self.helper.get_game_arena_boundary()
        lands = self.helper.get_platform_position()

        if my_speed[1] >= 0:
            if my_pos[0] < bound[0][0] + self.helper.get_self_radius():
                return AI_DIR_RIGHT_JUMP
            elif my_pos[0] > bound[1][0] - self.helper.get_self_radius():
                return AI_DIR_LEFT_JUMP

        if self.helper.get_distance(my_pos, other_pos) < self.helper.get_self_attack_radius() / 8 and self.helper.get_self_can_attack_time() == 0:
            return AI_DIR_ATTACK

        # the area below is empty
        flag = 1
        for platform in lands:
            if platform[0][1] > my_pos[1]:
                h = platform[0][1] - my_pos[1]
                t = (-my_speed[1] + math.sqrt(my_speed[1] ** 2 + 2 * h * self.helper.get_game_player_gravity_acceleration()))/ self.helper.get_game_player_gravity_acceleration()
                if platform[0][0] + self.helper.get_self_radius() * 1.5  < my_pos[0] + my_speed[0] * t < platform[1][0] - self.helper.get_self_radius() * 1.5:
                    flag = 0
        
        if my_speed[1] >= 0:
            if flag == 1:
                land_vec = self.get_position_vector_to_closest_land(my_pos, lands)
                if land_vec[0] > 0:
                    return AI_DIR_RIGHT_JUMP
                else:
                    return AI_DIR_LEFT_JUMP

        if len(self.stack) > 0:
            rt = self.stack[-1]
            self.stack.pop()
            return rt

        if self.helper.get_self_keep_item_id() > 0:
            if self.helper.get_self_keep_item_id() == 1:
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 2:
                self.stack.append(AI_DIR_USE_ITEM)
                self.stack.append(AI_DIR_JUMP)
                return AI_DIR_JUMP
            elif self.helper.get_self_keep_item_id() == 3:
                if self.helper.get_distance(my_pos, other_pos) < 500:
                    return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 4:
                if abs(other_pos[0] - my_pos[0]) <= 120:
                    return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 5:
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 6:
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 7:
                return AI_DIR_USE_ITEM
            
        cancer_pos = self.helper.get_all_drop_cancer_bomb_position()
        cancer_time = self.helper.get_all_drop_cancer_bomb_timer()

        for pos, time in zip(cancer_pos, cancer_time):
            if time <= 1 and self.helper.get_distance(my_pos, pos) < 400:
                if pos[0] > my_pos[0]:
                    return AI_DIR_LEFT_JUMP
                else:
                    return AI_DIR_RIGHT_JUMP

        if len(self.helper.get_all_big_black_hole_position()) > 0:
            return self.helper.walk_to_position(self.last_position)

        if self.helper.get_self_uncontrollable_time() > 0:
            return AI_DIR_JUMP

        self.last_position = my_pos

        if self.helper.get_distance(my_pos, other_pos) > self.helper.get_self_attack_radius() / 3:
            far = 0
            if abs(my_pos[0] - other_pos[0]) > abs(bound[0][0] - bound[1][0]) / 4:
                far = 1
            if other_pos[1] < my_pos[1]:
                if other_pos[0] > my_pos[0]:
                    if far == 1:
                        self.stack.append(AI_DIR_RIGHT_JUMP)
                    return AI_DIR_RIGHT_JUMP
                else:
                    if far == 1:
                        self.stack.append(AI_DIR_LEFT_JUMP)
                    return AI_DIR_LEFT_JUMP
            else:
                if other_pos[0] > my_pos[0]:
                    return AI_DIR_RIGHT
                else:
                    return AI_DIR_LEFT
        else:
            return AI_DIR_ATTACK
        
