# action
AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_LEFT_JUMP   = 3
AI_DIR_RIGHT_JUMP  = 4
AI_DIR_ATTACK      = 5
AI_DIR_USE_ITEM    = 6
AI_DIR_STAY        = 7

# item_id
NO_ITEM            = 0
BANANA_PISTOL      = 1
BIG_BLACK_HOLE     = 2
CANCER_BOMB        = 3
ZAP_ZAP_ZAP        = 4
BANANA_PEEL        = 5
RAINBOW_GROsUNDER  = 6
INVINCIBLE_BATTERY = 7

class TeamAI:
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [1, 0, 3, 2]  # (1, 0, 3, 2)
    
    def decide(self):
        myID = self.helper.get_self_id()
        myPos = self.helper.get_self_position()
        myAttackRadius = self.helper.get_self_attack_radius()
        myRadius = self.helper.get_self_radius()
        myVoltage = self.helper.get_self_voltage()
        closestPlayerID = self.helper.get_nearest_player()
        closestPlayerPos = self.helper.get_other_position(closestPlayerID)
        closestPlayerDis = self.helper.get_other_player_distance(closestPlayerID)
        closestPlayerRadius = self.helper.get_other_radius(closestPlayerID)
        platformID = self.helper.get_above_which_platform(self.helper.get_self_position())
        closestItemPos = self.helper.get_nearest_item_position()
        itemID = self.helper.get_self_keep_item_id()
        allVoltage = self.helper.get_all_voltage()
        allVector = self.helper.get_all_player_vector()

        if myPos[0]>1131:
            return AI_DIR_LEFT_JUMP
        if myPos[0]<1:
            return AI_DIR_RIGHT_JUMP
        if myPos[1]>620:
            return AI_DIR_JUMP

        if itemID != NO_ITEM:  # use item
            if itemID == BANANA_PEEL:  # banana peel
                return AI_DIR_USE_ITEM
            if itemID == BANANA_PISTOL:  # banana pistol
                return AI_DIR_USE_ITEM
            if itemID == BIG_BLACK_HOLE:  # black hole
                if closestPlayerDis < self.helper.get_black_hole_effect_radius():
                    return AI_DIR_USE_ITEM
            if itemID == CANCER_BOMB:  # cancer bomb
                if closestPlayerDis < self.helper.get_cancer_bomb_effect_radius():
                    return AI_DIR_USE_ITEM
            if itemID == RAINBOW_GROUNDER:  # rainbow grounder
                if myVoltage > 35: 
                    return AI_DIR_USE_ITEM
            if itemID == INVINCIBLE_BATTERY:  # invincible battery
                if closestPlayerDis < myAttackRadius:
                    return AI_DIR_USE_ITEM
            if itemID == ZAP_ZAP_ZAP:  # zap zap zap
                for vec in allVector:
                    if vec!=None and (vec[0]!=0 or vec[1]!=0) and abs(vec[0])<self.helper.get_zap_zap_zap_effect_range():
                        return AI_DIR_USE_ITEM
        if closestPlayerDis < myAttackRadius and self.helper.get_self_can_attack():
            return AI_DIR_ATTACK
        for i in [6,7]:
            itemPos = self.helper.get_nearest_specific_item_position(i)
            if itemPos != None: #and self.helper.get_above_which_platform(itemPos) != -1:
                return self.helper.walk_to_position(itemPos)
        for i in range(len(allVoltage)):  # trace the player with voltage > 100
            if allVoltage[i]!=None and (allVoltage[i] > 100):
                if self.helper.get_other_position(i)!=None:
                    return self.helper.walk_to_position(closestPlayerPos)
        for i in range(len(allVoltage)):  # trace the player with higher voltage
            if allVoltage[i]!=None and (allVoltage[i] > myVoltage):
                if self.helper.get_other_position(i)!=None:
                    return self.helper.walk_to_position(closestPlayerPos)
        if platformID != -1:
            # go to middle of the platform
            platform_pos = self.helper.get_platform_position()[platformID]
            platform_mid = ((platform_pos[0][0] + platform_pos[1][0]) * 0.5, platform_pos[0][1])
            return self.helper.walk_to_position(platform_mid)
        else:
            # go to closest land
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            closest_land_pos = (myPos[0] + closest_land_vec[0], myPos[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)
            
        
        
            
            
            

