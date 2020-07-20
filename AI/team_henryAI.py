

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_LEFT_JUMP   = 3
AI_DIR_RIGHT_JUMP  = 4
AI_DIR_ATTACK      = 5
AI_DIR_USE_ITEM    = 6
AI_DIR_STAY        = 7

PLAYER_RADIUS = 25
ATTACK_RADIUS = 12 * PLAYER_RADIUS

NO_ITEM = 0
BANANA_PISTOL = 1
BIG_BLACK_HOLE = 2
CANCER_BOMB = 3
ZAP_ZAP_ZAP = 4
BANANA_PEEL = 5
RAINBOW_GROUNDER = 6
INVINCIBLE_BATTERY = 7

X_OFFSET = 34.5
Y_OFFSET = 31.85

class TeamAI:
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0, 0]
        self.searching_item = False

    def in_the_map(self, position):
        if position[1] < 603 + Y_OFFSET and position[0] >= 0 + X_OFFSET and position[0] <= 1132 + X_OFFSET:
            return True
        return False

    def avoid_entity(self):
        if self.helper.get_nearest_drop_banana_peel_position() != None and abs(self.helper.get_self_position()[0] + self.helper.get_self_velocity()[0] * 0.15 - self.helper.get_nearest_drop_banana_peel_position()[0]) < 10 and abs(self.helper.get_self_position()[1] + self.helper.get_self_velocity()[1] * 0.15 - self.helper.get_nearest_drop_banana_peel_position()[1]) < 10:
            return True
        return False
        
    def decide(self):
        self_position = self.helper.get_self_position()
        target_player_position = self.helper.get_other_position(self.helper.get_nearest_player())
        nearest_item_position = self.helper.get_nearest_item_position()
        '''
        if self.avoid_entity():
            return AI_DIR_JUMP
        '''
        if self.helper.get_other_voltage(self.helper.get_highest_voltage_player()) >= 100 and self.in_the_map(self.helper.get_other_position(self.helper.get_highest_voltage_player())):
            target_player_position = self.helper.get_other_position(self.helper.get_highest_voltage_player())
        if self.helper.get_distance(self_position , target_player_position) <= ATTACK_RADIUS and self.helper.get_self_can_attack_time() == 0:
            self.searching_item = True
            return AI_DIR_ATTACK
        elif self.helper.get_self_keep_item_id() != NO_ITEM:
            if self.helper.get_self_can_attack_time() <= 0.2:
                self.searching_item = False
            return AI_DIR_USE_ITEM
        elif self.in_the_map(target_player_position) and self.helper.get_self_can_attack_time() <= 0.2 and not self.searching_item:
            return self.helper.walk_to_position(target_player_position)
        elif nearest_item_position != None and self.in_the_map(nearest_item_position):
            if self.helper.get_nearest_specific_item_position(7) != None:
                return  self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(7))
            elif self.helper.get_nearest_specific_item_position(6) != None:
                return  self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(6))
            elif self.helper.item_exists():
                return self.helper.walk_to_position(self.helper.get_nearest_item_position())
                
        platform_id = self.helper.get_above_which_platform(self.helper.get_self_position())
        if platform_id != -1:
            # go to middle of the platform
            platform_pos = self.helper.get_platform_position()[platform_id]
            platform_mid = ((platform_pos[0][0] + platform_pos[1][0]) / 2,\
                            (platform_pos[0][1]))
            return self.helper.walk_to_position(platform_mid)
        else:
            # go to closest land
            pos = self.helper.get_self_position()
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            closest_land_pos = (pos[0] + closest_land_vec[0], pos[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)

        # add your code