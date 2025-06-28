from pygame import display, init as pg_init
from pygame.sprite import LayeredUpdates
from .constantes import *


class Renderer:

    @classmethod
    def init(cls):
        pg_init()
        cls.screen = display.set_mode((WIDTH, HEIGHT))
        display.set_caption("Movimiento Solar Anual")
        cls.contents = LayeredUpdates()

    @classmethod
    def add_sprite(cls, sprite):
        cls.contents.add(sprite)

    @classmethod
    def del_sprite(cls, sprite):
        if sprite in cls.contents:
            cls.contents.remove(sprite)

    @classmethod
    def update(cls):
        cls.contents.draw(cls.screen)


Renderer.init()