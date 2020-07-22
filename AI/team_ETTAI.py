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
        self.stay_time = 0

    def decide(self):
        decision = None
        if decision is None:
            decision = self.attack()
        
        if decision is None:
            decision = self.not_drop()

        if decision is None:
            decision = self.dodge_banana_peel()

        if decision is None:
            decision = self.use_item()

        if decision is None:
            decision = self.dodge_bomb()

        if decision is None:
            decision = self.dodge_big_black_hole()

        if decision is None:
            decision = self.pick_item()
        
        if decision is None:
            decision = self.stay_away()

        if decision is None:
            decision = self.walk_to_other_player()

        return decision

    def stay_away(self):
        # Stay away from every one when voltage of all the players are still low
        # Still try to move when everyone is unaggresive
        if self.stay_time > 25 * 60:
            self.stay_time = 0

        elif self.stay_time > 15 * 60:
            self.stay_time += 1
            return None

        player_id = self.helper.get_highest_voltage_player()
        if player_id is None:
            return None
        if self.helper.get_other_voltage(player_id) >= 100 or self.helper.get_self_is_invincible():
            return None
        count = len([ True for life in self.helper.get_all_life() if life > 0 ])
        if count == 2:
            return None
            
        self.stay_time += 1
        # Stay at left most or right most position
        mid = (self.get_left_most_position()[0] + self.get_right_most_position()[1]) / 2
        if self.helper.get_self_position()[0] < mid:
            if self.helper.get_self_jump_quota() > 1:
                return self.jump_left()
            else:
                left_most = self.get_left_most_position()
                return AI_DIR_LEFT if abs(left_most[0] - self.helper.get_self_position()[0]) > self.helper.get_self_radius() * 2 else AI_DIR_RIGHT
        else:
            if self.helper.get_self_jump_quota() > 1:
                return self.jump_right()
            else:
                right_most = self.get_right_most_position()
                return AI_DIR_RIGHT if abs(right_most[0] - self.helper.get_self_position()[0]) > self.helper.get_self_radius() * 2 else AI_DIR_LEFT

    def attack(self):
        # Attack when at least a player is near you
        nearest_id = self.helper.get_nearest_player()
        nearest_player_position = self.helper.get_other_position(nearest_id)
        if self.helper.get_self_can_attack_time() == 0 and \
           self.helper.get_distance(self.helper.get_self_position(), nearest_player_position) <  self.effective_attack_radius(nearest_id):
            return AI_DIR_ATTACK
        return None

    def effective_attack_radius(self, other_id):
        # A range to attack other players
        return min(self.helper.get_self_radius() + 1.2 * self.helper.get_other_radius(other_id), self.helper.get_self_attack_radius())

    def walk_to_other_player(self):
        # Choose nearest player with voltage more that a specific value if it exists,
        # or just find a nearest player
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

    def use_item(self):
        # Use item with some strategy
        item_id = self.helper.get_self_keep_item_id()

        if item_id == NO_ITEM:
            return None

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
            # Use when somaone in front of you
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
        
        return AI_DIR_USE_ITEM

    def dodge(self, target, radius):
        # Dodge a target with radius specified
        right_most = self.get_right_most_position()
        left_most = self.get_left_most_position()
        return self.helper.walk_to_position((right_most[0] - 2 * self.helper.get_self_radius(), right_most[1])) \
               if right_most[0] - target[0] > radius else self.helper.walk_to_position((left_most[0] + 2 * self.helper.get_self_radius(), left_most[1]))

    def dodge_bomb(self):
        # Dodge bomb
        self_position = self.helper.get_self_position()

        dodge_time = max(5, self.helper.get_self_invincible_time())
        bombs_position = self.helper.get_all_drop_cancer_bomb_position()
        explode_time = self.helper.get_all_drop_cancer_bomb_timer()
        
        bomb_explode_first = None
        # Find the bomb that would explode first
        for bomb in zip(bombs_position, explode_time):
            if bomb[1] < dodge_time and self.helper.get_distance(self_position, bomb[0]) <= 2 * self.helper.get_cancer_bomb_effect_radius():
                if bomb_explode_first is None or bomb[1] < bomb_explode_first[1]:
                    bomb_explode_first = bomb

        if bomb_explode_first is None:
            return None
        elif self.helper.get_distance(self_position, bomb_explode_first[0]) >= 2 * self.helper.get_cancer_bomb_effect_radius():
            return self.jump_high()     
        return self.dodge(bomb[0], self.helper.get_cancer_bomb_effect_radius())

    def dodge_big_black_hole(self):
        self_pos = self.helper.get_self_position()
        target_pos = self.helper.get_nearest_specific_item_position(BIG_BLACK_HOLE)
        return self.dodge(target_pos, self.helper.get_black_hole_effect_radius()) \
               if target_pos is not None and self.helper.get_distance(target_pos, self_pos) <= 2 * self.helper.get_black_hole_effect_radius() \
               else None
        
    def dodge_banana_peel(self):
        # Dodge peel
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
        # Find left most position
        platform_position = self.helper.get_platform_position()
        left_most = None
        for upper_left, bottom_right in platform_position:
            if left_most is None or upper_left[0] < left_most[0] or (upper_left[0] == left_most[0] and upper_left[1] < left_most[1]):
                left_most = upper_left
        left_most = (left_most[0], left_most[1])
        return left_most
        
    def get_right_most_position(self):
        # Find right most position
        platform_position = self.helper.get_platform_position()
        right_most = None
        for upper_left, bottom_right in platform_position:
            if right_most is None or bottom_right[0] > right_most[0] or (bottom_right[0] == right_most[0] and bottom_right[1] < right_most[1]):
                right_most = bottom_right
        right_most = (right_most[0], right_most[1])
        return right_most

    def exist_right_platform(self):
        # Check if there exists platform at right
        platforms = self.helper.get_platform_position()
        for upper_left, bottom_right in platforms:
            if bottom_right[0] > self.helper.get_self_position()[0]:
                return True
        return False

    def exist_left_platform(self):
        # Check if there exists platform at left
        platforms = self.helper.get_platform_position()
        for upper_left, bottom_right in platforms:
            if upper_left[0] < self.helper.get_self_position()[0]:
                return True
        return False

    def not_drop(self):
        # Try not to fall
        if abs(self.helper.get_self_velocity()[1]) > 2 * self.helper.get_self_jump_speed() and self.helper.get_self_can_jump():
            return AI_DIR_JUMP
        if self.helper.get_self_have_platform_below():
            return None
        if self.helper.get_self_direction() == LEFT:
            return self.jump_left() if self.exist_left_platform() else self.jump_right()
        else:
            return self.jump_right() if self.exist_right_platform() else self.jump_left()

    def jump_left(self):
        # Jump left and try to jump high
        return AI_DIR_LEFT_JUMP if self.helper.get_self_velocity()[1] >= 0 else AI_DIR_LEFT

    def jump_right(self):
        # Jump right and try to jump high
        return AI_DIR_RIGHT_JUMP if self.helper.get_self_velocity()[1] >= 0 else AI_DIR_RIGHT

    def jump_high(self):
        # Jump high
        return AI_DIR_JUMP if self.helper.get_self_velocity()[1] >= 0 else AI_DIR_STAY