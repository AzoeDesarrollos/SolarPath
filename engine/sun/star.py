from math import pi, sin, cos, tan, atan2, asin, sqrt, acos, radians
from pygame import Surface, SRCALPHA, draw
from engine.globs import Renderer, SpriteHandler
from pygame.sprite import Sprite


class Star(Sprite):
    radius = 696340
    is_observer = False
    parent = None

    name = "Star"

    def set_parent(self, parent):
        self.parent = parent

    def __init__(self, radius):
        super().__init__()
        self.image = Surface((radius * 2, radius * 2), SRCALPHA)
        self.rect = self.image.get_rect()
        draw.circle(self.image, (255, 255, 0), self.rect.center, radius)

        Renderer.add_sprite(self)
        SpriteHandler.add_sprite(self)

    def update(self, *args, **kwargs):
        pass

    def move(self, dx, dy):
        pass

    def show(self):
        pass

    def hide(self):
        pass

    @staticmethod
    def mean_anomaly(day_frac):
        return 2 * pi * day_frac

    @staticmethod
    def true_anomaly(m, e):
        e_anom = m + e * sin(m) * (1 + e * cos(m))
        v = 2 * atan2(sqrt(1 + e) * sin(e_anom / 2),
                      sqrt(1 - e) * cos(e_anom / 2))
        return v

    @staticmethod
    def equation_of_time(m, ls, e, obliquity_rad):
        e_term = -2 * e * sin(m)
        obl_term = tan(obliquity_rad / 2) ** 2 * sin(2 * ls)
        return e_term + obl_term

    @staticmethod
    def declination(ls, obliquity_rad):
        return asin(sin(obliquity_rad) * sin(ls))

    @staticmethod
    def _solar_azimuth(latitude, hour_angle, decl, altitude):
        phi = radians(latitude)
        cos_az = (sin(decl) - sin(phi) * sin(altitude)) / (cos(phi) * cos(altitude))
        cos_az = max(-1, min(1, cos_az))
        az = acos(cos_az)
        if hour_angle > 0:
            az = 2 * pi - az
        return az

    def _small_angle_approximation(self, distance_km):
        diameter = 2 * self.radius
        angle_arcsec = (diameter * 206265) / distance_km
        angle_rad = angle_arcsec / 206265
        return angle_rad

    def get_solar_xy(self, planet, latitude, hour_angle, decl, distance_km=149_597_870):
        alt = planet.solar_altitude(latitude, hour_angle, decl)
        solar_radius_rad = self._small_angle_approximation(distance_km) / 2

        if alt < -solar_radius_rad:
            return None

        phi = radians(latitude)
        cos_az = (sin(decl) - sin(phi) * sin(alt)) / (cos(phi) * cos(alt))
        cos_az = max(-1, min(1, cos_az))  # evitar errores de dominio
        az = acos(cos_az)
        if hour_angle > 0:
            az = 2 * pi - az

        x = cos(alt) * sin(az)
        y = sin(alt)
        return x, y


Star(8)