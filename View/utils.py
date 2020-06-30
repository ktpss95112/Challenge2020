import pygame as pg
from PIL import Image
import numpy as np
from View.transforms import RGBTransform

class PureText():
    def __init__(self, text, size, font, color, **pos):
        '''
        pos: refer to the attributes of pg.Rect
        '''
        self.font = pg.font.Font(font, size)
        self.text_surface = self.font.render(text, True, pg.Color(color))
        self.pos_rect = self.text_surface.get_rect(**pos)

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)

def scaled_surface(surface, scale):
    '''
    example:
    image = scaled_surface(image, 0.3)
    '''
    try:
        return pg.transform.smoothscale(surface, (int(scale * surface.get_width()), int(scale * surface.get_height())))
    except:
        return pg.transform.scale(surface, (int(scale * surface.get_width()), int(scale * surface.get_height())))


"""
    reference:
    https://stackoverflow.com/questions/38665920/convert-pil-image-into-pygame-surface-image
    https://stackoverflow.com/questions/1616767/pil-best-way-to-replace-color/1616893
"""
def replace_color(path, origin, target):
    im = Image.open(path)
    im = im.convert('RGBA')
    data = np.array(im)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
    # Replace white with red... (leaves alpha values alone...)
    origin_areas = (red == origin[0]) & (green ==  origin[1]) & (blue ==  origin[2]) 
    data[..., :-1][origin_areas.T] = target # Transpose back needed
    im = Image.fromarray(data)
    im2 = pg.image.fromstring(im.tobytes(), im.size, im.mode)
    return im2

def overlay_color(im_path, color,scale ,transparency):
    im = Image.open(im_path)
    im = im.resize((int(im.width*scale), int(im.height*scale)), Image.ANTIALIAS)
    im = im.convert('RGB')
    im1 = RGBTransform().mix_with(color, transparency).applied_to(im)
    #im2 = RGBTransform().multiply_with(color, transparency).applied_to(im)
    #im3 = RGBTransform().desaturate(color, transparency, (0.5, 0.5, 0.5)).applied_to(im)
    mode = im1.mode
    size = im1.size
    data = im1.tobytes()
    im1 = pg.image.fromstring(data, size, mode)
    return im1
