import pygame as pg


try:
    pg.mixer.init(22050, -16, 2, 64)
    SOUND_ENABLE = True

except pg.error:
    SOUND_ENABLE = False
    print('audio disabled')
