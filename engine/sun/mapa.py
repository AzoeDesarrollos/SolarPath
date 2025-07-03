from engine.globs import SpriteHandler
from pygame import image, mask
from .base_class import Base
from os import path, getcwd


class Mapa(Base):
    is_observer = False
    parent = None
    name = 'mapa'

    def __init__(self):
        super().__init__()
        surface = image.load(path.join(getcwd(), 'data', 'mapa.png')).convert()
        self.mask = mask.from_threshold(surface, (255, 255, 255), (1, 1, 1))
        self.width, self.height = surface.get_width(), surface.get_height()
        SpriteHandler.add_sprite(self)

    def is_land(self, lat, lon):
        x = int((lon + 180) / 360 * self.width) % self.width
        y = int((90 - lat) / 180 * self.height) % self.height
        try:
            return self.mask.get_at((x, y)) == 1
        except IndexError:
            return False
Mapa()