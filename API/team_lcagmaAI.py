from API.base import BaseAI

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_LEFT_JUMP   = 3
AI_DIR_RIGHT_JUMP  = 4
AI_DIR_ATTACK      = 5
AI_DIR_USE_ITEM    = 6
AI_DIR_STAY        = 7

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0]
    
    def decide(self):
        my_index = self.helper.get_self_id()
        my_pos = self.helper.get_self_position()
        my_radius = self.helper.get_self_radius()
        other_index = self.helper.get_nearest_player()
        other_pos = self.helper.get_other_position(other_index)
        stage_index = self.helper.get_game_stage()
        entity_position = self.helper.get_all_entity_position()
        my_land_index = self.helper.get_above_which_land(my_pos)
        platform_position = self.helper.get_platform_position()
        banana_pistol_position = self.helper.get_all_banana_pistol_position()
        banana_peel_position = self.helper.get_all_banana_peel_position()
        bad_position = []
        bad_position.extend(entity_position)
        bad_position.extend(banana_pistol_position)
        bad_position.extend(banana_peel_position)
        
        if self.helper.get_self_keep_item_id() > 0:
            return AI_DIR_USE_ITEM
        
        if stage_index == 0 or stage_index == 2:
            if my_pos[0] < 250:
                return AI_DIR_RIGHT
            elif my_pos[0] > 550:
                return AI_DIR_LEFT
        elif stage_index == 1:
            if my_pos[0] < 50:
                return AI_DIR_RIGHT
            elif my_pos[0] < 550 and my_pos[0] > 400:
                return AI_DIR_RIGHT
            elif my_pos[0] > 200 and my_pos[0] < 400:
                return AI_DIR_LEFT
            elif my_pos[0] > 700:
                return AI_DIR_LEFT
            
        for pos in bad_position:
            if self.helper.get_distance(my_pos, pos) < 2 * my_radius:
                if abs(my_pos[0] - pos[0]) > 1.5 * my_radius:
                    return AI_DIR_JUMP
                elif self.helper.get_distance(my_pos, platform_position[my_land_index][0]) > self.helper.get_distance(my_pos, platform_position[my_land_index][1]):
                    return AI_DIR_LEFT_JUMP
                else:
                    return AI_DIR_RIGHT_JUMP
                
        if other_pos[0] > my_pos[0] and abs(other_pos[0] - my_pos[0]) > 3.5 * my_radius and self.helper.get_self_can_attack():
            return AI_DIR_RIGHT
        elif other_pos[0] < my_pos[0] and abs(other_pos[0] - my_pos[0]) > 3.5 * my_radius and self.helper.get_self_can_attack():
            return AI_DIR_LEFT
        elif abs(other_pos[1] - my_pos[1]) > 3.5 * my_radius or other_pos[1] - my_pos[1] == 0 and self.helper.get_self_can_attack():
            return AI_DIR_JUMP
        elif self.helper.get_self_can_attack():
            return AI_DIR_ATTACK
        else:
            return AI_DIR_JUMP
