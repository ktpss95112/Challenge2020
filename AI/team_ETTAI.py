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

BANANA_PEEL_RADIUS = 8

LEFT = (-1, 0)
RIGHT = (1, 0)


class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0, 0]
        self.jump = False
        self.item_wait_time = 0

    def decide(self):
        decision = None
        if decision is None:
            decision = self.attack()
        
        if decision is None:
            decision = self.not_drop()

        if decision is None:
            decision = self.dodge_banana_peel()

        if decision is None:
            decision = self.use_immediate_item()

        if decision is None:
            decision = self.dodge_bomb()

        if decision is None:
            decision = self.dodge_big_black_hole()

        if decision is None:
            decision = self.use_strategy_item()

        if decision is None:
            decision = self.pick_item()
        
        if decision == None:
            decision = self.stay_away()

        if decision == None:
            decision = self.walk_to_specific_player()

        return decision

    def stay_away(self):
        pass

    def attack(self):
        nearest_id = self.helper.get_nearest_player()
        nearest_player_position = self.helper.get_other_position(nearest_id)
        if self.helper.get_self_can_attack_time() == 0 and \
           self.helper.get_distance(self.helper.get_self_position(), nearest_player_position) <  self.effective_attack_radius(nearest_id):
            return AI_DIR_ATTACK
        return None

    def effective_attack_radius(self, other_id):
        return min(self.helper.get_self_radius() + 1.2 * self.helper.get_other_radius(other_id), self.helper.get_self_attack_radius())

    def walk_to_specific_player(self):
        player_ids = [ 0, 1, 2, 3 ]
        distances = self.helper.get_all_player_distance()
        id2dis = zip(player_ids, distances)
        id2dis = sorted(id2dis, key= lambda x : x[1] if x[1] is not None else 0, reverse= True)
        for player_id, distance in id2dis:
            if distance is not None and not self.helper.get_other_is_invincible(player_id) and self.helper.get_other_voltage(player_id) > 100:
                return self.helper.walk_to_position(self.helper.get_other_position(player_id))
        for player_id, distance in id2dis:
            if distance is not None and not self.helper.get_other_is_invincible(player_id):
                return self.helper.walk_to_position(self.helper.get_other_position(player_id))
        return None


    def walk_to_nearest_vincible_player(self):
        self_id = self.helper.get_self_id()
        self_position = self.helper.get_self_position()
        nearest_distance, nearest_player_position, nearest_player_radius = None, None, None
        for i in range(4):
            if i == self_id or self.helper.get_other_life(i) == 0:
                continue
            other_position = self.helper.get_other_position(i)
            distance = self.helper.get_distance(self_position, other_position)
            if not self.helper.get_other_is_invincible(i):
                if nearest_distance == None or distance < nearest_distance:
                    nearest_distance, nearest_player_position, nearest_player_radius = distance, other_position, self.helper.get_other_radius(i)
        
        if nearest_distance == None:
            return None
        return self.helper.walk_to_position((nearest_player_position[0], nearest_player_position[1] - nearest_player_radius - self.helper.get_self_radius()))
    
    def walk_to_highest_voltage_vincible_player(self):
        self_id = self.helper.get_self_id()
        self_position = self.helper.get_self_position()
        highest_voltage, target_player_position, target_player_radius = None, None, None
        for i in range(4):
            if i == self_id or self.helper.get_other_life(i) == 0:
                continue
            other_position = self.helper.get_other_position(i)
            other_voltage = self.helper.get_other_voltage(i)
            if other_voltage < 90:
                continue
            if not self.helper.get_other_is_invincible(i):
                if highest_voltage == None or other_voltage > highest_voltage:
                    highest_voltage, target_player_position, target_player_radius = other_voltage, other_position, self.helper.get_other_radius(i)
        
        if target_player_position == None:
            return None
        return self.helper.walk_to_position((target_player_position[0], target_player_position[0] - target_player_radius - self.helper.get_self_radius()))
    
    def pick_item(self):
        # Pick item according to priority
        if self.helper.get_self_keep_item_id() != NO_ITEM:
            return None

        elif self.helper.get_all_invincible_battery_position():
            return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(INVINCIBLE_BATTERY))
        
        elif self.helper.get_all_zap_zap_zap_position():
            return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(ZAP_ZAP_ZAP))
        
        elif self.helper.get_all_rainbow_grounder_position():
            return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(RAINBOW_GROUNDER))
        
        elif self.helper.get_self_is_invincible():
            return None

        elif self.helper.get_all_big_black_hole_position():
            return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(BIG_BLACK_HOLE))
        
        return None

    def use_immediate_item(self):
        item_id = self.helper.get_self_keep_item_id()
        if item_id == BANANA_PISTOL:
            return AI_DIR_USE_ITEM
            '''
            self_id = self.helper.get_self_id()
            self_position = self.helper.get_self_position()
            for i in range(4):
                if i == self_id or self.helper.get_other_life(i) == 0 or self.helper.get_other_is_invincible(i):
                    continue
                other_position = self.helper.get_other_position(i)
                if (self.helper.get_self_radius() == LEFT) ^ (other_position[0] > self_position[0]):
                    if abs(other_position[0] - self_position[0]) < 5 * self.helper.get_self_radius() and -self.helper.get_self_radius() <= other_position[1] - self_position[1] < 3 * self.helper.get_self_radius():
                        return AI_DIR_USE_ITEM

            return None
            '''

        elif item_id == BIG_BLACK_HOLE:
            return AI_DIR_USE_ITEM

        elif item_id == CANCER_BOMB:
            return AI_DIR_USE_ITEM

        elif item_id == ZAP_ZAP_ZAP:
            # Use when at least one player near you
            self_id = self.helper.get_self_id()
            self_position = self.helper.get_self_position()
            for i in range(4):
                if i == self_id or self.helper.get_other_life(i) == 0 or self.helper.get_other_is_invincible(i):
                    continue
                other_position = self.helper.get_other_position(i)
                if abs(self_position[0] - other_position[0]) < self.helper.get_zap_zap_zap_effect_range() // 2:
                    return AI_DIR_USE_ITEM
            return None

        elif item_id == BANANA_PEEL:
            if self.item_wait_time == 3 * 60:
                return AI_DIR_USE_ITEM
            self_id = self.helper.get_self_id()
            self_position = self.helper.get_self_position()
            for i in range(4):
                if i == self_id or self.helper.get_other_life(i) == 0 or self.helper.get_other_is_invincible(i):
                    continue
                other_position = self.helper.get_other_position(i)
                if (self.helper.get_self_radius() == LEFT) ^ (other_position[0] > self_position[0]):
                    if abs(other_position[0] - self_position[0]) < 5 * self.helper.get_self_radius() and -self.helper.get_self_radius() <= other_position[1] - self_position[1] < 3 * self.helper.get_self_radius():
                        self.item_wait_time = 0
                        return AI_DIR_USE_ITEM
            self.item_wait_time += 1
            return None

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
            return None

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
            if bomb[1] < dodge_time and self.helper.get_distance(self_position, bomb[0]) <= 2 * self.helper.get_cancer_bomb_effect_radius():
                if bomb_explode_first == None or bomb[1] < bomb_explode_first[1]:
                    bomb_explode_first = bomb

        if bomb_explode_first == None:
            return None
        if self.helper.get_distance(self_position, bomb_explode_first[0]) >= 2 * self.helper.get_black_hole_effect_radius():
            return self.jump_high()     
        return self.dodge(bomb[0], self.helper.get_black_hole_effect_radius())

    def dodge_big_black_hole(self):
        self_position = self.helper.get_self_position()

        hole_position = self.helper.get_all_drop_big_black_hole_position()

        target_hole_position = None
        min_distance = 0
        # Find neareat hole
        for pos in hole_position:
            distance = self.helper.get_distance(self_position, pos)
            if distance <= 2 * self.helper.get_black_hole_effect_radius():
                if target_hole_position == None or distance < min_distance:
                    min_distance = distance
                    target_hole_position = pos

        if target_hole_position == None:
            return None
        
        return self.dodge(target_hole_position, self.helper.get_black_hole_effect_radius())

    def dodge_banana_peel(self):
        if self.helper.get_self_invincible_time() > 0.05:
            return None

        self_pos = self.helper.get_self_position()
        self_dir = self.helper.get_self_direction()
        self_radius = self.helper.get_self_radius()
        for peel in self.helper.get_all_drop_banana_peel_position():
            if abs(peel[0] - self_pos[0]) < 2 * self_radius + BANANA_PEEL_RADIUS and abs(peel[1] - self_pos[1]) <= self_radius + BANANA_PEEL_RADIUS:
                if self_dir == LEFT and peel[0] - self_pos[0] < 0:
                    return AI_DIR_LEFT_JUMP
                elif self_dir == RIGHT and peel[0] - self_pos[0] > 0:
                    return AI_DIR_RIGHT_JUMP
        return None

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
            if bottom_right[0] > self.helper.get_self_position()[0]:
                return True
        return False

    def exist_left_platform(self):
        platforms = self.helper.get_platform_position()
        for upper_left, bottom_right in platforms:
            if upper_left[0] < self.helper.get_self_position()[0]:
                return True
        return False

    def not_drop(self):
        # Wait to modify
        if abs(self.helper.get_self_velocity()[1]) > 2 * self.helper.get_self_jump_speed():
            return AI_DIR_JUMP
        if self.helper.get_self_have_platform_below():
            return None
        if self.helper.get_self_direction() == LEFT:
            if self.exist_left_platform():
                return self.left_jump()
            else:
                return self.right_jump()
        else:
            if self.exist_right_platform():
                return self.right_jump()
            else:
                return self.left_jump()

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
    
    def left_jump(self):
        return AI_DIR_LEFT_JUMP if self.helper.get_self_velocity()[1] >= 0 else AI_DIR_LEFT

    def right_jump(self):
        return AI_DIR_RIGHT_JUMP if self.helper.get_self_velocity()[1] >= 0 else AI_DIR_RIGHT

    def jump_high(self):
        return AI_DIR_JUMP if self.helper.get_self_velocity()[1] >= 0 else AI_DIR_STAY

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
            if not self.helper.get_self_have_platform_below():
                if self.helper.get_self_can_jump():
                    return AI_DIR_JUMP
                else:
                    return AI_DIR_LEFT
            else:
                return AI_DIR_LEFT

        else:
            if not self.helper.get_self_have_platform_below():
                if self.helper.get_self_can_jump():
                    return AI_DIR_JUMP
                else:
                    return AI_DIR_RIGHT
            else:
                return AI_DIR_RIGHT

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