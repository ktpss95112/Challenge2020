from API.base import BaseAI

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
    
    def use_item(self):
        item_id = self.helper.get_self_keep_item_id()
        if item_id > 0:
            if item_id == 1:
                pass
            elif item_id == 2:
                pass
            elif item_id == 3:
                pass
            elif item_id == 4:
                pass
            elif item_id == 5:
                return 1
            elif item_id == 6 and self.helper.get_self_voltage() > 10:
                return 1
            elif item_id == 7 and not self.helper.get_self_will_drop():
                return 1
        return 0

    def where_to_go(self, direction):
        if self.helper.get_self_can_jump() and direction[1] < 0 and not self.helper.get_self_will_drop():
            if(direction[0] > 0):
                return AI_DIR_RIGHT_JUMP
            else:
                return AI_DIR_LEFT_JUMP
        else:
            if(direction[0] > 0):
                return AI_DIR_RIGHT
            else:
                return AI_DIR_LEFT

    def to_live(self, direction):
        my_pos = self.helper.get_self_position()
        my_v = self.helper.get_self_velocity()
        my_normal_speed = self.helper.get_self_normal_speed()
        my_jump_speed = self.helper.get_self_jump_speed()
        game_boundary = self.helper.get_game_arena_boundary()
        live_time = 0.75
        future_pos = (my_pos[0] + my_v[0] * live_time, my_pos[1] + my_v[1] * live_time)
        if future_pos[1] > game_boundary[1][1] and self.helper.get_self_can_jump():
            if future_pos[0] < game_boundary[0][0]:
                return AI_DIR_RIGHT_JUMP
            elif future_pos[0] > game_boundary[1][0]:
                return AI_DIR_LEFT_JUMP
        elif future_pos[0] < game_boundary[0][0]:
            return AI_DIR_RIGHT
        elif future_pos[1] < game_boundary[0][1]:
            direction = (direction[0], 0)
        elif future_pos[0] > game_boundary[1][0]:
            return AI_DIR_LEFT
        after_pos = (my_pos[0] + (my_normal_speed * (1 if direction[0] > 0 else -1) + my_v[0]) * live_time, my_pos[1] + (my_jump_speed * (-1 if direction[1] < 0 else 0) + my_v[1]) * live_time)
        if after_pos[1] > game_boundary[1][1] and self.helper.get_self_can_jump():
            if after_pos[0] < game_boundary[0][0]:
                return AI_DIR_RIGHT_JUMP
            elif after_pos[0] > game_boundary[1][0]:
                return AI_DIR_LEFT_JUMP
        elif after_pos[0] < game_boundary[0][0]:
            return AI_DIR_RIGHT
        elif after_pos[1] < game_boundary[0][1]:
            direction = (direction[0], 0)
        elif after_pos[0] > game_boundary[1][0]:
            return AI_DIR_LEFT
        return self.where_to_go(direction)

    def decide(self):
        print(self.use_item())
        if self.use_item(): 
            return AI_DIR_USE_ITEM
        my_id = self.helper.get_self_id()
        my_pos = self.helper.get_self_position()
        my_voltage = self.helper.get_self_voltage()
        enemy_id = self.helper.get_nearest_player()
        enemy_pos = self.helper.get_other_position(enemy_id)
        enemy_dst = self.helper.get_distance(my_pos, enemy_pos)
        voltages = self.helper.get_all_voltage()
        mean_voltage = sum(voltages) / len(voltages)
        if(my_voltage > mean_voltage):
            if(self.helper.get_self_can_attack() and enemy_dst < self.helper.get_self_attack_radius()):
                return AI_DIR_ATTACK
            all_distance = self.helper.get_all_player_distance()
            all_vector = self.helper.get_all_player_vector()
            ideal_vector = (0, 0)
            for i in range(len(all_vector)):
                ideal_vector = (ideal_vector[0] + all_vector[i][0] * all_distance[i],ideal_vector[1] + all_vector[i][1] * all_distance[i])
            ideal_direction = (- ideal_vector[0] / sum(all_distance), - ideal_vector[1] / sum(all_distance))
            return self.to_live(ideal_direction)
        else:
            if(self.helper.get_self_can_attack() and enemy_dst < self.helper.get_self_attack_radius() / 3):
                return AI_DIR_ATTACK
            return self.to_live(self.helper.get_vector(my_pos, enemy_pos))
