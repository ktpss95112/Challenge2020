from API.base import BaseAI
import Const

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_LEFT_JUMP   = 3
AI_DIR_RIGHT_JUMP  = 4
AI_DIR_ATTACK      = 5
AI_DIR_USE_ITEM    = 6
AI_DIR_STAY        = 7
AI_DIR_NOT_JUMP    = 8

def tuple_plus(a, b):
    return (a[0] + b[0], a[1] + b[1])

def tuple_minus(a, b):
    return (a[0] - b[0], a[1] - b[1])

def tuple_times(a, b):
    return (a[0] * b, a[1] * b)

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0, 0]
        self.mode = []

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
        factor = 0
        if item_id > 0:
            if item_id == 1:
                factor = 1
            elif item_id == 2:
                effect_num = 0
                for i in range(Const.PLAYER_NUM):
                    if Const.BLACK_HOLE_EFFECT_RADIUS > self.helper.get_other_player_distance(i):
                        effect_num = effect_num + 1
                if effect_num >= 3 or self.helper.get_live_player_num() == 2:
                    factor = 1
            elif item_id == 3:
                effect_num = 0
                for i in range(Const.PLAYER_NUM):
                    if Const.BOMB_EXPLODE_RADIUS > self.helper.get_other_player_distance(i):
                        effect_num = effect_num + 1
                if effect_num >= 3 or self.helper.get_live_player_num() == 2:
                    factor = 1
            elif item_id == 4:
                effect_num = 0
                for i in range(Const.PLAYER_NUM):
                    if Const.ZAP_ZAP_ZAP_RANGE > abs(self.helper.get_other_position(i)[0] - self.helper.get_self_position()[0]):
                        effect_num = effect_num + 1
                if effect_num >= 3 or self.helper.get_live_player_num() == 2:
                    factor = 1
            elif item_id == 5:
                factor = 1
            elif item_id == 6 and self.helper.get_self_voltage() > 10:
                factor = 1
            elif item_id == 7 and not self.helper.get_self_will_drop():
                factor = 1
        return AI_DIR_USE_ITEM if factor else -1

    def can_jump(self):
        return self.helper.get_self_jump_to_the_highest_time() < 0.02 and self.helper.get_self_can_jump()

    def where_to_go(self, direction):
        if direction == (0, 0):
            return -1
        if self.can_jump() and direction[1] < 0:
            if direction[0] > 0:
                return AI_DIR_RIGHT_JUMP
            elif direction[0] < 0:
                return AI_DIR_LEFT_JUMP
            else:
                return AI_DIR_JUMP
        else:
            if(direction[0] > 0):
                return AI_DIR_RIGHT
            elif(direction[0] < 0):
                return AI_DIR_LEFT
            else:
                return AI_DIR_STAY

    def judge_direction(self, direction):
        g = self.helper.get_game_gravity_acceleration()
        my_pos = self.helper.get_self_position()
        my_v = self.helper.get_self_velocity()
        my_normal_speed = self.helper.get_self_normal_speed()
        my_jump_speed = self.helper.get_self_jump_speed()
        game_boundary = self.helper.get_game_arena_boundary()
        live_time = 0.15
        after_pos = (my_pos[0] + (my_normal_speed * (1 if direction[0] > 0 else -1) + my_v[0]) * live_time, my_pos[1] + (my_jump_speed * (-1 if direction[1] < 0 else 0) + my_v[1]) * live_time + 1/2 * g * live_time ** 2)
        if after_pos[1] > game_boundary[1][1] or self.helper.get_position_will_drop(after_pos) or my_pos[0] < game_boundary[0][0] or my_pos[0] > game_boundary[1][0]:
            return (0, 0)
        else:
            return direction

    def to_live(self):
        g = self.helper.get_game_gravity_acceleration()
        my_pos = self.helper.get_self_position()
        my_v = self.helper.get_self_velocity()
        game_boundary = self.helper.get_game_arena_boundary()
        vector_to_land = self.helper.get_position_vector_to_closest_land()
        live_time = 0.15
        if my_pos[1] > game_boundary[1][1] or self.helper.get_self_will_drop():
            if vector_to_land[0] > 0:
                if self.can_jump():
                    return AI_DIR_RIGHT_JUMP
                else:
                    return AI_DIR_RIGHT
            elif vector_to_land[0] < 0:
                if self.can_jump():
                    return AI_DIR_LEFT_JUMP
                else:
                    return AI_DIR_LEFT
            elif self.can_jump():
                return AI_DIR_JUMP
        elif my_pos[0] < game_boundary[0][0]:
            return AI_DIR_RIGHT
        elif my_pos[1] < game_boundary[0][1]:
            return AI_DIR_NOT_JUMP
        elif my_pos[0] > game_boundary[1][0]:
            return AI_DIR_LEFT
        future_pos = (my_pos[0] + my_v[0] * live_time, my_pos[1] + my_v[1] * live_time + 1/2 * g * live_time ** 2)
        nearest_distance = 10000
        nearest = (0, 0)
        for banana in self.helper.get_all_drop_banana_peel_position():
            distance = self.helper.get_distance(my_pos, banana)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest = banana
        if nearest != (0, 0) and (my_pos[0] > nearest[0]) * (future_pos[0] < nearest[0]):
            if my_v[0] > 0:
                return AI_DIR_LEFT
            elif my_v[0] < 0:
                return AI_DIR_RIGHT

        if self.helper.get_position_will_drop(future_pos):
            if my_v[0] > 0:
                if abs(my_v[0] > 300) and self.can_jump():
                    return AI_DIR_LEFT_JUMP
                else:
                    return AI_DIR_LEFT
            else:
                if abs(my_v[0] > 300) and self.can_jump():
                    return AI_DIR_RIGHT_JUMP
                else:
                    return AI_DIR_RIGHT
        elif future_pos[0] < game_boundary[0][0]:
            return AI_DIR_RIGHT
        elif future_pos[0] > game_boundary[1][0]:
            return AI_DIR_LEFT
        return -1

    def to_attack(self, mode):
        my_pos = self.helper.get_self_position()
        if mode == "nearest":
            enemy_id = self.helper.get_nearest_player()
        elif mode == "highestV":
            enemy_id = self.helper.get_highest_voltage_player()
        enemy_pos = self.helper.get_other_position(enemy_id)
        enemy_dst = self.helper.get_distance(my_pos, enemy_pos)
        if mode == "highestV" and enemy_dst > self.helper.get_self_attack_radius() / 2.5 or self.helper.get_other_is_invincible(enemy_id):
            enemy_id = self.helper.get_nearest_player()
            enemy_pos = self.helper.get_other_position(enemy_id)
            enemy_dst = self.helper.get_distance(my_pos, enemy_pos)
        if(self.helper.get_self_can_attack() and enemy_dst < self.helper.get_self_attack_radius() / 2.5 and not self.helper.get_other_is_invincible(enemy_id)):
            return AI_DIR_ATTACK
        else:
            return -1

    def trace_enemy(self, mode):
        my_pos = self.helper.get_self_position()
        if mode == "nearest":
            enemy_id = self.helper.get_nearest_player()
        elif mode == "highestV":
            enemy_id = self.helper.get_highest_voltage_player()
        enemy_vector = self.helper.get_vector(my_pos, self.helper.get_other_position(enemy_id))
        return self.where_to_go(self.judge_direction(enemy_vector))

    def trace_item(self):
        if self.helper.get_self_keep_item_id() != 0:
            return -1
        my_pos = self.helper.get_self_position()
        item_vector = self.helper.get_vector(my_pos, self.helper.get_nearest_item_position())
        return self.where_to_go(self.judge_direction(item_vector))

    def run_away(self, mode):
        direction = (0, 0)
        if mode == "all":
            all_distance = self.helper.get_all_player_distance()
            all_vector = self.helper.get_all_player_vector()
            ideal_vector = (0, 0)
            for i in range(len(all_vector)):
                if self.helper.get_other_player_distance(i) < self.helper.get_other_attack_radius(i):
                    ideal_vector = (ideal_vector[0] + all_vector[i][0] * all_distance[i],ideal_vector[1] + all_vector[i][1] * all_distance[i])
            direction = tuple_times(ideal_vector, -1/sum(all_distance))
        elif mode == "nearest":
            enemy_pos = self.helper.get_other_position(self.helper.get_nearest_player())
            if self.helper.get_other_player_distance(self.helper.get_nearest_player()) < self.helper.get_other_attack_radius(self.helper.get_nearest_player()):
                direction = tuple_times(self.helper.get_vector(self.helper.get_self_position(), enemy_pos), -1)
        return self.where_to_go(self.judge_direction(direction))

    def avoid_urgent_item(self):
        my_pos = self.helper.get_self_position()
        nearest = (0, 0)
        nearest_distance = 10000
        direction = (0, 0)
        for banana in self.helper.get_all_drop_banana_peel_position():
            distance = self.helper.get_distance(my_pos, banana)
            if self.helper.get_distance(my_pos, banana) < 30 and banana[1] >= my_pos[1] - self.helper.get_self_attack_radius() and distance < nearest_distance:
                nearest_distance = distance
                nearest = banana
        if nearest != (0, 0):
            direction = self.helper.get_vector(my_pos, nearest)
            direction = (-direction[0], -direction[1])
            return self.where_to_go(direction)
        else:
            return -1

    def avoid_item(self):
        my_pos = self.helper.get_self_position()
        nearest = (0, 0)
        nearest_distance = 10000
        direction = (0, 0)
        for bomb in self.helper.get_all_drop_cancer_bomb_position():
            distance = self.helper.get_distance(my_pos, bomb)
            if distance < Const.BOMB_EXPLODE_RADIUS and distance < nearest_distance:
                nearest_distance = distance
                nearest = bomb
        for banana in self.helper.get_all_drop_banana_peel_position():
            distance = self.helper.get_distance(my_pos, banana)
            if self.helper.get_distance(my_pos, banana) < 70 and distance < nearest_distance:
                nearest_distance = distance
                nearest = banana
        for black_hole in self.helper.get_all_drop_big_black_hole_position():
            distance = self.helper.get_distance(my_pos, black_hole)
            if self.helper.get_distance(my_pos, black_hole) < Const.BLACK_HOLE_EFFECT_RADIUS * 0.9 and distance < nearest_distance:
                nearest_distance = distance
                nearest = black_hole
        if nearest != (0, 0):
            direction = self.helper.get_vector(my_pos, nearest)
            direction = (-direction[0], -direction[1])
        return self.where_to_go(direction)

    def decide(self):
        my_voltage = self.helper.get_self_voltage()
        voltages = self.helper.get_all_voltage()
        mean_voltage = sum(voltages) / len(voltages)
        highest_voltage = self.helper.get_other_voltage(self.helper.get_highest_voltage_player())
        if self.helper.get_self_can_attack_time() < 0.75:
            if my_voltage <= mean_voltage or self.helper.get_self_is_invincible() or self.helper.get_live_player_num() <= 2:
                self.mode = [lambda self: self.avoid_urgent_item(), lambda self: self.to_live(), lambda self: self.avoid_item(), lambda self: self.to_attack("highestV"), lambda self: self.trace_enemy("highestV"),
                            lambda self: self.use_item(), lambda self: self.trace_item()]
            elif my_voltage <= (mean_voltage + highest_voltage) / 2:
                self.mode = [lambda self: self.avoid_urgent_item(), lambda self: self.to_live(), lambda self: self.avoid_item(), lambda self: self.to_attack("nearest"), lambda self: self.use_item(),
                            lambda self: self.run_away("nearest"), lambda self: self.trace_enemy("nearest"), lambda self: self.trace_item()]
            else:
                self.mode = [lambda self: self.avoid_urgent_item(), lambda self: self.to_live(), lambda self: self.avoid_item(), lambda self: self.to_attack("nearest"), lambda self: self.use_item(),
                            lambda self: self.run_away("all"), lambda self: self.trace_item(), lambda self: self.trace_enemy("nearest")]
        else:
            self.mode = [lambda self: self.avoid_urgent_item(), lambda self: self.to_live(), lambda self: self.avoid_item(), lambda self: self.use_item(),
                        lambda self: self.run_away("nearest"), lambda self: self.trace_item(), lambda self: self.trace_enemy("nearest")]

        not_jump = 0
        for i, function in enumerate(self.mode):
            instruction = function(self)
            if instruction != -1:
                if instruction == AI_DIR_NOT_JUMP:
                    not_jump = 1
                elif not (not_jump and instruction == AI_DIR_LEFT_JUMP or instruction == AI_DIR_RIGHT_JUMP or instruction == AI_DIR_JUMP):
                    return instruction
        return AI_DIR_STAY

