import imp, traceback
import pygame as pg
import Const
from API.helper import Helper
from Events.EventManager import *
import Model.Model

class Interface(object):
    def __init__(self, ev_manager, model : Model.Model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.model = model
        self.player_AI = {}
        self.is_init_AI = False

    def notify(self, event: BaseEvent):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, EventEveryTick):
            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_PLAY:
                self.API_play()
        elif isinstance(event, EventQuit):
            pass
        elif isinstance(event, EventInitialize):
            self.initialize()

    def API_play(self):
        for player in self.model.players:
            if player.is_AI:
                AI_dir = self.player_AI[player.player_id].decide()
                if AI_dir == 0:
                    self.ev_manager.post(EventPlayerMove(player.player_id, 'left'))
                elif AI_dir == 1:
                    self.ev_manager.post(EventPlayerMove(player.player_id, 'right'))
                elif AI_dir == 2:
                    self.ev_manager.post(EventPlayerJump(player.player_id))
                elif AI_dir == 3:
                    self.ev_manager.post(EventPlayerAttack(player.player_id)) 
                elif AI_dir == 4:
                    self.ev_manager.post(EventPlayerPickItem(player.player_id))
                elif AI_dir == 5:
                    self.ev_manager.post(EventPlayerUseItem(player.player_id))

    def initialize(self):
        if self.is_init_AI:
            return
        self.is_init_AI = True
        
        for player in self.model.players:
            if player.player_name == "manual":
                continue
            # load TeamAI .py file
            try:
                loadtmp = imp.load_source('', "./C:/code/Challenge2020/API/team_AI.py")
            except:
                self.load_msg(str(player.player_id), player.player_name, "AI can't load")
                player.player_name, player.is_AI = "Error", False
                continue
            self.load_msg(str(player.player_id), player.player_name, "Loading")
            # init TeamAI class
            try:
                print(player.player_id)
                self.player_AI[player.player_id] = loadtmp.TeamAI(Helper(self.model, player.player_id))
            except:
                self.load_msg(str(player.player_id), player.player_name, "AI init crashed")
                traceback.print_exc()
                player.player_name, player.is_AI = "Error", False
                continue
            self.load_msg(str(player.player_id), player.player_name, "Successful to Load")

    def load_msg(self, player_id, player_name ,msg):
        print(f"[{str(player_id)}] team_{player_name}.py: {msg}")
