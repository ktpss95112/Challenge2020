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
        platform_id = self.helper.get_above_which_platform(self.helper.get_self_position())
        if platform_id == -1:
            # go to closest land
            pos = self.helper.get_self_position()
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            closest_land_pos = (pos[0] + closest_land_vec[0], pos[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)
        

        item_id = self.helper.get_self_keep_item_id()
        distance = [i for i in self.helper.get_all_player_distance() if i is not None and i != 0]
        vector = [i for i in self.helper.get_all_player_vector() if i is not None and not (i[0] == 0 and i[1] == 0)]

        if self.helper.get_self_invincible_time() > 1:
            a = [distance[i] for i in range(len(distance)) if vector[i][0] != 0 or vector[i][1] != 0]
            if len(a) > 0 and self.helper.get_self_can_attack() and \
                min(a) < self.helper.get_self_attack_radius() * 2 / 3:
                return AI_DIR_ATTACK
        
        # use item
        if item_id != NO_ITEM:
            if item_id == BANANA_PISTOL:
                for i in vector:
                    if i[0] != 0 and i[1] == 0 and i[0] * self.helper.get_self_direction()[0] < 0:
                        return AI_DIR_USE_ITEM
            if item_id == ZAP_ZAP_ZAP:
                for i in vector:
                    if not (i[0] == 0 and i[1] == 0) and abs(i[0]) <= self.helper.get_zap_zap_zap_effect_range() * 2 / 3:
                        return AI_DIR_USE_ITEM
                else:
                    if self.helper.get_nearest_player() != None:
                        return self.helper.walk_to_position(self.helper.get_other_position(self.helper.get_nearest_player()))
            else:
                return AI_DIR_USE_ITEM

        a = [distance[i] for i in range(len(distance)) if vector[i][0] != 0 or vector[i][1] != 0]
        if len(a) > 0 and self.helper.get_self_can_attack() and \
            min(a) < self.helper.get_self_attack_radius() * 2 / 3:
            return AI_DIR_ATTACK

        # find nearest invincible battery
        b = self.helper.get_nearest_specific_item_position(INVINCIBLE_BATTERY)
        if b != None and self.helper.get_above_which_platform(b) != -1: 
            return self.helper.walk_to_position(b)
        
        # find nearest rainbow grounder
        b = self.helper.get_nearest_specific_item_position(RAINBOW_GROUNDER)
        if b != None and self.helper.get_above_which_platform(b) != -1:
            return self.helper.walk_to_position(b)

        # hit others
        b = self.helper.get_highest_voltage_player()
        if b != None:
            if self.helper.get_all_player_distance()[b] != 0 and (self.helper.get_other_voltage(b) > self.helper.get_self_voltage() \
                or abs(self.helper.get_other_position(b)[0] - 566) > abs(self.helper.get_self_position()[0] - 566)):
                return self.hit_player(b)

        # find nearest item / (no zap_zap_zap)    
        platform_id = self.helper.get_above_which_platform(self.helper.get_self_position())
        if platform_id != -1:
            # go to middle of the platform
            platform_pos = self.helper.get_platform_position()[platform_id]
            platform_mid = ((platform_pos[0][0] + platform_pos[1][0]) * 0.5, platform_pos[0][1])
            d = self.helper.get_distance(platform_mid, self.helper.get_self_position())
            return self.helper.walk_to_position(platform_mid)
        else:
            # go to closest land
            pos = self.helper.get_self_position()
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            closest_land_pos = (pos[0] + closest_land_vec[0], pos[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)

    def hit_player(self, id):
        p = self.helper.get_other_position(id)
        n = (p[0] + self.helper.get_self_radius() * 2 if p[0] < 566 else p[0] - self.helper.get_self_radius() * 2, p[1] + 30)
        if self.helper.get_above_which_platform(n) != -1:
            return self.helper.walk_to_position(n)
        return AI_DIR_JUMP