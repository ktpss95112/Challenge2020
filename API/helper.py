import pygame as pg

import Const

class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.player_id = index
        self.player_radius = Const.PLAYER_RADIUS
        self.player_normal_speed = Const.PLAYER_NORMAL_SPEED
        self.player_jump_speed = Const.PLAYER_JUMP_SPEED
        self.player_respawn_position = Const.PLAYER_RESPAWN_POSITION
        self.player_gravity_acceleration = Const.GRAVITY_ACCELERATION
        self.attack_radius_multiple_constant = Const.ATTACK_RADIUS_MULTIPLE_CONSTANT
        self.be_attacked_acceleration = Const.BE_ATTACKED_ACCELERATION
        self.drag_critical_speed = Const.DRAG_CRITICAL_SPEED
        self.drag_coefficient = Const.DRAG_COEFFICIENT
        self.arena_size = Const.ARENA_SIZE
        self.life_boundary = tuple(Const.LIFE_BOUNDARY)

    # get self information
    def get_self_id(self):
        return self.player_id
    
    def get_self_position(self):
        return tuple(self.model.players[self.player_id].position)

    def get_self_velocity(self):
        return tuple(self.model.players[self.player_id].velocity)

    def get_self_direction(self):
        return tuple(self.model.players[self.player_id].direction)

    def get_self_keep_item_id(self):
        return self.model.players[self.player_id].keep_item_id

    def get_self_voltage(self):
        return self.model.players[self.player_id].voltage

    def get_self_is_invincible(self):
        return (self.model.players[self.player_id].invincible_time > 0)
    
    def get_self_invincible_time(self):
        return self.model.players[self.player_id].invincible_time

    def get_self_can_not_control_time(self):
        return self.model.players[self.player_id].can_not_control_time
    
    def get_self_life(self):
        return self.model.players[self.player_id].life

    def get_self_score(self):
        return self.model.players[self.player_id].score

    # get all player information    
    def get_all_position(self):
        return [tuple(player.position) for player in self.model.players]

    def get_all_velocity(self):
        return [tuple(player.velocity) for player in self.model.players]

    def get_all_direction(self):
        return [tuple(player.direction) for player in self.model.players]

    def get_all_keep_item_id(self):
        return [player.keep_item_id for player in self.model.players]

    def get_all_voltage(self):
        return [player.voltage for player in self.model.players]

    def get_all_is_invincible(self):
        return [player.invincible_time > 0 for player in self.model.players]
    
    def get_all_invincible_time(self):
        return [player.invincible_time for player in self.model.players]

    def get_all_can_not_control_time(self):
        return [player.can_not_control_time for player in self.model.players]
    
    def get_all_life(self):
        return [player.life for player in self.model.players]

    def get_all_score(self):
        return [player.score for player in self.model.players]

    # get other players information
    def get_other_position(self, index):
        return tuple(self.model.players[index].position)

    def get_other_velocity(self, index):
        return tuple(self.model.players[index].velocity)

    def get_other_direction(self, index):
        return tuple(self.model.players[index].direction)

    def get_other_keep_item_id(self, index):
        return self.model.players[index].keep_item_id

    def get_other_voltage(self, index):
        return self.model.players[index].voltage

    def get_other_is_invincible(self, index):
        return (self.model.players[index].invincible_time > 0)
    
    def get_other_invincible_time(self, index):
        return self.model.players[index].invincible_time

    def get_other_can_not_control_time(self, index):
        return self.model.players[index].can_not_control_time
    
    def get_other_life(self, index):
        return self.model.players[index].life

    def get_other_score(self, index):
        return self.model.players[index].score

    # get item information
    def get_all_item_position(self):
        itemlist = []
        for i in range(Const.ITEM_SPECIES + 1):
            itemlist.append([])
        for item in self.model.items:
            itemlist[item.item_id].append(tuple(item.position))

    # get entity information

    # get platform information 
    def get_platform_position(self):
        return [(tuple(platform.upper_left), tuple(platform.bottom_right)) for platform in self.model.platforms]

    # get special information
    def get_nearest_player(self):  # when the nearest_player not only one?
        nearest_id = 0
        minimum_distance = 10000 ** 2 
        for player in self.model.players:
            if player.player_id != self.player_id:
                current_distance = (self.model.players[self.player_id].position - player.position).magnitude() 
                if current_distance < minimum_distance:
                    minimum_distance = current_distance
                    nearest_id = player.player_id
        return player_id
    
    def get_highest_voltage_player(self):    # when the highest_voltage_player not only one?
        highest_voltage_id = 0
        highest_voltage = 0
        for player in self.model.players:
            if player.voltage > highest_voltage:
                highest_voltage = player.voltage
                highest_voltage_id = player.player_id
        return highest_voltage_id

    def get_highest_score_player(self):   # when the highest_score_player not only one?
        highest_score_id = 0
        highest_score = 0
        for player in self.model.players:
            if player.score > highest_score:
                highest_score = player.score
                highest_score_id = player.player_id
        return highest_score_id

    # def get_distance(p, q):
    # def get_position_vector(p, q):
    # def get_distance_to_closest_land():
    # def get_position_vector_to_closest_land():
