from engine.globs import SpriteHandler
from pygame.sprite import Sprite
from pygame import SRCALPHA, Surface


class Observer(Sprite):
    latitude = -34
    longitude_deg = 0
    sky_radius_px = 400

    is_observer = True
    delta_time = 0

    parent = None

    name = "Observer"

    def __init__(self):
        super().__init__()
        self.image = Surface([1, 1], SRCALPHA)
        self.rect = self.image.get_rect()
        self.x, self.y = 0, 0

        SpriteHandler.add_sprite(self)

    def set_parent(self, parent):
        self.parent = parent

    def move(self, dx, dy):
        self.x = dx
        self.y = dy
        latitude_deg = self.latitude

        latitude_deg += dy * 10 * self.delta_time  # 20 grados por segundo ajustable

        # Asegurar latitud en rango -180 a +180 con rollover
        if latitude_deg > 180:
            latitude_deg -= 360
        elif latitude_deg < -180:
            latitude_deg += 360


Observer()