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

    def decide(self):
        # get information
        self_position = self.helper.get_self_position()
        others_position = self.helper.get_other_position(self.helper.get_nearest_player())
        distance = self.helper.get_all_player_distance()
        distance.pop(self.helper.get_self_id())
        my_item = self.helper.get_self_keep_item_id()
        attack_radius = self.helper.get_self_attack_radius()


        platform_id = self.helper.get_above_which_platform(self.helper.get_self_position())
        if platform_id == -1:
            # go to closest land
            pos = self.helper.get_self_position()
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            closest_land_pos = (pos[0] + closest_land_vec[0], pos[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)
        


        if self.helper.get_self_can_attack() and\
            min(d for d in distance if not d is None) < self.helper.get_self_attack_radius() / 2:
            return AI_DIR_ATTACK
    
        #遠離毒瘤炸彈
        boom = None
        cancer_bomb = self.helper.get_all_drop_cancer_bomb_position()
        cancer_bomb_time = self.helper.get_all_drop_cancer_bomb_position()
        cancer_bomb_effect = self.helper.get_cancer_bomb_effect_radius()
        cancer_bomb_position = None
        for i in range(len(cancer_bomb) - 1):
            if cancer_bomb_time[i] < cancer_bomb_time[i+1]:
                boom = cancer_bomb_time[i]
                cancer_bomb_position = cancer_bomb[i]
        if cancer_bomb_position != None and abs(self_position[0] - cancer_bomb_position[0]) <= cancer_bomb_effect:
            if self_position[0] > cancer_bomb_position[0]:
                return AI_DIR_RIGHT
            else:
                return AI_DIR_LEFT
        if cancer_bomb_position != None and abs(self_position[1] - cancer_bomb_position[1]) <= cancer_bomb_effect:
            if self_position[1] > cancer_bomb_position[1]:
                return AI_DIR_JUMP

        '''
        #躲蕉蕉皮
        banana_peels = self.helper.get_all_banana_peel_position()
        safe_distance = self.helper.get_self_radius()
        for peel in banana_peels:
            if abs(peel[0] - self_position[0]) and abs(peel[1] - self_position[1]) <  safe_distance :
                if (peel[0] - self_position[0]) > 0:
                    return AI_DIR_LEFT_JUMP
                else :
                    return AI_DIR_RIGHT_JUMP
        '''
        
        # Use item
        if my_item == BIG_BLACK_HOLE:
            black_hole_effect_radius = self.helper.get_black_hole_effect_radius()
            if self.helper.get_distance(self_position, others_position) <= black_hole_effect_radius:
                return AI_DIR_USE_ITEM
        
        elif my_item == CANCER_BOMB:
            #放毒瘤炸彈
            nearest_player_position = self.helper.get_nearest_player_position()
            if nearest_player_position == None:
                return AI_DIR_USE_ITEM
            if abs(nearest_player_position[0] - self_position[0]) <= cancer_bomb_effect / 2:
                return AI_DIR_USE_ITEM
            elif self_position[0] > nearest_player_position[0]:
                return self.helper.walk_to_position((nearest_player_position[0] + cancer_bomb_effect/2, nearest_player_position[1]))
            else:
                return self.helper.walk_to_position((nearest_player_position[0] - cancer_bomb_effect/2, nearest_player_position[1]))

        elif my_item in [ 1, 4, 5 ]:
            if abs(self.helper.get_nearest_player_position()[1] - self_position[1]) > attack_radius:
                return self.move(self.helper.get_nearest_player_position)
            elif self.helper.get_self_direction()[0] * ( self.helper.get_nearest_player_position()[0] - self_position[0] ) > 0 :
                return AI_DIR_USE_ITEM
            elif self.helper.get_nearest_player_position()[0] - self_position[0] :
                return AI_DIR_RIGHT
            elif self.helper.get_nearest_player_position()[0] - self_position[0] :
                return AI_DIR_LEFT

        elif my_item != NO_ITEM:
            return AI_DIR_USE_ITEM
        

        #躲黑洞閃電
        other_item = self.helper.get_all_keep_item_id()
        other_item.pop(self.helper.get_self_id())
        my_item = self.helper.get_self_keep_item_id()
        self_position = self.helper.get_self_position()
        other_position = self.helper.get_all_position()
        other_position.pop(self.helper.get_self_id())
        for i in range(3):
            if other_position[i] == None:
                continue
            if 2 in other_item or 4 in other_item :
                if (other_position[i][0] - self_position[0]) > 0:
                    return AI_DIR_LEFT
                else :
                    return AI_DIR_RIGHT

        # Pick item
        if my_item == 0:
            nearest_battery = self.helper.get_nearest_specific_item_position(INVINCIBLE_BATTERY)
            if nearest_battery != None and self.helper.get_above_which_platform(nearest_battery) != -1:
                return self.helper.walk_to_position(nearest_battery)
            
            nearest_grounder = self.helper.get_nearest_specific_item_position(RAINBOW_GROUNDER)
            if nearest_grounder != None and self.helper.get_above_which_platform(nearest_grounder) != -1:
                return self.helper.walk_to_position(nearest_grounder)

            nearest_zap_zap_zap = self.helper.get_nearest_specific_item_position(ZAP_ZAP_ZAP)
            if nearest_zap_zap_zap != None and self.helper.get_above_which_platform(nearest_zap_zap_zap) != -1:
                return self.helper.walk_to_position(nearest_zap_zap_zap)

            nearest_banana_pistol = self.helper.get_nearest_specific_item_position(1) # banana pistol
            if nearest_banana_pistol != None and self.helper.get_above_which_platform(nearest_banana_pistol) != -1:
                return self.helper.walk_to_position(nearest_banana_pistol)

            nearest_banana_peel = self.helper.get_nearest_specific_item_position(5) # bananan peel
            if nearest_banana_peel != None and self.helper.get_above_which_platform(nearest_banana_peel) != -1:
                return self.helper.walk_to_position(nearest_banana_peel)

    
        # if self.helper.get_self_can_attack() and\
        # min(d for d in distance if not d is None) < self.helper.get_self_attack_radius()/2:
        #     return AI_DIR_USE_ITEM

        highest_voltageget = self.helper.get_highest_voltage_player()
        highest_voltageget_position = self.helper.get_other_position(highest_voltageget)
        others_voltageget = self.helper.get_other_voltage(highest_voltageget)
        if others_voltageget >=  100 and self.helper.get_other_have_platform_below(highest_voltageget):
            #attack the highest player
            return self.helper.walk_to_position(highest_voltageget_position)
        else:
            # attack the nearest player
            nearest_player = self.helper.get_nearest_player()
            nearest_player_position = self.helper.get_nearest_player_position()
            nearest_player = self.helper.get_nearest_player()
            nearest_player_position = self.helper.get_nearest_player_position()
            if self.helper.get_self_can_attack() and self.helper.get_other_have_platform_below(nearest_player):
                return self.helper.walk_to_position(nearest_player_position)


        platform_id = self.helper.get_above_which_platform(self.helper.get_self_position())
        if platform_id != -1:
            # go to middle of the platform
            platform_pos = self.helper.get_platform_position()[platform_id]
            platform_mid = ((platform_pos[0][0] + platform_pos[1][0]) / 2, platform_pos[0][1])
            return self.helper.walk_to_position(platform_mid)
        else:
            # go to closest land
            pos = self.helper.get_self_position()
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            closest_land_pos = (pos[0] + closest_land_vec[0], pos[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)
            # get_all_player_distance()　and get_all_player_position

        #如果球球靠近死亡邊緣，讓球球遠離他
        game_arena = self.helper.get_game_arena_boundary()
        self_position = self.helper.get_self_position()
        #左右
        if abs(self_position[0] - game_arena[0][0]) <= (game_arena[1][0] - game_arena[0][0])/20 or abs(self_position[0] - game_arena[1][0]) <= (game_arena[1][0] - game_arena[0][0])/20:
            if self_position[0] > (game_arena[0][0] + game_arena[1][0]/2):
                return AI_DIR_LEFT
            else:
                return AI_DIR_RIGHT
        #上下
        if abs(self_position[1] - game_arena[0][1]) <= ((game_arena[1][1] - game_arena[0][1])/10) or abs(self_position[1] - game_arena[1][1]) <= ((game_arena[1][1] - game_arena[0][1])/10):
            if self_position[1] < game_arena[1][1]:
                return AI_DIR_JUMP

    def move(self, position):
        '''
        for i in range (4) :
            if i == self.helper.get_self_id() :
                continue
            else self.helper.get_other_position(i) == self.helper.get_nearest_player_position() :
                py_id = i
        '''
        py_id = self.helper.get_nearest_player()
        platform_id = self.helper.get_above_which_platform(self.helper.get_self_position())
        position = self.helper.get_self_position()
        if platform_id == -1:
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            closest_land_pos = (position[0] + closest_land_vec[0], position[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)
        if self.helper.get_distance(position, self.helper.get_nearest_player_position()) < self.helper.get_other_attack_radius(py_id)/8:
            if self.helper.get_nearest_player_position()[0] - self.helper.get_self_position()[0] > 0:
                return AI_DIR_LEFT
            else:
                return AI_DIR_RIGHT

