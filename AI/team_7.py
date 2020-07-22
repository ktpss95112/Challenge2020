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
        #do nothing if dead
        if self.helper.get_self_life() == 0:
            return AI_DIR_STAY

        platform_id = self.helper.get_above_which_platform(self.helper.get_self_position())

        # get distance to other player
        distance = self.helper.get_all_player_distance()
        distance.pop(self.helper.get_self_id())

        #get gift
        gift = self.helper.get_gift_position()
        if gift is not None:
            return self.helper.walk_to_position(gift)

        #use item as long as you own one
        if self.helper.get_self_keep_item_id() != NO_ITEM:
            return AI_DIR_USE_ITEM

        #attack
        if self.helper.get_self_can_attack() and min(d for d in distance if d is not None) < self.helper.get_self_attack_radius():
            return AI_DIR_ATTACK

        #dodge bomb
        if self.helper.get_nearest_drop_cancer_bomb_position() is not None:
            if self.helper.get_distance(self.helper.get_self_position(), self.helper.get_nearest_drop_cancer_bomb_position()) < (self.helper.get_self_radius() + self.helper.get_cancer_bomb_effect_radius()):
                if self.helper.get_vector(self.helper.get_self_position(), self.helper.get_nearest_drop_cancer_bomb_position())[0] > 0:
                    #move away from the nearest right bomb
                    return AI_DIR_LEFT
                else:
                    #move away from the nearest left bomb
                    return AI_DIR_RIGHT

        #dodge blackhole
        if self.helper.get_nearest_drop_big_black_hole_position() is not None:
            if self.helper.get_distance(self.helper.get_self_position(), self.helper.get_nearest_drop_big_black_hole_position()) < (self.helper.get_self_radius() + self.helper.get_black_hole_effect_radius()):
                if self.helper.get_vector(self.helper.get_self_position(), self.helper.get_nearest_drop_big_black_hole_position())[0] > 0:
                    #move away from the nearest right bomb
                    return AI_DIR_LEFT
                else:
                    #move away from the nearest left bomb
                    return AI_DIR_RIGHT

        # #dodge banana peels
        # if self.helper.get_nearest_drop_banana_peel_position() is not None:
        #     banana_peel = self.helper.get_nearest_drop_banana_peel_position()
        #     if self.helper.get_distance(self.helper.get_self_position(), banana_peel) <= (2 * self.helper.get_self_radius()):
        #         if self.helper.get_self_direction()[0] == -1:
        #             return AI_DIR_LEFT_JUMP
        #         else:
        #             return AI_DIR_RIGHT_JUMP

        #get invincible battery
        if self.helper.get_nearest_specific_item_position(INVINCIBLE_BATTERY) is not None:
            battery_pos = self.helper.get_nearest_specific_item_position(INVINCIBLE_BATTERY)
            return self.helper.walk_to_position(battery_pos)

        #go to rainbow if voltage is high
        if self.helper.get_self_voltage() > 50:
            rainbow = self.helper.get_nearest_specific_item_position(RAINBOW_GROUNDER)
            if rainbow is not None:
                return self.helper.walk_to_position(rainbow)

        if platform_id == -1:
            # go to closest land
            pos = self.helper.get_self_position()
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            closest_land_pos = (pos[0] + closest_land_vec[0], pos[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)
        else:
            #go to highest voltage player
            target_position = self.helper.get_other_position(self.helper.get_highest_voltage_player())
            if self.helper.get_above_which_platform(target_position) == -1:
                return AI_DIR_STAY
            else :
                return self.helper.walk_to_position(target_position)