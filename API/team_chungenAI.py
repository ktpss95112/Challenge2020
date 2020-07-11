from API.base import BaseAI
import pygame as pg
import Const

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_LEFT_JUMP   = 3
AI_DIR_RIGHT_JUMP  = 4
AI_DIR_ATTACK      = 5
AI_DIR_USE_ITEM    = 6
AI_DIR_STAY        = 7

"""
AI constants
"""
DIR_NUM = 8
MAX_DEPTH = 2
DECIDE_FRAME_NUM = 2
DECIDE_TIME = DECIDE_FRAME_NUM / 60 # (second)
STATE_PER_FRAME = (DIR_NUM ** (MAX_DEPTH + 1) - 1) // DECIDE_FRAME_NUM + 1
DEBUG = False

class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0]
        self.decide_timer = 0
        self.state_tree = StateTree(self.helper)
        self.state_tree_is_init = False

    def decide(self):
        if not self.state_tree_is_init: # first initialize
            self.state_tree_is_init = True
            self.state_tree.initialize()
            self.decide_timer = DECIDE_FRAME_NUM
            return AI_DIR_STAY
        if self.decide_timer == 0:
            self.decide_timer = DECIDE_FRAME_NUM
            decision = self.state_tree.decide(score)
            self.state_tree.initialize()
            if DEBUG:
                print(f'decision {decision}')
            self.decide_timer -= 1
            return decision
        else:
            for _ in range(STATE_PER_FRAME):
                self.state_tree.predict()
            self.decide_timer -= 1
            return AI_DIR_STAY


