import pygame as pg

from EventManager import EventManager
from Model import GameEngine
from Controller import Controller
from View import GraphicalView


def main():
    pg.init()
    ev_manager = EventManager()
    model      = GameEngine(ev_manager)
    controller = Controller(ev_manager, model)
    view       = GraphicalView(ev_manager, model)

    model.run()


if __name__ == "__main__":
    main()
