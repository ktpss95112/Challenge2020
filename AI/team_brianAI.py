import random
import math

# action
AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_LEFT_JUMP   = 3
AI_DIR_RIGHT_JUMP  = 4
AI_DIR_ATTACK      = 5
AI_DIR_USE_ITEM    = 6
AI_DIR_STAY        = 7

# item_id
NO_ITEM            = 0
BANANA_PISTOL      = 1
BIG_BLACK_HOLE     = 2
CANCER_BOMB        = 3
ZAP_ZAP_ZAP        = 4
BANANA_PEEL        = 5
RAINBOW_GROUNDER   = 6
INVINCIBLE_BATTERY = 7

# Constant
DELTA = 1
DEBUG = 0

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0, 0]
        self.last_position = (0, 0)
        self.stack = [random.randint(0, 4), random.randint(0, 4)]
        self.last_platform = -1
        self.last_platform_vec = (0, 0)
        self.timer = 600
    
    def get_closest_land_id(self, my_pos, my_speed, lands):
        min_dis = 10000 ** 2
        min_id = 0
        for id, platform in enumerate(lands):
            platformy = platform[0][1]
            if platform[0][1] - self.helper.get_self_radius() > my_pos[1] and platform[0][0] > my_pos[0]:
                dis = self.helper.get_distance(my_pos, (platform[0][0] + self.helper.get_self_radius() - my_speed[0] * DELTA, platformy))
            elif platform[0][1] - self.helper.get_self_radius() > my_pos[1] and platform[1][0] < my_pos[0]:
                dis = self.helper.get_distance(my_pos, (platform[1][0] - self.helper.get_self_radius() - my_speed[0] * DELTA, platformy))
            else:
                dis = self.helper.get_distance(my_pos, (my_pos[0], platformy))
            if dis < min_dis:
                min_dis = dis
                min_id = id
        return min_id

    def get_dis_to_platform(self, my_pos, lands, id):
        if lands[id][0][0] < my_pos[0] < lands[id][1][0]:
            return self.helper.get_distance(my_pos, (my_pos[0], lands[id][0][1]))
        return self.helper.get_distance(my_pos, ((lands[id][0][0] + lands[id][1][0]) / 2, lands[id][0][1]))
    
    def get_vec_to_platform(self, my_pos, lands, id):
        if lands[id][0][0] < my_pos[0] < lands[id][1][0]:
            if abs(lands[id][0][0] - my_pos[0]) < abs(lands[id][1][0] - my_pos[0]):
                return (1, lands[id][0][1] - my_pos[1])
            else:
                return (-1, lands[id][0][1] - my_pos[1])
        return ((lands[id][0][0] + lands[id][1][0]) / 2 - my_pos[0], lands[id][0][1] - my_pos[1])

    def get_position_vector_to_closest_land(self, my_pos, my_speed, lands):
        min_id = self.get_closest_land_id(my_pos, my_speed, lands)
        return ((lands[min_id][0][0] + lands[min_id][1][0]) / 2 - my_pos[0], lands[min_id][0][1] - my_pos[1])

    def no_target(self, id):
        if id is None:
            return 0
        if (self.helper.get_other_is_invincible(id) or \
               self.helper.get_other_life(id) == 0 or \
               self.helper.get_above_which_platform(self.helper.get_other_position(id)) == -1) or\
               self.helper.get_self_id() == id or \
               self.helper.get_other_voltage(id) < self.timer / 6:
            return 1
        return 0

    def x_distance_to_platform(self, x, platform):
        return min(abs(platform[0][0] - x), abs(platform[1][0] - x))
    
    def decide(self):
        
        my_pos = self.helper.get_self_position()
        my_radius = self.helper.get_self_radius()
        my_speed = self.helper.get_self_velocity()
        other_list = []
        gbound = self.helper.get_game_arena_boundary()
        bound = self.helper.get_game_life_boundary()
        lands = self.helper.get_platform_position()

        for i in range(4):
            if self.no_target(i) == 0:
                other_list.append(i)

        if other_list == []:
            self.timer = max(self.timer - 1, 0)
            if DEBUG == 1:
                print('Here1')
            if self.helper.get_self_keep_item_id() != NO_ITEM:
                return AI_DIR_USE_ITEM

            cancer_pos = self.helper.get_all_drop_cancer_bomb_position()
            cancer_time = self.helper.get_all_drop_cancer_bomb_timer()

            for pos, time in zip(cancer_pos, cancer_time):
                if time <= 0.5 and self.helper.get_distance(my_pos, pos) < 400:
                    #print('here5')
                    if (pos[0] > my_pos[0] and my_pos[0] - self.helper.get_self_radius() * 4 > gbound[0][0]) or \
                        my_pos[0] + self.helper.get_self_radius() * 4 > gbound[1][0]:
                        return AI_DIR_LEFT_JUMP
                    else:
                        return AI_DIR_RIGHT_JUMP
            
            # get distance to other player
            distance = self.helper.get_all_player_distance()
            distance.pop(self.helper.get_self_id())
        
            if self.helper.get_self_can_attack() and\
                min(d for d in distance if not d is None) < self.helper.get_self_attack_radius():
                return AI_DIR_ATTACK

            min_count = 100
            platform_id = -1
            for i in range(len(lands)):
                cnt = 0
                for j in range(4):
                    if j != self.helper.get_self_id():
                        pos = self.helper.get_other_position(j)
                        if not pos is None and self.helper.get_above_which_platform(pos) == i:
                            cnt += 1
                    if cnt < min_count:
                        platform_id = i
            return self.helper.walk_to_position(((lands[platform_id][0][0] + lands[platform_id][1][0]) / 2, lands[platform_id][0][1] + 5))
        else:
            min_dis = 10000 ** 2
            other_id = other_list[0]
            for i in other_list:
                if min_dis > self.helper.get_distance(my_pos, self.helper.get_other_position(i)):
                    min_dis = self.helper.get_distance(my_pos, self.helper.get_other_position(i))
                    other_id = i

        self.timer = min(self.timer + 5, 600)
        other_pos = self.helper.get_other_position(other_id)

        if my_pos[0] < bound[0][0] + self.helper.get_self_radius() * 6:
            #print('here0')
            if my_speed[1] >= 0:
                if DEBUG == 1:
                    print('Here2')
                return AI_DIR_RIGHT_JUMP
            else:
                if DEBUG == 1:
                    print('Here3')
                return AI_DIR_RIGHT
        elif my_pos[0] > bound[1][0] - self.helper.get_self_radius() * 6:
            #print('here1')
            if my_speed[1] >= 0:
                if DEBUG == 1:
                    print('Here4')
                return AI_DIR_LEFT_JUMP
            else:
                if DEBUG == 1:
                    print('Here5')
                return AI_DIR_LEFT
        
        distance = self.helper.get_all_player_distance()
        distance.pop(self.helper.get_self_id())
        
        if self.helper.get_self_can_attack() and\
            min(d for d in distance if not d is None) < self.helper.get_self_attack_radius() / 6:
            if DEBUG == 1:
                print('Here6')
            return AI_DIR_ATTACK
        
        if self.helper.get_self_uncontrollable_time() > 0 and my_speed[1] >= 0:
            if DEBUG == 1:
                print('Here7')
            return AI_DIR_JUMP

        # the area below is empty
        flag = 1
        for platform in lands:
            if platform[0][1] > my_pos[1] + self.helper.get_self_radius():
                h = platform[0][1] - my_pos[1] - self.helper.get_self_radius()
                t = (-my_speed[1] + math.sqrt(my_speed[1] ** 2 + 2 * h * self.helper.get_game_gravity_acceleration())) / self.helper.get_game_gravity_acceleration()
                #print(my_pos,my_speed,platform,t)
                if (t >= 0.08 * (4 - self.helper.get_self_jump_quota()) and self.x_distance_to_platform(my_pos[0] + my_speed[0] * t, platform) < self.helper.get_self_radius() * (1.5 + self.helper.get_self_jump_quota())) or \
                    platform[0][0] + self.helper.get_self_radius() * 1.5  < my_pos[0] + my_speed[0] * t < platform[1][0] - self.helper.get_self_radius() * 1.5:
                    flag = 0
        
        if flag == 1:
            #print("here2")
            #print('*****',self.last_platform)
            if self.last_platform != -1 and max(abs(self.last_platform_vec[0]), 5) > abs(self.get_vec_to_platform(my_pos, lands, self.last_platform)[0]):
                land_vec = self.get_vec_to_platform(my_pos, lands, self.last_platform)
                self.last_platform_vec = self.get_vec_to_platform(my_pos, lands, self.last_platform)
            else:
                self.last_platform = self.get_closest_land_id(my_pos, my_speed, lands)
                land_vec = self.get_vec_to_platform(my_pos, lands, self.last_platform)
                self.last_platform_vec = self.get_vec_to_platform(my_pos, lands, self.last_platform)
            if land_vec[0] > 0:
                if my_speed[1] >= 0 and (my_speed[1] > 50 or land_vec[1] <= -self.helper.get_self_radius() * 1.6):
                    if DEBUG == 1:
                        print('Here8')
                    return AI_DIR_RIGHT_JUMP
                else:
                    if DEBUG == 1:
                        print('Here9')
                    return AI_DIR_RIGHT
            else:
                if my_speed[1] >= 0 and (my_speed[1] > 50 or land_vec[1] <= -self.helper.get_self_radius() * 1.6):
                    if DEBUG == 1:
                        print('Here10')
                    return AI_DIR_LEFT_JUMP
                else:
                    if DEBUG == 1:
                        print('Here11')
                    return AI_DIR_LEFT
        
        if len(self.stack) > 0:
            rt = self.stack[-1]
            self.stack.pop()
            if DEBUG == 1:
                print('Here12')
            return rt

        if self.helper.get_self_keep_item_id() > 0:
            if self.helper.get_self_keep_item_id() == 1:
                if DEBUG == 1:
                    print('Here13')
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 2:
                self.stack.append(AI_DIR_USE_ITEM)
                self.stack.append(AI_DIR_JUMP)
                if DEBUG == 1:
                    print('Here14')
                return AI_DIR_JUMP
            elif self.helper.get_self_keep_item_id() == 3:
                if self.helper.get_distance(my_pos, other_pos) < 500:
                    if DEBUG == 1:
                        print('Here15')
                    return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 4:
                if abs(other_pos[0] - my_pos[0]) <= self.helper.get_zap_zap_zap_effect_range():
                    if DEBUG == 1:
                        print('Here16')
                    return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 5:
                if DEBUG == 1:
                    print('Here17')
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 6:
                if DEBUG == 1:
                    print('Here18')
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 7:
                if DEBUG == 1:
                    print('Here19')
                return AI_DIR_USE_ITEM
            
        cancer_pos = self.helper.get_all_drop_cancer_bomb_position()
        cancer_time = self.helper.get_all_drop_cancer_bomb_timer()

        for pos, time in zip(cancer_pos, cancer_time):
            if time <= 0.5 and self.helper.get_distance(my_pos, pos) < 400:
                #print('here5')
                if (pos[0] > my_pos[0] and my_pos[0] - self.helper.get_self_radius() * 4 > gbound[0][0]) or \
                    my_pos[0] + self.helper.get_self_radius() * 4 > gbound[1][0]:
                    if DEBUG == 1:
                        print('Here20')
                    return AI_DIR_LEFT_JUMP
                else:
                    if DEBUG == 1:
                        print('Here21')
                    return AI_DIR_RIGHT_JUMP
        
        if self.helper.get_self_can_attack() and \
            min(d for d in distance if not d is None) < self.helper.get_self_attack_radius():
            if DEBUG == 1:
                print('Here6')
            return AI_DIR_ATTACK
    
        self.last_platform = self.helper.get_above_which_platform(other_pos)
        if self.last_platform != -1:
            self.last_platform_vec = self.get_vec_to_platform(my_pos, lands, self.last_platform)
        other_platform = lands[self.helper.get_above_which_platform(other_pos)]
        if abs(other_pos[0] - other_platform[0][0]) < abs(other_pos[0] - other_platform[1][0]):
            return self.helper.walk_to_position((other_pos[0] + self.helper.get_self_radius(), other_pos[1] - self.helper.get_self_radius()))
        else:
            return self.helper.walk_to_position((other_pos[0] - self.helper.get_self_radius(), other_pos[1] - self.helper.get_self_radius()))
        '''
        self.last_position = my_pos
        print(other_id,other_pos,my_pos)
        if self.helper.get_distance(my_pos, other_pos) > self.helper.get_self_attack_radius() or \
           (not self.helper.get_self_can_attack()):
            if other_pos[1] + self.helper.get_self_radius() < my_pos[1]:
                #print('here4')
                if other_pos[0] > my_pos[0]:
                    if DEBUG == 1:
                        print('Here22')
                    return AI_DIR_RIGHT_JUMP
                else:
                    if DEBUG == 1:
                        print('Here23')
                    return AI_DIR_LEFT_JUMP
            else:
                close_land_vec = self.helper.get_position_vector_to_closest_land()
                curr_land = lands[self.helper.get_above_which_platform(my_pos)]
                self.last_platform = self.helper.get_above_which_platform(other_pos)
                other_land = lands[self.last_platform]
                self.last_platform_vec = self.get_vec_to_platform(my_pos, lands, self.last_platform)
                #print('here3')
                if curr_land[0][1] > other_pos[1] and curr_land[0][0] < other_pos[0] < curr_land[1][0]: 
                    if my_pos[0] > other_pos[0]:
                        if my_speed[1] >= 0:
                            if DEBUG == 1:
                                print('Here24')
                            return AI_DIR_LEFT_JUMP
                        else:
                            if DEBUG == 1:
                                print('Here25')
                            return AI_DIR_LEFT
                    else:
                        if my_speed[1] >= 0:
                            if DEBUG == 1:
                                print('Here26')
                            return AI_DIR_RIGHT_JUMP
                        else:
                            if DEBUG == 1:
                                print('Here27')
                            return AI_DIR_RIGHT
                elif (min(abs(curr_land[0][0] - other_land[0][0]), abs(curr_land[0][0] - other_land[1][0]))< \
                     min(abs(curr_land[1][0] - other_land[0][0]), abs(curr_land[1][0] - other_land[1][0])) or\
                     curr_land[1][0] + self.helper.get_self_radius() * 4 > gbound[1][0]) and \
                     curr_land[0][0] - self.helper.get_self_radius() * 4 > gbound[0][0]:
                    if DEBUG == 1:
                        print('Here28')
                    return AI_DIR_LEFT
                else:
                    if DEBUG == 1:
                        print('Here29')
                    return AI_DIR_RIGHT
        else:
            if DEBUG == 1:
                print('Here30')
            return AI_DIR_ATTACK
        '''