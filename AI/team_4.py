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
RAINBOW_GROUNDER   = 6
INVINCIBLE_BATTERY = 7

class TeamAI:
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0, 0]
    
    def decide(self):
        # get distance to other player
        distance = self.helper.get_all_player_distance()
        myid = self.helper.get_self_id()
        heidongr = self.helper.get_black_hole_effect_radius()
        bombr = self.helper.get_cancer_bomb_effect_radius()
        zapr = self.helper.get_zap_zap_zap_effect_range()
        #print(zapr)
        all_pos = self.helper.get_all_position()
        my_pos = self.helper.get_self_position()
        platform_id = self.helper.get_above_which_platform(my_pos)
        plats = self.helper.get_platform_position()
        my_id = self.helper.get_self_id()
        np = self.helper.get_nearest_player()
        nppos = self.helper.get_nearest_player_position()
        if self.helper.get_self_keep_item_id() == RAINBOW_GROUNDER:
            return AI_DIR_USE_ITEM
        if self.helper.get_self_voltage() > 20 and self.helper.get_self_keep_item_id() == NO_ITEM:
            #rbs = self.helper.get_all_rainbow_grounder_position()
            #print(rbs)
            rbs = self.helper.get_nearest_specific_item_position(RAINBOW_GROUNDER)
            
            if rbs != None and self.helper.get_self_keep_item_id() == NO_ITEM:
                if self.helper.get_above_which_platform(rbs) != -1:
                    #print('rain' , rbs , self.helper.get_self_keep_item_id())
                    return self.helper.walk_to_position(rbs)
                '''if rbs[minpos] - self.helper.get_platform_position()\
                    [self.helper.get_above_which_platform(rbs[minpos])][1] <= 50:
                    return self.helper.walk_to_position(rbs[minpos])'''

        btrs = self.helper.get_nearest_specific_item_position(INVINCIBLE_BATTERY)
        if btrs != None and self.helper.get_self_keep_item_id() == NO_ITEM:
            if self.helper.get_above_which_platform(btrs) != -1:
                #print('battery' , btrs , self.helper.get_self_keep_item_id())
                return self.helper.walk_to_position(btrs)
        if self.helper.get_self_can_attack() and\
            min(d for d in distance if not d is None) < self.helper.get_self_attack_radius():
            if self.helper.get_self_keep_item_id == INVINCIBLE_BATTERY:
                return AI_DIR_USE_ITEM
            return AI_DIR_ATTACK
        if self.helper.get_self_keep_item_id() != NO_ITEM:
            if self.helper.get_self_keep_item_id() == BIG_BLACK_HOLE:
                
                if sum(1 if dis < heidongr * 0.7 else 0 for dis in distance if dis !=None) >= 2 \
                    and self.helper.get_self_voltage() < 80:
                    return AI_DIR_USE_ITEM
                elif self.helper.get_self_voltage() >= 80:
                    return AI_DIR_USE_ITEM
                maxidx = distance.index(max(distance))
                meanpos = (sum(all_pos[i][0] for i in range(len(distance)) if i != maxidx)/2 , \
                sum(all_pos[i][1] for i in range(len(distance)) if i != maxidx)/2)
                return self.helper.walk_to_position(meanpos)
                
            elif self.helper.get_self_keep_item_id() == CANCER_BOMB: 
                if min(dis for dis in distance if dis != None) < self.helper.get_cancer_bomb_effect_radius() * 0.7:
                    return AI_DIR_USE_ITEM
                #return self.helper.walk_to_position(self.helper.get_nearest_player_position())
            elif self.helper.get_self_keep_item_id() == ZAP_ZAP_ZAP:
                for p in range(len(all_pos)):
                    if all_pos[p] != None and my_pos != None:
                        if abs(all_pos[p][0] - my_pos[0]) < zapr * 0.8 and p != my_id:
                            return AI_DIR_USE_ITEM
                
            elif self.helper.get_self_keep_item_id() == BANANA_PISTOL:
                return AI_DIR_USE_ITEM
            else:
                return AI_DIR_USE_ITEM
        '''if self.helper.get_other_voltage(np) < self.helper.get_self_voltage()\
             and self.helper.get_self_voltage() >= 80 and not self.helper.get_self_is_invincible():
            p = plats[(platform_id + 2) % len(plats)]
            pos = ((p[0][0] + p[1][0]) / 2 , p[0][1])
            return self.helper.walk_to_position(pos)'''
        if platform_id == -1 and self.helper.get_self_jump_quota() <= 2:
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            closest_land_pos = (my_pos[0] + closest_land_vec[0], my_pos[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)
        chenzoe = self.helper.get_highest_voltage_player()
        if self.helper.get_self_can_attack() and\
            min(d for d in distance if not d is None) < self.helper.get_self_attack_radius():
            return AI_DIR_ATTACK
        return self.helper.walk_to_position(self.helper.get_other_position(chenzoe))
        
        
        
        my_ID = self.helper.get_self_id()
        my_radius = self.helper.get_self_radius() #原本大小約 == 25
        my_pos = self.helper.get_self_position() 
        my_volt = self.helper.get_self_voltage()
        my_speed = self.helper.get_self_velocity() #自己的速度
        now_item = self.helper.get_self_keep_item_id() #現在已吃的道具
        dis_others = self.helper.get_all_player_distance() #自己和其他人的距離(包含自己)
        middle = (566.0, 312.0)

        platform_id = self.helper.get_above_which_platform(self.helper.get_self_position()) #不在平台 = -1 在平台回傳平台的值
        
        my_id = self.helper.get_self_id()
        position = (0,0)
        max = 0
        max_id = 0
        for i in range(4):
            if i != my_id and self.helper.get_other_life(i) > max :
                position = self.helper.get_other_position(i)
                max = self.helper.get_other_life(i)
                max_id = i

        # get distance to other player
        distance = self.helper.get_all_player_distance()

        if self.helper.get_self_can_attack() and\
            distance[max_id] < self.helper.get_self_attack_radius():
            return AI_DIR_ATTACK

        if self.helper.get_self_can_attack():
            return self.helper.walk_to_position( (position[0], position[1]) )
        elif self.helper.get_nearest_specific_item_position(6)!=None and self.helper.get_above_which_platform(self.helper.get_nearest_specific_item_position(6)) != -1:
            return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(6))    

        #------------以下是何時會使用道具 by 宇倫 + 昱承瑜芳婷馨------------
        
        #找到最靠近的人(不用min是因為會找到自己與自己的距離(== 0))
        dis_nearest = dis_others[my_ID]
        
        for i in dis_others:
            if i == None : 
                continue
            elif i < dis_nearest and i != 0:
                dis_nearest = i

        #dis_nearest = 最靠近自己的人的距離
        if now_item != 0:
            if now_item == ZAP_ZAP_ZAP : # 閃電
                if dis_nearest <= self.helper.get_zap_zap_zap_effect_range()-10 :
                    return AI_DIR_USE_ITEM
                else: #不夠靠近就過去找人用
                    return self.helper.walk_to_position(self.helper.get_nearest_player_position())

            elif now_item == BANANA_PISTOL : #距離夠接近就使用香蕉手槍
                if dis_nearest < 70:
                    return AI_DIR_USE_ITEM 
                else: #不夠靠近就過去找人用
                    return self.helper.walk_to_position(self.helper.get_nearest_player_position())
            elif now_item == CANCER_BOMB: #距離夠接近就使用香蕉手槍
                if dis_nearest < 70:
                    return AI_DIR_USE_ITEM
                else: #不夠靠近就過去找人用
                    return self.helper.walk_to_position(self.helper.get_nearest_player_position())
            
            else :
                return AI_DIR_USE_ITEM 

        #------------以上是何時會使用道具------------

        if my_pos[1] < 50:
            return AI_DIR_RIGHT
        elif my_pos[1] > 580:
            return AI_DIR_LEFT 
        elif my_pos[0] < 50:
            return  AI_DIR_LEFT
        elif my_pos[0] > 1090:
            return  AI_DIR_JUMP

        if platform_id == -1: # 一離開平台就回到最近的平台(防掉落)
            closest_land_vec = self.helper.get_position_vector_to_closest_land()
            closest_land_pos = (my_pos[0] + closest_land_vec[0], my_pos[1] + closest_land_vec[1])
            return self.helper.walk_to_position(closest_land_pos)

        #------------以下是躲開香蕉皮、黑洞 by 宥程---------

        pos_banana = self.helper.get_all_drop_banana_peel_position() #get bananas position
        pos_bh = self.helper.get_all_drop_big_black_hole_position() #get black hole position

        for banana in pos_banana:
            if self.helper.get_distance(my_pos, banana) < 60: #self.helper.get_self_radius()+10: #取得香蕉皮與我的距離
                if my_pos[0] > banana[0]: #如果我的x座標大於香蕉的x座標
                    return AI_DIR_RIGHT_JUMP #往右跳
                elif my_pos[0] < banana[0]: #如果我的x座標小於香蕉的x座標
                    return AI_DIR_LEFT_JUMP #往左跳
        for bh in pos_bh:
            if self.helper.get_distance(my_pos, bh) < 200: #取得香蕉皮與我的距離
                if my_pos[0] > bh[0]: #如果我的x座標大於bh的x座標
                    return AI_DIR_RIGHT_JUMP #往右跳
                elif my_pos[0] < bh[0]: #如果我的x座標小於bh的x座標
                    return AI_DIR_LEFT_JUMP #往左跳

        #------------以下是躲開香蕉皮、黑洞 by 宥程---------


        #------------以下是躲開炸彈 by 怡蓁如軒舒婷高敏----------

        bomb_position = self.helper.get_all_drop_cancer_bomb_position() #獲得炸彈的位置
        bomb_radius = self.helper.get_cancer_bomb_effect_radius() #獲得炸彈的攻擊半徑
        if len(bomb_position) > 0: #有炸彈 (bomb_position != [])
            for i in range(len(bomb_position)): #逃離每個炸彈
                bomb_distance = self.helper.get_distance(bomb_position[i], my_pos)#獲得該炸彈和我的距離
                #逃離該炸彈的攻擊半徑
                if bomb_distance <= bomb_radius:
                    all_platform_position = self.helper.get_platform_position()#獲得所有平台的位置
                    which_platform = self.helper.get_above_which_platform(bomb_position[i])#獲得炸彈所在的平台位置
                #移動至炸彈所在平台以外的平台
                    for j in range(len(all_platform_position)):
                        if all_platform_position[j] == which_platform:
                            return self.helper.walk_to_position(all_platform_position[j + 1][0])
                        else:
                            return self.helper.walk_to_position(all_platform_position[j][0])
                            
        #------------以上是躲開炸彈----------            

        
        #------------以下是沒道具時撿道具的順序 by 昱承瑜芳婷馨--------------

        if my_volt >= 90:  #電壓過高
            if len(self.helper.get_all_rainbow_grounder_position()) != 0:   #如果有接地器優先撿
                return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(RAINBOW_GROUNDER))
        else :  #電壓不高時撿道具順序 : 無敵電池->閃電->炸彈->香蕉手槍->黑洞
            if len(self.helper.get_all_invincible_battery_position()) != 0:
                return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(INVINCIBLE_BATTERY))
            elif len(self.helper.get_all_zap_zap_zap_position()) != 0:
                return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(ZAP_ZAP_ZAP))
            elif len(self.helper.get_all_cancer_bomb_position()) != 0:
                return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(CANCER_BOMB))
            elif len(self.helper.get_all_banana_pistol_position()) != 0:
                return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(BANANA_PISTOL))
            elif len(self.helper.get_all_big_black_hole_position()) != 0:
                return self.helper.walk_to_position(self.helper.get_nearest_specific_item_position(BIG_BLACK_HOLE))
        
        #------------以上是沒道具時撿道具的順序--------------
        
        

        #------------以下是攻擊最高電壓的玩家 by 哲睿----------------

        highv_ID = self.helper.get_highest_voltage_player()  #最高電壓的玩家的ID(自己除外且若相同則回傳ID值較小的玩家)
        highv_volt = self.helper.get_other_voltage(highv_ID)
        highv_speed = self.helper.get_other_normal_speed(highv_ID) #電壓最高玩家之移動速度
        highv_pos = self.helper.get_other_position(highv_ID) #最高玩家之位置

        if my_volt < highv_volt and highv_volt > 80:
            if self.helper.get_other_player_distance(highv_ID) >= self.helper.get_self_attack_radius(): #離最高電壓玩家距離 >  自身攻擊範圍
                return self.helper.walk_to_position(highv_pos) #往電壓最高玩家移動
            else: #離最高電壓玩家距離 <= 自身攻擊範圍
                return AI_DIR_ATTACK

        #-------------以上是攻擊最高電壓的玩家----------------