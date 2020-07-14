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
        if self.helper.get_self_keep_item_id() != NO_ITEM:
            return AI_DIR_USE_ITEM

        # get distance to other player
        distance = self.helper.get_all_player_distance()
        distance.pop(self.helper.get_self_id())
        
        if self.helper.get_self_can_attack() and\
            min(distance) < self.helper.get_self_attack_radius():
            return AI_DIR_ATTACK

        platform_id = self.helper.get_above_which_land(self.helper.get_self_position())
        if platform_id != -1:
            # go to middle of the platform
            platform_pos = self.helper.get_platform_position()[platform_id]
            platform_mid = ((platform_pos[0][0] + platform_pos[1][0]) / 2,\
                            (platform_pos[0][1] + platform_pos[1][1]) / 2)
            return self.helper.walk_to_position(platform_mid)
        else:
            # go to closest land
            pos = self.helper.get_self_position()
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            closest_land_pos = (pos[0] + closest_land_vec[0], pos[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)

