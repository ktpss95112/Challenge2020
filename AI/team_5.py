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
GIFT               = 8

# Const
SIDE = 30

class TeamAI:
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0, 0]
        self.zap = True # if I put a zapzapzap there. self.zap = False
        self.zap_position_x = 0

    def sign(self, number: int):
        return 1 if number >= 0 else -1

    def decide(self):

        distance = self.helper.get_all_player_distance()
        distance.pop(self.helper.get_self_id())

        if self.helper.get_self_is_invincible() == True:

            I_p = self.helper.get_self_position()
            nearest = self.helper.get_nearest_player()
            nearest_p = self.helper.get_other_position(nearest)

            if self.helper.get_self_voltage() > 40:
                if self.helper.get_self_invincible_time() <= 3:
                    return self.helper.walk_to_position(nearest_p)
                else:
                    if nearest_p[0] <= I_p[0]:
                        return AI_DIR_RIGHT
                    else:
                        return AI_DIR_LEFT
            else:
                if self.helper.get_self_can_attack() and\
                    min(d for d in distance if not d is None) < self.helper.get_self_attack_radius():
                    return AI_DIR_ATTACK
                else:
                    return self.helper.walk_to_position(nearest_p)
        '''
        if self.zap == False:
            pos = self.helper.get_self_position()
            life_boundary = self.helper.get_game_life_boundary()
            if pos < self.zap_position_x - self.helper.get_zap_zap_zap_effect_range() or pos > self.zap_position_x + self.helper.get_zap_zap_zap_effect_range():
                self.zap = True
            elif (pos - self.zap_position_x) > 0 and self.zap_position_x - self.helper.get_zap_zap_zap_effect_range() > life_boundary[0][0]:
                return AI_DIR_LEFT
            else:
                return AI_DIR_RIGHT
        '''

        # ITEM USAGE
        if self.helper.get_self_keep_item_id() != NO_ITEM:
            if self.helper.get_self_keep_item_id() == BANANA_PISTOL:
                my_position = self.helper.get_self_position()
                opponent_position = self.helper.get_all_position()
                opponent_radius = self.helper.get_all_radius()

                opponent_position.pop(self.helper.get_self_id())
                opponent_radius.pop(self.helper.get_self_id())
                self_speed = self.helper.get_self_velocity()

                for position, radius in zip(opponent_position, opponent_radius):

                # if opponent is reachable in y direction
                    if position == None:
                        continue

                    if position[1] - radius  <= my_position[1] <= position[1] + radius:

                        # if
                        if sign(self.helper.get_self_direction()[0]) == sign(position - my_position[0]):
                            return AI_DIR_USE_ITEM
                        else:
                            return AI_DIR_RIGHT if sign(position - my_position[0]) == 1 else AI_DIR_LEFT
                    else:
                        if self_speed[1] > -50:
                            return AI_DIR_JUMP
                        else:
                            my_position = self.helper.get_self_position()
                            platform_id = self.helper.get_above_which_platform(my_position)
                            platform_pos = self.helper.get_platform_position()[platform_id]
                            platform_mid = ((platform_pos[0][0] + platform_pos[1][0]) / 2, platform_pos[0][1])
                            return self.helper.walk_to_position(platform_mid)
            elif self.helper.get_self_keep_item_id() == BIG_BLACK_HOLE:
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == RAINBOW_GROUNDER:
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == INVINCIBLE_BATTERY:
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == BANANA_PEEL:
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == ZAP_ZAP_ZAP:
                all_AI_position = self.helper.get_all_position()
                all_AI_position.pop(self.helper.get_self_id())
                self.a = True
                for i in range(3):
                    if all_AI_position[i] == None:
                        continue
                    pos = self.helper.get_self_position()
                    closest_land_vec = self.helper.get_position_vector_to_closest_land()
                    if all_AI_position[i][0] <= pos[0] + self.helper.get_zap_zap_zap_effect_range() and all_AI_position[i][0] >= pos[0] - self.helper.get_zap_zap_zap_effect_range():
                        #print("NO")
                        self.a = False
                        self.zap_position_x = pos[0]
                        return AI_DIR_USE_ITEM
                if self.a:
                    nearest_distance_AI = self.helper.get_other_position(self.helper.get_nearest_player())
                    if abs(nearest_distance_AI[0]+self.helper.get_zap_zap_zap_effect_range()-pos[0]) < abs(nearest_distance_AI[0]-self.helper.get_zap_zap_zap_effect_range()-pos[0]):
                        destination = nearest_distance_AI[0]+self.helper.get_zap_zap_zap_effect_range(), pos[1] + closest_land_vec[1]
                    else:
                        destination = nearest_distance_AI[0]-self.helper.get_zap_zap_zap_effect_range(), pos[1] + closest_land_vec[1]
                    #print("Ya")
                    return self.helper.walk_to_position(destination)
            elif self.helper.get_self_keep_item_id() == CANCER_BOMB:
                # It's said that it would work like ZAP_ZAP_ZAP
                return AI_DIR_USE_ITEM
            else:
                return AI_DIR_USE_ITEM

        # WALK TO THE CLOEST LAND

        # get distance to other player

        if self.helper.get_self_can_attack() and\
            min(d for d in distance if not d is None) < self.helper.get_self_attack_radius():
            return AI_DIR_ATTACK

        player_id = self.helper.get_nearest_player()
        platform_id = self.helper.get_above_which_platform(self.helper.get_self_position())

        if self.helper.get_self_voltage() + 35 < self.helper.get_other_voltage(player_id) and\
        self.helper.get_other_keep_item_id(player_id) != ZAP_ZAP_ZAP and\
        self.helper.get_other_keep_item_id(player_id) != INVINCIBLE_BATTERY and\
        self.helper.get_other_is_invincible(player_id) == False:
            return self.helper.walk_to_position(self.helper.get_other_position(player_id))

        items_pos = []
        for i in range(1, 9):
            items_pos.append(self.helper.get_nearest_specific_item_position(i))

        self_pos = self.helper.get_self_position()


        SOME_DISTANCE = 15 * self.helper.get_self_radius()               # should be modified


        if items_pos[ZAP_ZAP_ZAP] != None and self.helper.get_distance(self_pos, items_pos[ZAP_ZAP_ZAP]) < SOME_DISTANCE:
            return self.helper.walk_to_position(items_pos[ZAP_ZAP_ZAP])
        elif items_pos[INVINCIBLE_BATTERY] != None and self.helper.get_distance(self_pos, items_pos[INVINCIBLE_BATTERY]) < SOME_DISTANCE:
            return self.helper.walk_to_position(items_pos[INVINCIBLE_BATTERY])
        elif items_pos[RAINBOW_GROUNDER] != None and self.helper.get_distance(self_pos, items_pos[RAINBOW_GROUNDER]) < SOME_DISTANCE and self.helper.get_self_voltage() >= 25:
            return self.helper.walk_to_position(items_pos[RAINBOW_GROUNDER])
        elif items_pos[CANCER_BOMB] != None and self.helper.get_distance(self_pos, items_pos[CANCER_BOMB]) < SOME_DISTANCE:
            return self.helper.walk_to_position(items_pos[CANCER_BOMB])
        elif items_pos[BIG_BLACK_HOLE] != None and self.helper.get_distance(self_pos, items_pos[BIG_BLACK_HOLE]) < SOME_DISTANCE:
            return self.helper.walk_to_position(items_pos[BIG_BLACK_HOLE])


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
