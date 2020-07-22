import random
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

class TeamAI:
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0, 0]
        self.time_on_the_same_ground = 0
        self.transfer = False
        self.state0 = 0
        self.transfer_target = 0
        self.attack_target = 0
        self.state = 0 # 0 -> wandering, 1 -> escape from bomb, 2 -> attack, 3 -> lowering voltage

    def random_id(self, cur_id):
        ans = cur_id
        num = len(self.helper.get_platform_position())
        while(ans == cur_id):
            ans = random.randint(0, num-1)
        #print(ans, cur_id)
        return ans

    def lowest_plate(self):
    	y = 0
    	for po in self.helper.get_platform_position():
    		y = max(y, po[0][1])
    	#print(y)
    	return y

    def decide(self):
        # emergency jump
        cur_pos = self.helper.get_self_position()
        if cur_pos[1] > self.lowest_plate() or cur_pos[0] < 0 or cur_pos[0] > 1200:
            if cur_pos[0] > 800:
                return AI_DIR_LEFT_JUMP
            elif cur_pos[0] < 400:
                return AI_DIR_RIGHT_JUMP
            else:
                return AI_DIR_JUMP
        # use item
        if self.helper.get_self_keep_item_id() != NO_ITEM:
            return AI_DIR_USE_ITEM

        # attack
        distance = self.helper.get_all_player_distance()
        distance.pop(self.helper.get_self_id())
        if self.helper.get_self_can_attack() and\
            min(d for d in distance if not d is None) < self.helper.get_self_attack_radius():
            return AI_DIR_ATTACK

        # if invincible, then be aggressive
        if self.helper.get_self_is_invincible():	
            enemy_pos = self.helper.get_all_position()
            nearest_enemy_dis, nearest_enemy = 10000, -1
            for i, pos in enumerate(enemy_pos):
                if pos != None and self.helper.get_other_voltage(i) > 70 and nearest_enemy_dis > self.helper.get_distance(self.helper.get_self_position(), pos):
                    nearest_enemy_dis, nearest_enemy = self.helper.get_distance(self.helper.get_self_position(), pos), i
            if nearest_enemy_dis != 10000:
                return self.helper.walk_to_position(self.helper.get_other_position(nearest_enemy))
        

        if self.helper.get_self_voltage() > 50:
            #1 get rainbow
            rainbow_pos = self.helper.get_all_rainbow_grounder_position()
            min_dis_rain, nearest_rainbow_pos = 10000, -1
            for i, pos in enumerate(rainbow_pos):
                if min_dis_rain > self.helper.get_distance(self.helper.get_self_position(), pos):
                    min_dis_rain, nearest_rainbow_pos = self.helper.get_distance(self.helper.get_self_position(), pos), pos
            if min_dis_rain < 400:
                return self.helper.walk_to_position(nearest_rainbow_pos)

            #2 get invincible battery
            battery_pos = self.helper.get_all_invincible_battery_position()
            min_dis_batt, nearest_battery_pos = 10000, -1
            for i, pos in enumerate(battery_pos):
                if min_dis_batt > self.helper.get_distance(self.helper.get_self_position(), pos):
                    min_dis_batt, nearest_battery_pos = self.helper.get_distance(self.helper.get_self_position(), pos), pos
            if min_dis_batt < 400:
                return self.helper.walk_to_position(nearest_battery_pos)
        else:
            #1 get invincible battery
            battery_pos = self.helper.get_all_invincible_battery_position()
            min_dis_batt, nearest_battery_pos = 10000, -1
            for i, pos in enumerate(battery_pos):
                if min_dis_batt > self.helper.get_distance(self.helper.get_self_position(), pos):
                    min_dis_batt, nearest_battery_pos = self.helper.get_distance(self.helper.get_self_position(), pos), pos
            if min_dis_batt < 400:
                return self.helper.walk_to_position(nearest_battery_pos)

            #2 get blackhole
            black_pos = self.helper.get_all_big_black_hole_position()
            min_dis_black, nearest_black_pos = 10000, -1
            for i, pos in enumerate(black_pos):
                if min_dis_black > self.helper.get_distance(self.helper.get_self_position(), pos):
                    min_dis_black, nearest_black_pos = self.helper.get_distance(self.helper.get_self_position(), pos), pos
            if min_dis_black < 400:
                return self.helper.walk_to_position(nearest_black_pos)

            #3 get rainbow
            rainbow_pos = self.helper.get_all_rainbow_grounder_position()
            min_dis_rain, nearest_rainbow_pos = 10000, -1
            for i, pos in enumerate(rainbow_pos):
                if min_dis_rain > self.helper.get_distance(self.helper.get_self_position(), pos):
                    min_dis_rain, nearest_rainbow_pos = self.helper.get_distance(self.helper.get_self_position(), pos), pos
            if min_dis_rain < 400:
                return self.helper.walk_to_position(nearest_rainbow_pos)

        if self.state == 0:
            # escape from bomb
            bomb_pos = self.helper.get_all_cancer_bomb_position()
            escape = False
            for b_pos in bomb_pos:
                if self.helper.get_distance(self.helper.get_self_position(), b_pos) < 2*self.helper.get_cancer_bomb_effect_radius():
                    escape = True
            
            # attack others
            max_voltage = 0
            for i, v in enumerate(self.helper.get_all_voltage()):
                if v != None and v > max_voltage:
                    max_voltage, self.attack_target = v, i
            if self.state0 > 180 or escape == True:
                platform_id = self.helper.get_above_which_platform(self.helper.get_self_position())
                self.transfer_target = self.random_id(platform_id)
                self.state = 1
            elif max_voltage > 90:
                self.state = 2
        #print(self.state)
        #print(self.state)
        if self.state == 0:
            self.state0 += 1
            platform_pos = self.helper.get_platform_position()[self.transfer_target]
            if (platform_pos[0][0]+platform_pos[1][0])/2 < 400:
                platform_mid = (random.randint((platform_pos[0][0]*2+platform_pos[1][0])//3, (platform_pos[0][0] + platform_pos[1][0]*5)//6), platform_pos[0][1])
            elif (platform_pos[0][0]+platform_pos[1][0])/2 > 720:
                platform_mid = (random.randint((platform_pos[0][0]*5 + platform_pos[1][0])//6, (platform_pos[0][0]+platform_pos[1][0]*2)//3), platform_pos[0][1])
            else:
                platform_mid = (random.randint((platform_pos[0][0]*5 + platform_pos[1][0])//6, (platform_pos[0][0] + platform_pos[1][0]*5)//6), platform_pos[0][1])
            return self.helper.walk_to_position(platform_mid)
        elif self.state == 1: # escape from bomb
            self.state0 = 0
            cur_platform_id = self.helper.get_above_which_platform(self.helper.get_self_position())
            if cur_platform_id == self.transfer_target:
                self.state = 0
                return AI_DIR_JUMP
            else:
                platform_pos = self.helper.get_platform_position()[self.transfer_target]
                if (platform_pos[0][0]+platform_pos[1][0])/2 < 400:
                    platform_mid = (random.randint((platform_pos[0][0]*2+platform_pos[1][0])//3, (platform_pos[0][0] + platform_pos[1][0]*5)//6), platform_pos[0][1])
                elif (platform_pos[0][0]+platform_pos[1][0])/2 > 720:
                    platform_mid = (random.randint((platform_pos[0][0]*5 + platform_pos[1][0])//6, (platform_pos[0][0]+platform_pos[1][0]*2)//3), platform_pos[0][1])
                else:
                    platform_mid = (random.randint((platform_pos[0][0]*5 + platform_pos[1][0])//6, (platform_pos[0][0] + platform_pos[1][0]*5)//6), platform_pos[0][1])
                return self.helper.walk_to_position(platform_mid)
        elif self.state == 2: # attack
            self.state0 = 0
            if self.helper.get_other_voltage(self.attack_target) == None or self.helper.get_other_voltage(self.attack_target) < 90:
                self.state = 0
                return AI_DIR_JUMP
            else:
                return self.helper.walk_to_position(self.helper.get_other_position(self.attack_target))
        else:
            return AI_DIR_JUMP

# 1. 躲炸彈 (躲香蕉)
# 2. 如果有對手大於80 自己小於100 衝過去
# 3. 自己電壓超過30 先吃彩虹
# 4. 如果有道具（按照各道具的施放方法丟）
# 5. 想辦法吃道具（去道具偏多的地方）
# 6. 隨便晃晃

        
'''
        if cur_pos[1] > self.lowest_plate() or cur_pos[0] < 0 or cur_pos[0] > 1200:
            #print("Current position:")
            #print(cur_pos)
            #print(cur_pos[0], cur_pos[1])
            #print("Target position:")
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            if cur_pos[0] < 400:
                #print(cur_pos[0] + closest_land_vec[0] + 150, cur_pos[1] + closest_land_vec[1])
                closest_land_pos = (cur_pos[0] + closest_land_vec[0] + 150, cur_pos[1] + closest_land_vec[1])
            elif cur_pos[0] > 800:
                #print(cur_pos[0] + closest_land_vec[0] - 150, cur_pos[1] + closest_land_vec[1])
                closest_land_pos = (cur_pos[0] + closest_land_vec[0] - 150, cur_pos[1] + closest_land_vec[1])
            else:
                closest_land_pos = (cur_pos[0] + closest_land_vec[0], cur_pos[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)
'''