from engine.globs import WIDTH, HEIGHT, Renderer, SpriteHandler
from math import degrees, sin, radians
from pygame import draw, Surface
from .base_class import Base


class Sky(Base):
    is_observer = False
    parent = None
    name = "Sky"

    def __init__(self):
        super().__init__()
        self.image = Surface([WIDTH, HEIGHT // 2 + 100])
        self.rect = self.image.get_rect()

        Renderer.add_sprite(self)
        SpriteHandler.add_sprite(self)

    @staticmethod
    def interpolate_color(c1, c2, t):
        return (
            int(c1[0] * (1 - t) + c2[0] * t),
            int(c1[1] * (1 - t) + c2[1] * t),
            int(c1[2] * (1 - t) + c2[2] * t)
        )

    def draw_dynamic_sky(self, altura):
        alt_deg = degrees(altura)

        # Elegir colores según altitud solar
        if alt_deg <= -6:
            sky_top, sky_bottom = (5, 5, 20), (10, 10, 30)
        elif -6 < alt_deg <= 5:
            mix = (alt_deg + 6) / 11
            sky_top = self.interpolate_color((5, 5, 20), (200, 100, 50), mix)
            sky_bottom = self.interpolate_color((10, 10, 30), (255, 120, 60), mix)
        elif 5 < alt_deg <= 30:
            mix = (alt_deg - 5) / 25
            sky_top = self.interpolate_color((200, 100, 50), (100, 160, 255), mix)
            sky_bottom = self.interpolate_color((255, 120, 60), (180, 220, 255), mix)
        else:
            sky_top, sky_bottom = (100, 160, 255), (180, 220, 255)

        # Color central (donde el Sol está)
        sun_color = sky_bottom

        # Determinar posición vertical del Sol (en píxeles)
        sun_y_px = HEIGHT / 2 - sin(radians(alt_deg)) * (HEIGHT / 2)

        fade_range = HEIGHT * 0.9  # controla el ancho del gradiente
        for cy in range(HEIGHT):
            distance = abs(cy - sun_y_px)
            ratio = min(distance / fade_range, 1)

            # Interpolar entre el color solar y el color del cielo (gradual)
            r = int(sun_color[0] * (1 - ratio) + sky_top[0] * ratio)
            g = int(sun_color[1] * (1 - ratio) + sky_top[1] * ratio)
            b = int(sun_color[2] * (1 - ratio) + sky_top[2] * ratio)
            draw.line(self.image, (r, g, b), (0, cy), (WIDTH, cy))

    def update(self):
        star = self.parent.get_sprite('Star')
        self.draw_dynamic_sky(star.altitude)


Sky()