class StateTree(object):
    def __init__(self, helper):
        self.env = Environment(helper)
        self.max_state_num = (DIR_NUM ** (MAX_DEPTH + 1) - 1) // (DIR_NUM - 1)

    def initialize(self):
        # generate root using env
        self.env.initialize()
        self.states = [SelfState(*self.env.self_info(), self.env)]

    def predict(self):
        # predict next state
        n = len(self.states)
        if n >= self.max_state_num:
            return
        parent, step = self.states[(n - 1) // DIR_NUM], (n - 1) % DIR_NUM
        if parent is None:
            self.states.append(None)
        else:
            self.states.append(parent.child_state(step))

    def decide(self, score_f):
        score_sum_of_steps = [0 for _ in range(DIR_NUM)]
        child_num_of_steps = [0 for _ in range(DIR_NUM)]
        child_num = DIR_NUM ** (MAX_DEPTH - 1)
        start = (DIR_NUM ** MAX_DEPTH - 1) // (DIR_NUM - 1)
        for step in range(DIR_NUM):
            for i in range(start + step * child_num, start + (step + 1) * child_num):
                if self.states[i] is None:
                    continue
                child_num_of_steps[step] += 1
                score_sum_of_steps[step] += score_f(self.states[i], self.env)
        avg_score_of_steps = [s / n if n != 0 else -10000 for s, n in zip(score_sum_of_steps, child_num_of_steps)]
        if DEBUG:
            print(avg_score_of_steps)
        return avg_score_of_steps.index(max(avg_score_of_steps))


class Environment(object):
    def __init__(self, helper):
        self.helper = helper

    def initialize(self):
        # get all needed game information
        self.self_id = self.helper.get_self_id()

        self.self_normal_speed = self.helper.get_self_normal_speed()
        self.self_jump_speed = self.helper.get_self_jump_speed()
        self.self_attack_radius = self.helper.get_self_attack_radius()
        
        self.self_pos = self.helper.get_self_position()
        self.self_vel = self.helper.get_self_velocity()
        self.self_life = self.helper.get_self_life()
        self.self_voltage = self.helper.get_self_voltage()
        self.self_item_id = self.helper.get_self_keep_item_id()
        self.self_jump_quota = self.helper.get_self_jump_quota()
        self.self_attack_cd = self.helper.get_self_can_attack_time()
        self.self_invincible_time = self.helper.get_self_invincible_time()
        self.self_uncontrollable_time = self.helper.get_self_uncontrollable_time()
        self.self_respawn_position = Const.PLAYER_RESPAWN_POSITION[self.helper.get_game_stage()][self.helper.get_self_id()]

        self.platforms = self.helper.get_platform_position()
        self.items = self.helper.get_all_item_position()
        self.entities = self.helper.get_all_entity_position()
        self.other_player_pos = list(map(pg.Vector2, self.helper.get_all_position()))
        self.other_player_pos.pop(self.helper.get_self_id())

        self.arena_boundary = self.helper.get_game_arena_boundary()
        self.life_boundary = self.helper.get_game_life_boundary()
        self.g = self.helper.get_game_player_gravity_acceleration()

    def self_info(self):
        return (self.self_life, self.self_pos, self.self_vel, self.self_voltage, self.self_item_id,\
            self.self_jump_quota, self.self_attack_cd,\
            self.self_invincible_time, self.self_uncontrollable_time,)


class SelfState(object):
    def __init__(self, life, pos, vel, voltage, item_id,\
                jump_quota, attack_cd, invincible_time, uncontrollable_time,\
                environment):
        self.life = life
        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(vel)
        self.voltage = voltage
        self.item_id = item_id
        self.jump_quota = jump_quota
        self.attack_cd = attack_cd
        self.invincible_time = invincible_time
        self.uncontrollable_time = uncontrollable_time

        self.env = environment

    def child_state(self, step):
        next_life = self.life
        next_pos = pg.Vector2(self.pos)
        next_vel = pg.Vector2(self.vel)
        next_voltage = self.voltage
        next_item_id = self.item_id
        next_jump_quota = self.jump_quota
        next_attack_cd = self.attack_cd
        next_invincible_time = self.invincible_time
        next_uncontrollable_time = self.uncontrollable_time
        
        if step == AI_DIR_LEFT:
            if next_uncontrollable_time > 0:
                return None
            next_vel.x = -self.env.self_normal_speed

        elif step == AI_DIR_RIGHT:
            if next_uncontrollable_time > 0:
                return None
            next_vel.x = self.env.self_normal_speed

        elif step == AI_DIR_JUMP:
            if next_jump_quota == 0:
                return None
            next_vel.y = -self.env.self_jump_speed

        elif step == AI_DIR_LEFT_JUMP:
            if next_jump_quota == 0 or next_uncontrollable_time > 0:
                return None
            next_vel.y = -self.env.self_jump_speed
            next_vel.x -= self.env.self_normal_speed

        elif step == AI_DIR_RIGHT_JUMP:
            if next_jump_quota == 0 or next_uncontrollable_time > 0:
                return None
            next_vel.y = -self.env.self_jump_speed
            next_vel.x += self.env.self_normal_speed

        elif step == AI_DIR_ATTACK:
            if self.attack_cd > 0:
                return None
            next_attack_cd = 90 # frame

        elif step == AI_DIR_USE_ITEM:
            if next_item_id == 0:
                return None
            if next_item_id == 1:
                pass
            elif next_item_id == 2:
                pass
            elif next_item_id == 3:
                pass
            elif next_item_id == 4:
                next_voltage += 10
            elif next_item_id == 5:
                pass
            elif next_item_id == 6:
                next_voltage -= 10
            elif next_item_id == 7:
                next_invincible_time += 300
            next_item_id = 0

        elif step == AI_DIR_STAY:
            pass

        # update pos and vel (simple ver.)
        next_vel.y -= self.env.g
        next_pos += next_vel * DECIDE_TIME + 0.5 * pg.Vector2(0, self.env.g) * DECIDE_TIME ** 2
        
        # detect platform collision
        for platform in self.env.platforms:
            collide_point = detect_platform_collision(self.pos, next_pos, platform)
            if not collide_point is None:
                next_vel.y *= -1
                next_pos = collide_point
                next_jump_quota = 3
                break
        # detect item
        # detect entity

        # update timer
        next_attack_cd -= DECIDE_TIME
        if next_attack_cd < 0:
            next_attack_cd = 0
        next_invincible_time -= DECIDE_TIME
        if next_invincible_time < 0:
            next_invincible_time = 0
        next_uncontrollable_time -= DECIDE_TIME
        if next_uncontrollable_time < 0:
            next_uncontrollable_time = 0
        
        # detect boundary
        if not ((self.env.life_boundary[0][0] <= next_pos.x <= self.env.life_boundary[1][0]) and\
                (self.env.life_boundary[0][1] <= next_pos.y <= self.env.life_boundary[1][1])):
            next_life -= 1
            next_vel = pg.Vector2(0, 0)
            next_pos = pg.Vector2(self.env.self_respawn_position)
            next_item_id = 0
            next_voltage = 0
            next_jump_quota = 3
            next_attack_cd = 0
            next_invincible_time = 0
            next_uncontrollable_time = 0

        return SelfState(next_life, next_pos, next_vel, next_voltage, next_item_id,\
                next_jump_quota, next_attack_cd, next_invincible_time, next_uncontrollable_time,\
                self.env)


def detect_platform_collision(pos, next_pos, platform):
    if not ((pos.y < next_pos.y) and (next_pos.y > platform[0][1] > pos.y)):
        return None
    ub = platform[1][0] - pos.x
    lb = platform[0][0] - pos.x
    dy = platform[0][1] - pos.y
    dx = (next_pos.x - pos.x) / (next_pos.y - pos.y) * dy
    return pg.Vector2(pos.x + dx, pos.y + dy) if lb <= dx <= ub else None

def score(selfstate, env):
    score = 0
    score += selfstate.life * 100

    for platform in env.platforms:
        width = platform[1][0] - platform[0][0]
        dist = env.helper.get_distance(selfstate.pos, (pg.Vector2(platform[0]) + pg.Vector2(platform[1])) / 2)
        score += width / dist
    
    return score