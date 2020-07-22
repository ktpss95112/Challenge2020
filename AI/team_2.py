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

    def get_nearest_rainbow_position(self):
        a=[]
        position = self.helper.get_all_rainbow_grounder_position()


        for i in range(0,len(position)):
            a.append(self.helper.get_distance(self.helper.get_self_position(), position[i]))

        a=sorted(a)

        for i in range(0,len(position)):

            if (self.helper.get_distance(self.helper.get_self_position(), position[i]))==a[0]:
                return position[i]

    def get_nearest_zap_position(self):
        a=[]
        position = self.helper.get_all_zap_zap_zap_position()


        for i in range(0,len(position)):
            a.append(self.helper.get_distance(self.helper.get_self_position(), position[i]))

        a=sorted(a)

        for i in range(0,len(position)):
            if (self.helper.get_distance(self.helper.get_self_position(), position[i]))==a[0]:
                return position[i]

    def get_nearest_black_hole_position(self):
        a=[]
        position = self.helper.get_all_big_black_hole_position()


        for i in range(0,len(position)):
            a.append(self.helper.get_distance(self.helper.get_self_position(), position[i]))

        a=sorted(a)

        for i in range(0,len(position)):
            if (self.helper.get_distance(self.helper.get_self_position(), position[i]))==a[0]:
                return position[i]

    def get_nearest_bomb_position(self):
        a=[]
        position = self.helper.get_all_cancer_bomb_position()


        for i in range(0,len(position)):
            a.append(self.helper.get_distance(self.helper.get_self_position(), position[i]))

        a=sorted(a)

        for i in range(0,len(position)):
            if (self.helper.get_distance(self.helper.get_self_position(), position[i]))==a[0]:
                return position[i]

    def get_nearest_banana_position(self):
        a=[]
        position = self.helper.get_all_banana_pistol_position()


        for i in range(0,len(position)):
            a.append(self.helper.get_distance(self.helper.get_self_position(), position[i]))

        a=sorted(a)

        for i in range(0,len(position)):
            if (self.helper.get_distance(self.helper.get_self_position(), position[i]))==a[0]:
                return position[i]

    def get_nearest_battery_position(self):
        a=[]
        position = self.helper.get_all_invincible_battery_position()


        for i in range(0,len(position)):
            a.append(self.helper.get_distance(self.helper.get_self_position(), position[i]))

        a=sorted(a)

        for i in range(0,len(position)):
            if (self.helper.get_distance(self.helper.get_self_position(), position[i]))==a[0]:
                return position[i]

    def decide(self):
        if self.helper.get_self_keep_item_id == INVINCIBLE_BATTERY:
            return AI_DIR_USE_ITEM



        # get distance to other player
        distance = self.helper.get_all_player_distance()
        distance.pop(self.helper.get_self_id())


        if self.helper.get_self_keep_item_id == NO_ITEM and self.helper.get_self_voltage()>=50 and len(self.helper.get_all_rainbow_grounder_position()) != 0:
            return self.helper.walk_to_position(self.get_nearest_rainbow_position())

        elif self.helper.get_self_can_attack() and\
            min(d for d in distance if not d is None) < self.helper.get_self_attack_radius():
            return AI_DIR_ATTACK

        elif min(d for d in distance if not d is None) < 0.25 * self.helper.get_self_attack_radius() and not self.helper.get_self_can_attack():
            return AI_DIR_STAY


        elif self.helper.get_self_can_attack() and self.helper.get_above_which_platform(self.helper.get_nearest_player_position())!=-1 and self.helper.get_self_voltage() < self.helper.get_other_voltage(self.helper.get_nearest_player()):
            return self.helper.walk_to_position(self.helper.get_nearest_player_position())

        platform_id = self.helper.get_above_which_platform(self.helper.get_self_position())
        if platform_id == -1:
            pos = self.helper.get_self_position()
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            closest_land_pos = (pos[0] + closest_land_vec[0], pos[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)

        if self.helper.get_self_keep_item_id() not in [0, 6] and self.helper.get_distance(self.helper.get_nearest_player_position(),self.helper.get_self_position())<200:
            return AI_DIR_USE_ITEM
        elif self.helper.get_self_keep_item_id() ==6 :
            return AI_DIR_USE_ITEM
        elif self.helper.item_exists():
            if self.helper.get_self_keep_item_id() != NO_ITEM:
                return AI_DIR_USE_ITEM

            if len(self.helper.get_all_invincible_battery_position())!=0 and self.helper.get_above_which_platform(self.get_nearest_battery_position())!=-1:
                return self.helper.walk_to_position(self.get_nearest_battery_position())

            elif len(self.helper.get_all_big_black_hole_position())!=0 and self.helper.get_above_which_platform(self.get_nearest_black_hole_position())!=-1:
                return self.helper.walk_to_position(self.get_nearest_black_hole_position())

            elif len(self.helper.get_all_zap_zap_zap_velocity())!=0 and self.helper.get_above_which_platform(self.get_nearest_zap_position())!=-1:
                return self.helper.walk_to_position(self.get_nearest_zap_position())

            elif len(self.helper.get_all_banana_pistol_position())!=0 and self.helper.get_above_which_platform(self.get_nearest_banana_position())!=-1:
                return self.helper.walk_to_position(self.get_nearest_banana_position())

            elif len(self.helper.get_all_rainbow_grounder_position())!=0 and self.helper.get_above_which_platform(self.get_nearest_rainbow_position())!=-1:
                return self.helper.walk_to_position(self.get_nearest_rainbow_position())

            elif len(self.helper.get_all_cancer_bomb_position())!=0 and self.helper.get_above_which_platform(self.get_nearest_bomb_position())!=-1:
                return self.helper.walk_to_position(self.get_nearest_bomb_position())

            platform_pos = self.helper.get_platform_position()[platform_id]
            platform_mid = ((platform_pos[0][0] + platform_pos[1][0]) / 2, platform_pos[0][1])
            return self.helper.walk_to_position(platform_mid)

        
