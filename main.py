import pygame as pg

from Events.EventManager import EventManager
from Model.Model import GameEngine
from Controller.Controller import Controller
from View.View import GraphicalView


def main():
    ev_manager = EventManager()
    model      = GameEngine(ev_manager)
    controller = Controller(ev_manager, model)
    view       = GraphicalView(ev_manager, model)

    model.run()

if __name__ == "__main__":
    main()
