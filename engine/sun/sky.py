from engine.globs import WIDTH, HEIGHT, Renderer, SpriteHandler
from pygame.sprite import Sprite
from pygame import draw, Surface
from math import degrees


class Sky(Sprite):
    is_observer = False
    parent = None
    name = "Sky"

    def __init__(self):
        super().__init__()
        self.image = Surface([WIDTH, HEIGHT // 2 + 100])
        self.rect = self.image.get_rect()

        Renderer.add_sprite(self)
        SpriteHandler.add_sprite(self)

    def set_parent(self, parent):
        self.parent = parent

    @staticmethod
    def interpolate_color(c1, c2, t):
        return (
            int(c1[0] * (1 - t) + c2[0] * t),
            int(c1[1] * (1 - t) + c2[1] * t),
            int(c1[2] * (1 - t) + c2[2] * t)
        )

    def draw_dynamic_sky(self, altura, dy):
        alt_deg = degrees(altura)
        if alt_deg <= -6:
            top, bottom = (5, 5, 20), (10, 10, 30)
        elif -6 < alt_deg <= 5:
            mix = (alt_deg + 6) / 11
            top = self.interpolate_color((5, 5, 20), (200, 100, 50), mix)
            bottom = self.interpolate_color((10, 10, 30), (255, 120, 60), mix)
        elif 5 < alt_deg <= 30:
            mix = (alt_deg - 5) / 25
            top = self.interpolate_color((200, 100, 50), (100, 160, 255), mix)
            bottom = self.interpolate_color((255, 120, 60), (180, 220, 255), mix)
        else:
            top, bottom = (100, 160, 255), (180, 220, 255)
        for cy in range(HEIGHT):
            ratio = dy / HEIGHT
            r = int(top[0] * (1 - ratio) + bottom[0] * ratio)
            g = int(top[1] * (1 - ratio) + bottom[1] * ratio)
            b = int(top[2] * (1 - ratio) + bottom[2] * ratio)
            draw.line(self.image, (r, g, b), (0, cy), (WIDTH, cy))

    def update(self):
        pass


Sky()