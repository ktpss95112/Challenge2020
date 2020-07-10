from API.base import BaseAI
import Const

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
    def get_position_vector_to_closest_land(self, position):
        minimum_distance = 10000 ** 2
        distance = 0
        minimum_vector = (10000, 10000)
        vector = (0, 0)
        for platform in self.helper.model.platforms:
            if position[0] > platform.upper_left.x and position[0] < platform.bottom_right.x:
                distance =  abs(position[1] - platform.upper_left.y)
                vector = (0, platform.upper_left.y - position[1])
            else:
                if self.helper.get_distance(position, platform.upper_left) > self.helper.get_distance(position, platform.bottom_right):
                    distance = self.helper.get_distance(position, platform.bottom_right)
                    vector = (platform.bottom_right[0] - position[0], platform.bottom_right[1] - position[1])
                else:
                    distance = self.helper.get_distance(position, platform.upper_left)
                    vector = (platform.upper_left[0] - position[0], platform.upper_left[1] - position[1])
            if distance < minimum_distance:
                minimum_distance = distance
                minimum_vector = vector
        return minimum_vector

    def use_item(self):
        item_id = self.helper.get_self_keep_item_id()
        if item_id > 0:
            if item_id == 1:
                return 1
            elif item_id == 2:
                effect_num = 0
                for i in range(Const.PLAYER_NUM):
                    if Const.BLACK_HOLE_EFFECT_RADIUS > self.helper.get_other_distance(i):
                        effect_num = effect_num + 1
                if effect_num >= 3 or self.helper.get_live_player_num() == 2:
                    return 1
            elif item_id == 3:
                return 1
            elif item_id == 4:
                effect_num = 0
                for i in range(Const.PLAYER_NUM):
                    if Const.ZAP_ZAP_ZAP_RANGE > abs(self.helper.get_other_position(i)[0] - self.helper.get_self_position()[0]):
                        effect_num = effect_num + 1
                if effect_num >= 3 or self.helper.get_live_player_num() == 2:
                    return 1
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

    def to_live(self, direction, enemy_dst, enemy_id):
        g = self.helper.get_game_player_gravity_acceleration()
        my_pos = self.helper.get_self_position()
        my_v = self.helper.get_self_velocity()
        my_normal_speed = self.helper.get_self_normal_speed()
        my_jump_speed = self.helper.get_self_jump_speed()
        game_boundary = self.helper.get_game_arena_boundary()
        live_time = 1
        future_pos = (my_pos[0] + my_v[0] * live_time, my_pos[1] + my_v[1] * live_time - 1/2 * g * live_time ** 2)
        if future_pos[1] > game_boundary[1][1] or self.helper.get_self_will_drop():
            if self.get_position_vector_to_closest_land(future_pos)[0] > -2:
                if self.helper.get_self_can_jump():
                    return AI_DIR_RIGHT_JUMP
                else:
                    return AI_DIR_RIGHT
            elif self.get_position_vector_to_closest_land(future_pos)[0] < -2:
                if self.helper.get_self_can_jump():
                    return AI_DIR_LEFT_JUMP
                else:
                    return AI_DIR_LEFT
        elif future_pos[0] < game_boundary[0][0]:
            return AI_DIR_RIGHT
        elif future_pos[1] < game_boundary[0][1]:
            direction = (direction[0], 0)
        elif future_pos[0] > game_boundary[1][0]:
            return AI_DIR_LEFT
        after_pos = (my_pos[0] + (my_normal_speed * (1 if direction[0] > 0 else -1) + my_v[0]) * live_time, my_pos[1] + (my_jump_speed * (-1 if direction[1] < 0 else 0) + my_v[1]) * live_time - 1/2 * g * live_time ** 2)
        if after_pos[1] > game_boundary[1][1] or self.helper.get_self_will_drop():
            if self.get_position_vector_to_closest_land(after_pos)[0] > 0:
                if self.helper.get_self_can_jump():
                    return AI_DIR_RIGHT_JUMP
                else:
                    return AI_DIR_RIGHT
            elif self.get_position_vector_to_closest_land(after_pos)[0] < 0:
                if self.helper.get_self_can_jump():
                    return AI_DIR_LEFT_JUMP
                else:
                    return AI_DIR_LEFT
        elif after_pos[0] < game_boundary[0][0]:
            return AI_DIR_RIGHT
        elif after_pos[1] < game_boundary[0][1]:
            direction = (direction[0], 0)
        elif after_pos[0] > game_boundary[1][0]:
            return AI_DIR_LEFT
        all_bomb = self.helper.get_all_drop_cancer_bomb_position()
        vector = (0, 0)
        for bomb in all_bomb:
            bomb_vector = self.helper.get_vector(self.helper.get_self_position(), bomb)
            vector = (vector[0] + bomb_vector[0], vector[1] + bomb_vector[1])
        if len(all_bomb) != 0:
            vector = (-vector[0] / len(all_bomb), 0)
            direction = vector
        if(self.helper.get_self_can_attack() and enemy_dst < self.helper.get_self_attack_radius() / 3 and not self.helper.get_other_is_invincible(enemy_id)):
            return AI_DIR_ATTACK
        return self.where_to_go(direction)

    def decide(self):
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
        if(my_voltage > mean_voltage * 1.5) and self.helper.get_live_player_num() > 2:
            '''
            all_distance = self.helper.get_all_player_distance()
            all_vector = self.helper.get_all_player_vector()
            ideal_vector = (0, 0)
            for i in range(len(all_vector)):
                ideal_vector = (ideal_vector[0] + all_vector[i][0] * all_distance[i],ideal_vector[1] + all_vector[i][1] * all_distance[i])
            ideal_direction = (- ideal_vector[0] / sum(all_distance), - ideal_vector[1] / sum(all_distance))
            '''
            return self.to_live((-self.helper.get_vector(my_pos, enemy_pos)[0], -self.helper.get_vector(my_pos, enemy_pos)[1]), enemy_dst, enemy_id)
        else:
            return self.to_live(self.helper.get_vector(my_pos, enemy_pos), enemy_dst, enemy_id)
