import pygame as pg


try:
    pg.mixer.init()
    SOUND_ENABLE = True

except pg.error:
    SOUND_ENABLE = False
    print('audio disabled')
