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

        my_id = self.helper.get_self_id()
        my_pos = self.helper.get_self_position()
        position = (0,0)
        max = 0
        max_id = 0
        platform_id = self.helper.get_above_which_platform(self.helper.get_self_position())
        if my_pos[1] > 750:
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
        for i in range(4):
            if i != my_id:
                if self.helper.get_other_life(i) == 5:
                    position = self.helper.get_other_position(i)
                    max_id = i
                    break
                elif self.helper.get_other_voltage(i)!=None and self.helper.get_other_voltage(i) >= max:
                    position = self.helper.get_other_position(i)
                    max = self.helper.get_other_voltage(i)
                    max_id = i
        # get distance to other player
        distance = self.helper.get_all_player_distance()
        min = 100000
        min_id = 0
        for i in range(4):
            if distance[i] == None:
                    continue
            if i != my_id and distance[i] <= min:
                    position = self.helper.get_other_position(i)
                    min = self.helper.get_other_voltage(i)
                    min_id = i

        if my_pos[1] < -500:
            return 0 if my_pos[0] > 520 else 1
        if self.helper.get_self_can_attack() and\
            distance[min_id] < self.helper.get_self_attack_radius()*10/13:
            return AI_DIR_ATTACK

        if self.helper.get_nearest_drop_banana_peel_position() != None and my_pos != None:
            if self.helper.get_distance(self.helper.get_nearest_drop_banana_peel_position(), my_pos) < 100:
                return 3 if my_pos[0] > 520 else 4
        if self.helper.get_nearest_specific_item_position(7)!=None and self.helper.get_nearest_specific_item_position(7)[1]<630:
            return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(7))
        elif (self.helper.get_self_can_attack() and not (self.helper.get_other_is_invincible(max_id))) or self.helper.get_self_voltage()<65 or (self.helper.get_self_is_invincible() and self.helper.get_self_invincible_time()>0.5):
            return self.helper.walk_to_position( (position[0], position[1]) )
        elif self.helper.get_nearest_specific_item_position(6)!=None and self.helper.get_nearest_specific_item_position(6)[1]<630:
            return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(6))
        
        enemy_radius = self.helper.get_other_attack_radius( min_id )
        enemy_dis = self.helper.get_distance( self.helper.get_other_position(min_id) , my_pos )
        if enemy_dis < (enemy_radius*4/9):
            enemy_vector = self.helper.get_vector( self.helper.get_other_position(min_id) , my_pos )
            move_vector = ( enemy_vector[0] + (50 if my_pos[0] > 520 else -50) , enemy_vector[1] - 1000 )
            return self.helper.walk_to_position( (my_pos[0] + move_vector[0] , my_pos[1] + move_vector[1]) )

        if self.helper.get_nearest_drop_cancer_bomb_position() != None:
            bomb_radius = self.helper.get_cancer_bomb_effect_radius()
            bomb_dis = self.helper.get_distance( self.helper.get_nearest_drop_cancer_bomb_position() , my_pos )
            if bomb_dis < bomb_radius:
                bomb_vector = self.helper.get_vector( self.helper.get_nearest_drop_cancer_bomb_position() , my_pos )
                move_vector = ( bomb_vector[0] + (50 if my_pos[0] > 520 else -50) , bomb_vector[1] - (1000 if my_pos[1] > 50 else -1000) )
                return self.helper.walk_to_position( (my_pos[0] + move_vector[0] , my_pos[1] + move_vector[1]) )

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

            #https://drive.google.com/drive/folders/17nqJ5Bkl2Qk2rKe6BFIhnAmXepESdRiL?fbclid=IwAR3HUrhC3c0Jt1M33Vq3xF8pYie1lUlqLhX0Tiz31gJ8P8JS1C2fBSxmUYQ
