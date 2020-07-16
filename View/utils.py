import pygame as pg

class PureText:
    def __init__(self, text, size, font, color, **pos):
        '''
        pos: refer to the attributes of pg.Rect
        '''
        self.font = pg.font.Font(font, size)
        self.text_surface = self.font.render(text, True, pg.Color(color))
        self.pos_rect = self.text_surface.get_rect(**pos)

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)

class MutableText:
    def __init__(self, font, color):
        '''
        pos: refer to the attributes of pg.Rect
        '''
        self.color = color
        self.font = font

    def draw(self, text, screen, **pos):
        self.text_surface = self.font.render(text, True, self.color)
        self.pos_rect = self.text_surface.get_rect(**pos)
        screen.blit(self.text_surface, self.pos_rect)

    def draw_align_right(self, text, screen, pos):
        self.text_surface = self.font.render(text, True, self.color)
        self.pos_rect = self.text_surface.get_rect()
        self.pos_rect.topright = pos
        screen.blit(self.text_surface, self.pos_rect)


__image_cache = dict()
def load_image(path):
    global __image_cache

    if path not in __image_cache:
        __image_cache[path] = pg.image.load(path)

    return __image_cache[path].copy()


def scaled_surface(surface, scale):
    try:
        return pg.transform.smoothscale(surface, (int(scale * surface.get_width()), int(scale * surface.get_height())))
    except:
        return pg.transform.scale(surface, (int(scale * surface.get_width()), int(scale * surface.get_height())))

