from pygame import display, init as pg_init, font
from pygame.sprite import LayeredUpdates
from .constantes import *
from math import pi


class Renderer:

    @classmethod
    def init(cls):
        pg_init()
        cls.screen = display.set_mode((WIDTH, HEIGHT))
        display.set_caption("Movimiento Solar Anual")
        cls.contents = LayeredUpdates()
        cls.fuente = font.SysFont('Verdana', 18)

        cls.east_text = cls.fuente.render("Este", True, (0, 0, 0))
        cls.west_text = cls.fuente.render("Oeste", True, (0, 0, 0))

    @classmethod
    def add_sprite(cls, sprite):
        if sprite not in cls.contents.sprites():
            cls.contents.add(sprite)

    @classmethod
    def del_sprite(cls, sprite):
        if sprite in cls.contents.sprites():
            cls.contents.remove(sprite)

    @classmethod
    def get_sprite(cls, name):
        for sprite in cls.contents.sprites():
            if sprite.name == name:
                return sprite

    @classmethod
    def update(cls):
        rect_list = cls.contents.draw(cls.screen)
        planet = cls.get_sprite('Planet')
        observer = cls.get_sprite('Observer')
        latitude_deg = observer.latitude
        current_day = planet.get_current_day()

        # Hora solar estimada
        hour_angle = planet.get_hour_angle()
        solar_hour = (hour_angle / (2 * pi)) * 24 + 12
        solar_hour = solar_hour % 24
        hours = int(solar_hour)
        minutes = int((solar_hour - hours) * 60)
        # abs_lat = abs(latitude_deg % 360)
        lat_display = planet.normalize_latitude(latitude_deg)[0]

        # east_label = cls.east_text if observer.facing_north else cls.west_text
        # west_label = cls.west_text if observer.facing_north else cls.east_text
        # y = (HEIGHT // 2 + 100) + 10
        # cls.screen.blit(east_label, (WIDTH - 70, y))  # derecha
        # cls.screen.blit(west_label, (10, y))  # izquierda

        period = planet.orbital_period
        day_text = cls.fuente.render(f"Día del año: {current_day} / {int(period)}", True, 'white')
        time_text = cls.fuente.render(f"Hora solar: {hours:02d}:{minutes:02d}", True, 'white')
        lat_text = cls.fuente.render(f"Latitud: {lat_display:.1f}°", True, (255, 255, 255))
        mode_text = cls.fuente.render(f"Modo: {'Real' if planet.real_time_mode else 'Simulado'}", True, 'white')
        rect_a = cls.screen.blit(day_text, (10, 10))
        rect_b = cls.screen.blit(time_text, (10, rect_a.bottom))
        rect_c = cls.screen.blit(lat_text, (10, rect_b.bottom))
        cls.screen.blit(mode_text, (10, rect_c.bottom))
        rect_list.extend([rect_a])
        rect_list.extend([rect_b])
        rect_list.extend([rect_c])

        display.update(rect_list)


Renderer.init()
