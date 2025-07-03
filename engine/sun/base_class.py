from pygame.sprite import Sprite
from engine.globs import Renderer


class Base(Sprite):
    is_observer = False
    parent = None
    name = None

    def __init__(self):
        super().__init__()

    def set_parent(self, parent):
        self.parent = parent

    def __repr__(self):
        return self.name

    def show(self):
        Renderer.add_sprite(self)

    def hide(self):
        Renderer.del_sprite(self)