import pygame as pg
import sys

from Events.EventManager import EventManager
from Model.Model import GameEngine
from Controller.Controller import Controller
from View.View import GraphicalView
from View.sounds import Audio
import API.interface

def main(argv):
    ev_manager = EventManager()
    model      = GameEngine(ev_manager, argv[1:5])
    controller = Controller(ev_manager, model)
    view       = GraphicalView(ev_manager, model)
    interface  = API.interface.Interface(ev_manager, model)
    sound      = Audio(ev_manager, model)
    model.run()

if __name__ == "__main__":
	main(sys.argv)
