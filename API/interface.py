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
            if player.is_AI and player.is_alive():
                AI_dir = self.player_AI[player.player_id].decide()
                if AI_dir == 0:
                    self.ev_manager.post(EventPlayerMove(player.player_id, 'left'))
                elif AI_dir == 1:
                    self.ev_manager.post(EventPlayerMove(player.player_id, 'right'))
                elif AI_dir == 2:
                    self.ev_manager.post(EventPlayerJump(player.player_id))
                elif AI_dir == 3:
                    self.ev_manager.post(EventPlayerMove(player.player_id, 'left'))
                    self.ev_manager.post(EventPlayerJump(player.player_id))
                elif AI_dir == 4:
                    self.ev_manager.post(EventPlayerMove(player.player_id, 'right'))
                    self.ev_manager.post(EventPlayerJump(player.player_id))
                elif AI_dir == 5 and player.can_attack():
                    self.ev_manager.post(EventPlayerAttack(player.player_id))
                elif AI_dir == 6 and player.has_item():
                    self.ev_manager.post(EventPlayerItem(player.player_id))
                elif AI_dir == 7:
                    pass

    def initialize(self):
        if self.is_init_AI:
            return
        self.is_init_AI = True

        for player in self.model.players:
            if player.player_name == "manual":
                continue
            # load TeamAI .py file
            # TODO: change the path
            try:
                loadtmp = imp.load_source('', f"./AI/team_{player.player_name}.py")
            except:
                self.load_msg(str(player.player_id), player.player_name, "AI can't load")
                player.player_name, player.is_AI = "Error", False
                continue
            self.load_msg(str(player.player_id), player.player_name, "Loading")
            # init TeamAI class
            try:
                self.player_AI[player.player_id] = loadtmp.TeamAI(Helper(self.model, player.player_id))
            except:
                self.load_msg(str(player.player_id), player.player_name, "AI init crashed")
                traceback.print_exc()
                player.player_name, player.is_AI = "Error", False
                continue
            try:
                player.enhance(self.player_AI[player.index].enhancement)
            except:
                pass
            self.load_msg(str(player.player_id), player.player_name, "Successful to Load")

    def load_msg(self, player_id, player_name ,msg):
        print(f"[{str(player_id)}] team_{player_name}.py: {msg}")
