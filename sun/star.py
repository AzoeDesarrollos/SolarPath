from pygame.sprite import Sprite
from pygame import Surface, SRCALPHA, draw

class Star(Sprite):
    radius = 696340

    def __init__(self, radius):
        super().__init__()
        self.image = Surface((radius * 2, radius * 2), SRCALPHA)
        self.rect = self.image.get_rect()
        draw.circle(self.image, (255, 255, 0), self.rect.center, radius)

    def update(self, *args, **kwargs):
        pass

    def move(self, dx, dy):
        pass

    def show(self):
        pass

    def hide(self):
        pass