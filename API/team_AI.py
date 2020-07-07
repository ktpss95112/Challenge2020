from API.base import BaseAI

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_ATTACK      = 3
AI_DIR_USE_ITEM    = 4

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
    def decide(self):
        
        my_pos = self.helper.get_self_position()
        my_radius = self.helper.get_self_radius()
        other_pos = self.helper.get_other_position(self.helper.get_nearest_player())
        if self.helper.get_self_keep_item_id() > 0:
            return AI_DIR_USE_ITEM

        if my_pos[0] < 250:
            return AI_DIR_RIGHT
        elif my_pos[0] > 550:
            return AI_DIR_LEFT 

        if other_pos[0] > my_pos[0] and abs(other_pos[0] - my_pos[0]) > 3.5 * my_radius:
            return AI_DIR_RIGHT
        elif other_pos[0] < my_pos[0] and abs(other_pos[0] - my_pos[0]) > 3.5 * my_radius:
            return AI_DIR_LEFT
        elif abs(other_pos[1] - my_pos[1]) > 3.5 * my_radius or other_pos[1] - my_pos[1] == 0:
            return AI_DIR_JUMP
        else:
            return AI_DIR_ATTACK
        
        '''
        print(self.helper.get_self_position())
        print(self.helper.get_self_velocity())
        print(self.helper.get_self_direction())
        print(self.helper.get_self_keep_item_id())
        print(self.helper.get_self_voltage())
        print(self.helper.get_self_radius())
        print(self.helper.get_self_is_invincible())
        print(self.helper.get_self_invincible_time())
        print(self.helper.get_self_uncontrollable_time())
        print(self.helper.get_self_life())
        print(self.helper.get_self_score())
        print(self.helper.get_self_jump_quota())
        print(self.helper.get_self_jump_to_the_highest_time())
        print(self.helper.get_self_can_attack_time())
        
        print(self.helper.get_all_position())
        print(self.helper.get_all_velocity())
        print(self.helper.get_all_direction())
        print(self.helper.get_all_keep_item_id())
        print(self.helper.get_all_voltage())
        print(self.helper.get_all_radius())
        print(self.helper.get_all_is_invincible())
        print(self.helper.get_all_invincible_time())
        print(self.helper.get_all_uncontrollable_time())
        print(self.helper.get_all_life())
        print(self.helper.get_all_score())
        print(self.helper.get_all_jump_quota())
        print(self.helper.get_all_jump_to_the_highest_time())
        print(self.helper.get_all_can_attack_time())
        
        print(self.helper.get_other_position(2))
        print(self.helper.get_other_velocity(2))
        print(self.helper.get_other_direction(2))
        print(self.helper.get_other_keep_item_id(2))
        print(self.helper.get_other_voltage(2))
        print(self.helper.get_other_radius(2))
        print(self.helper.get_other_is_invincible(2))
        print(self.helper.get_other_invincible_time(2))
        print(self.helper.get_other_uncontrollable_time(2))
        print(self.helper.get_other_life(2))
        print(self.helper.get_other_score(2))
        print(self.helper.get_other_jump_quota(2))
        print(self.helper.get_other_jump_to_the_highest_time(2))
        print(self.helper.get_other_can_attack_time(2))
        '''
