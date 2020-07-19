import pygame as pg
import sys

from Events.EventManager import EventManager
from Model.Model_no_display import GameEngine
from Controller.Controller import Controller
from View.View import GraphicalView
from View.sounds import Audio
import API.interface
import numpy as np
import random

def main(argv):
    np.random.seed(2020)
    random.seed(2021)
    ev_manager = EventManager()
    model      = GameEngine(ev_manager, argv[1:5])
    #controller = Controller(ev_manager, model)
    #view       = GraphicalView(ev_manager, model)
    interface  = API.interface.Interface(ev_manager, model)
    #sound      = Audio(ev_manager, model)
    return model.run()

if __name__ == "__main__":
	main(sys.argv)
