from engine.globs import SpriteHandler, Renderer
from pygame import SRCALPHA, Surface
from .base_class import Base


class Observer(Base):
    latitude = -34
    true_latitude = latitude
    longitude_deg = 0
    sky_radius_px = 390

    is_observer = True
    delta_time = 0

    parent = None

    name = "Observer"

    moviendose = False

    def __init__(self):
        super().__init__()
        self.image = Surface([1, 1], SRCALPHA)
        self.rect = self.image.get_rect()
        self.x, self.y = 0, 0

        self.vx = 0
        self.vy = 0
        self.facing_north = True

        self.scroll_y = 0
        self.scroll_x = 0

        SpriteHandler.add_sprite(self)
        Renderer.add_sprite(self)

    def moverse(self, vx, vy):
        self.vy = vy
        self.vx = vx
        if vx != 0 or vy != 0:
            self.moviendose = True
        else:
            self.moviendose = False

    def move(self, delta_time):
        planet = self.parent.get_sprite('Planet')

        self.y += self.vy
        self.x += self.vx
        self.delta_time = delta_time

        # Movimiento visual del scroll (más rápido para hacerlo visible)
        self.scroll_y -= self.vy * 100 * delta_time  # Ajustá 2000 si es necesario
        self.scroll_x -= self.vx * 100 * delta_time

        # Movimiento astronómico: latitud lógica
        self.true_latitude += self.vy * 0.2 * delta_time
        self.longitude_deg += self.vx * 0.2 * delta_time  # ← movimiento en longitud

        # Normalizar para mantener en rango [-180, +180]
        self.longitude_deg = planet.normalize_longitude(self.longitude_deg)

        # Derivar latitud visible y orientación
        lat, facing_north = planet.normalize_latitude(self.true_latitude)
        self.latitude = lat
        self.facing_north = facing_north
        # print(f"scroll_y: {self.scroll_y:.2f}, latitude: {self.latitude:.2f}")


Observer()
