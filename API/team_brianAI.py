from API.base import BaseAI
import random

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_LEFT_JUMP   = 3
AI_DIR_RIGHT_JUMP  = 4
AI_DIR_ATTACK      = 5
AI_DIR_USE_ITEM    = 6

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0]
        self.last_position = (0, 0)
        self.stack = [random.randint(0, 4), random.randint(0, 4)]
    
    def decide(self):
     
        if len(self.stack) > 0:
            rt = self.stack[-1]
            self.stack.pop()
            return rt

        my_pos = self.helper.get_self_position()
        my_radius = self.helper.get_self_radius()
        other_pos = self.helper.get_other_position(self.helper.get_nearest_player())

        if self.helper.get_distance(my_pos, other_pos) < self.helper.get_self_attack_radius() / 8 and self.helper.get_self_can_attack_time() == 0:
            return AI_DIR_ATTACK

        lands = self.helper.get_platform_position()
        if self.helper.get_self_keep_item_id() > 0:
            if self.helper.get_self_keep_item_id() == 1:
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 2:
                self.stack.append(AI_DIR_USE_ITEM)
                self.stack.append(AI_DIR_JUMP)
                return AI_DIR_JUMP
            elif self.helper.get_self_keep_item_id() == 3:
                self.stack.append(AI_DIR_LEFT_JUMP)
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 4:
                if abs(other_pos[0] - my_pos[0]) <= 120:
                    return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 5:
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 6:
                return AI_DIR_USE_ITEM
            elif self.helper.get_self_keep_item_id() == 7:
                return AI_DIR_USE_ITEM

        # the area below is empty
        flag = 1
        for platform in lands:
            if platform[0][0] - 10 < my_pos[0] < platform[1][0] + 10:
                flag = 0
        if flag == 1:
            land_pos = self.helper.get_position_vector_to_closest_land()
            if land_pos[0] > 0:
                return AI_DIR_RIGHT_JUMP
            else:
                return AI_DIR_LEFT_JUMP

        if len(self.helper.get_all_big_black_hole_position()) > 0:
            return self.helper.walk_to_position(self.last_position)

        if self.helper.get_self_uncontrollable_time() > 0:
            return AI_DIR_JUMP

        self.last_position = my_pos

        if self.helper.get_distance(my_pos, other_pos) > self.helper.get_self_attack_radius() / 2:
            if other_pos[1] < my_pos[1]:
                if other_pos[0] > my_pos[0]:
                    return AI_DIR_RIGHT_JUMP
                else:
                    return AI_DIR_LEFT_JUMP
            else:
                if other_pos[0] > my_pos[0]:
                    return AI_DIR_RIGHT
                else:
                    return AI_DIR_LEFT
        else:
            return AI_DIR_ATTACK
        
