from API.base import BaseAI
import random
import math

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_LEFT_JUMP   = 3
AI_DIR_RIGHT_JUMP  = 4
AI_DIR_ATTACK      = 5
AI_DIR_USE_ITEM    = 6
AI_DIR_STAY        = 7

NO_ITEM = 0
BANANA_PISTOL = 1
BIG_BLACK_HOLE = 2
CANCER_BOMB = 3
ZAP_ZAP_ZAP = 4
BANANA_PEEL = 5
RAINBOW_GROUNDER = 6
INVINCIBLE_BATTERY = 7

LEFT = (-1, 0)
RIGHT = (1, 0)
PLAYER_RADIUS = 25
ZAP_ZAP_ZAP_RANGE = 5 * PLAYER_RADIUS
BOMB_EXPLODE_RADIUS = 16 * PLAYER_RADIUS
BLACK_HOLE_EFFECT_RADIUS = 10 * PLAYER_RADIUS


class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0, 0]
        self.jump = False

    def decide(self):
        decision = None
        #if decision == None and self.jump:
        #    self.jump = False
        #    return AI_DIR_JUMP

        if decision == None:
            decision = self.not_drop()

        if decision == None:
            decision = self.attack()

        if decision == None:
            decision = self.use_immediate_item()

        if decision == None:
            decision = self.dodge_bomb()

        if decision == None:
            decision = self.use_strategy_item()

        if decision == None:
            decision = self.pick_item()

        if decision == None:
            decision = self.walk_to_highest_voltage_vincible_player()

        if decision == None:
            decision = self.walk_to_nearest_vincible_player()
            
        if decision == None:
            decision = AI_DIR_STAY

        #if decision == AI_DIR_JUMP:
        #    self.jump = True

        return decision

    def attack(self):
        nearest_id = self.helper.get_nearest_player()
        nearest_player_position = self.helper.get_other_position(nearest_id)
        if self.helper.get_self_can_attack_time() == 0 and \
           self.helper.get_distance(self.helper.get_self_position(), nearest_player_position) < 1.5 * self.helper.get_self_radius() + self.helper.get_other_radius(nearest_id):
            return AI_DIR_ATTACK
        return None

    def walk_to_good_place(self):
        self_position = self.helper.get_self_position()
        land_index = self.helper.get_above_which_land(self_position)
        if land_index == -1:
            land_position_vector = self.helper.get_position_vector_to_closest_land()
            return self.helper.walk_to_position((land_position_vector[0] + self_position[0], land_position_vector[1] + self_position[1]))
        
        land_position = self.helper.get_platform_position()[land_index]
        land_radius = (land_position[1][0] - land_position[0][0]) // 2
        land_center = (land_position[1][0] + land_position[0][0]) // 2
        if land_center - land_radius // 2 <= self_position[0] <= land_center - land_radius // 2:
            return None
        return self.helper.walk_to_position((land_center, land_position[0][1] - 2 * self.helper.get_self_radius()))
        

    def walk_to_nearest_player(self):
        nearest_id = self.helper.get_nearest_player()
        nearest_player_position = self.helper.get_other_position(nearest_id)
        return self.helper.walk_to_position((nearest_player_position[0], nearest_player_position[1] + self.helper.get_other_radius(nearest_id) + self.helper.get_self_radius()))

    def walk_to_nearest_vincible_player(self):
        self_id = self.helper.get_self_id()
        self_position = self.helper.get_self_position()
        nearest_distance = None
        nearest_player_position = None
        for i in range(4):
            if i == self_id:
                continue
            other_position = self.helper.get_other_position(i)
            distance = self.helper.get_distance(self_position, other_position)
            if not self.helper.get_other_is_invincible(i) and not self.helper.get_other_will_drop(i):
                if nearest_distance == None or distance < nearest_distance:
                    nearest_distance, nearest_player_position = distance, other_position
        
        if nearest_distance == None:
            return None
        return self.helper.walk_to_position(nearest_player_position)
    
    def walk_to_highest_voltage_vincible_player(self):
        self_id = self.helper.get_self_id()
        self_position = self.helper.get_self_position()
        highest_voltage = None
        target_player_position = None
        for i in range(4):
            if i == self_id:
                continue
            other_position = self.helper.get_other_position(i)
            other_voltage = self.helper.get_other_voltage(i)
            if other_voltage > 85:
                continue
            if not self.helper.get_other_is_invincible(i) and not self.helper.get_other_will_drop(i):
                if highest_voltage == None or other_voltage > highest_voltage:
                    highest_voltage, target_player_position = other_voltage, other_position
        
        if target_player_position == None:
            return None
        return self.helper.walk_to_position(target_player_position)
    
    def pick_item(self):
        # Pick item according to priority
        if self.helper.get_self_keep_item_id() != NO_ITEM:
            return None

        elif self.helper.get_all_invincible_battery_position():
            return self.walk_to_nearest_item(self.helper.get_all_invincible_battery_position())
        
        elif self.helper.get_all_rainbow_grounder_position():
            return self.walk_to_nearest_item(self.helper.get_all_rainbow_grounder_position())
        
        elif self.helper.get_self_is_invincible():
            return None

        elif self.helper.get_all_zap_zap_zap_position():
            return self.walk_to_nearest_item(self.helper.get_all_zap_zap_zap_position())

        elif self.helper.get_all_big_black_hole_position():
            return self.walk_to_nearest_item(self.helper.get_all_big_black_hole_position())
        
        return None

    def walk_to_nearest_item(self, items):
        # Walk to the nearist item in the list
        self_position = self.helper.get_self_position()
        min_distance = None
        min_item_position = self_position
        for p in items:
            distance = self.helper.get_distance(self_position, p)
            if not self.helper.get_position_will_drop(p):
                if min_distance == None or distance < min_distance:
                    min_distance = distance
                    min_item_position = p
        return self.helper.walk_to_position(min_item_position)

    def use_immediate_item(self):
        item_id = self.helper.get_self_keep_item_id()
        if item_id == BANANA_PISTOL:
            return AI_DIR_USE_ITEM

        elif item_id == BIG_BLACK_HOLE:
            return AI_DIR_USE_ITEM

        elif item_id == CANCER_BOMB:
            return AI_DIR_USE_ITEM

        elif item_id == ZAP_ZAP_ZAP:
            # Use when at least one player near you
            self_id = self.helper.get_self_id()
            self_position = self.helper.get_self_position()
            for i in range(4):
                if i == self_id:
                    continue
                other_position = self.helper.get_other_position(i)
                if abs(self_position[0] - other_position[0]) < ZAP_ZAP_ZAP_RANGE // 2:
                    return AI_DIR_USE_ITEM
            return None

        elif item_id == BANANA_PEEL:
            return AI_DIR_USE_ITEM

        elif item_id == RAINBOW_GROUNDER:
            return AI_DIR_USE_ITEM

        elif item_id == INVINCIBLE_BATTERY:
            return AI_DIR_USE_ITEM
        
        return None

    def use_strategy_item(self):
        # Use item with some strategy
        item_id = self.helper.get_self_keep_item_id()
        if item_id == NO_ITEM:
            return None

        else:
            return AI_DIR_USE_ITEM

    def dodge(self, target, radius):
        # Use self_position when implement where could arrive quickly
        # self_position = self.helper.get_self_position()
        right_most = self.get_right_most_position()
        left_most = self.get_left_most_position()
        if right_most[0] - target[0] > radius:
            return self.helper.walk_to_position((right_most[0] - 2 * self.helper.get_self_radius(), right_most[1]))
        elif target[0] - left_most[0] > radius:
            return self.helper.walk_to_position((left_most[0] + 2 * self.helper.get_self_radius(), left_most[1]))

    def dodge_bomb(self):
        self_position = self.helper.get_self_position()

        dodge_time = max(5, self.helper.get_self_invincible_time())
        bombs_position = self.helper.get_all_drop_cancer_bomb_position()
        explode_time = self.helper.get_all_drop_cancer_bomb_timer()
        
        bomb_explode_first = None
        # Fine neareat bomb
        for bomb in zip(bombs_position, explode_time):
            if bomb[1] < dodge_time and self.helper.get_distance(self_position, bomb[0]) <= 2 * BOMB_EXPLODE_RADIUS:
                if bomb_explode_first == None or bomb[1] < bomb_explode_first[1]:
                    bomb_explode_first = bomb

        if bomb_explode_first == None:
            return None
        if self.helper.get_distance(self_position, bomb_explode_first[0]) >= 2 * BOMB_EXPLODE_RADIUS:
            return AI_DIR_JUMP        
        return self.dodge(bomb[0], BOMB_EXPLODE_RADIUS)

    def dodge_big_black_hole(self):
        self_position = self.helper.get_self_position()

        hole_position = self.helper.get_all_drop_big_black_hole_position()

        target_hole_position = None
        min_distance = 0
        # Find neareat hole
        for pos in hole_position:
            distance = self.helper.get_distance(self_position, pos)
            if distance <= 2 * BLACK_HOLE_EFFECT_RADIUS:
                if target_hole_position == None or distance < min_distance:
                    min_distance = distance
                    target_hole_position = pos

        if target_hole_position == None:
            return None
        
        return self.dodge(target_hole_position, BLACK_HOLE_EFFECT_RADIUS)

    def get_left_most_position(self):
        # Get position of the left most place
        platform_position = self.helper.get_platform_position()
        left_most = None
        for upper_left, bottom_right in platform_position:
            if left_most == None or upper_left[0] < left_most[0] or (upper_left[0] == left_most[0] and upper_left[1] < left_most[1]):
                left_most = upper_left
        left_most = (left_most[0], left_most[1])
        return left_most
        
    def get_right_most_position(self):
        # Get position of the right most place
        platform_position = self.helper.get_platform_position()
        right_most = None
        for upper_left, bottom_right in platform_position:
            if right_most == None or bottom_right[0] > right_most[0] or (bottom_right[0] == right_most[0] and bottom_right[1] < right_most[1]):
                right_most = bottom_right
        right_most = (right_most[0], right_most[1])
        return right_most

    def exist_right_platform(self):
        platforms = self.helper.get_platform_position()
        for upper_left, bottom_right in platforms:
            if upper_left[0] > self.helper.get_self_position()[0]:
                return True
        return False

    def exist_left_platform(self):
        platforms = self.helper.get_platform_position()
        for upper_left, bottom_right in platforms:
            if bottom_right[0] < self.helper.get_self_position()[0]:
                return True
        return False

    def not_drop(self):
        if not self.helper.get_self_will_drop():
            return None
        if self.helper.get_self_direction() == LEFT:
            if self.exist_left_platform() and self.helper.get_self_can_jump():
                return AI_DIR_LEFT_JUMP
            else:
                return AI_DIR_RIGHT
        else:
            if self.exist_right_platform():
                return AI_DIR_RIGHT_JUMP
            else:
                return AI_DIR_LEFT

        self_position = self.helper.get_self_position()
        platforms = self.helper.get_platform_position()
        min_distance = None
        min_position = None
        is_upper_left = None
        for upper_left, bottom_right in platforms:
            distance_upper = self.helper.get_distance(upper_left, self_position)
            distance_bottom = self.helper.get_distance(bottom_right, self_position)
            
            if min_distance == None or distance_upper < min_distance:
                min_position, min_distance = upper_left, distance_upper
                is_upper_left = True

            if min_distance == None or distance_bottom < min_distance:
                min_position, min_distance = (bottom_right[0], upper_left[1]), distance_bottom
                is_upper_left = False

        if min_distance == None:
            # Must not be executed
            return None
        
        self_radius = self.helper.get_self_radius()
        if is_upper_left:
            min_position = (min_position[0] + 2 * self_radius, 0)
        else:
            min_position = (min_position[0] - 2 * self_radius, 0)

        return self.helper.walk_to_position(min_position)
        
    def suicide(self):
        # Wait to implement well
        if self.helper.get_self_voltage() < 90:
            return None

        self_position = self.helper.get_self_position()
        left_most = self.get_left_most_position()
        right_most = self.get_right_most_position()
        left_distance = self.helper.get_distance(left_most, self_position)
        right_distance = self.helper.get_distance(right_most, self_position)
        go_left = True

        if right_distance < left_distance:
            go_left = False
        if go_left:
            if self.helper.get_self_will_drop():
                if self.helper.get_self_can_jump():
                    return AI_DIR_JUMP
                else:
                    return AI_DIR_LEFT
            else:
                return AI_DIR_LEFT

        else:
            if self.helper.get_self_will_drop():
                if self.helper.get_self_can_jump():
                    return AI_DIR_JUMP
                else:
                    return AI_DIR_RIGHT
            else:
                return AI_DIR_RIGHT