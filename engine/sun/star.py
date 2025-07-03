from math import pi, sin, cos, tan, atan2, asin, sqrt, acos, radians
from engine.globs import Renderer, SpriteHandler, WIDTH, HEIGHT
from pygame import Surface, SRCALPHA, draw
from pygame.transform import smoothscale
from .base_class import Base


class Star(Base):
    radius = 696340
    name = "Star"
    altitude = 0

    def __init__(self, radius):
        super().__init__()
        self.original_image = Surface((radius * 2, radius * 2), SRCALPHA)
        self.rect = self.original_image.get_rect()
        draw.circle(self.original_image, (255, 255, 0), self.rect.center, radius)
        self.image = self.original_image

        self.layer = 1

        Renderer.add_sprite(self)
        SpriteHandler.add_sprite(self)

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

    def _small_angle_approximation(self, distance_km):
        diameter = 2 * self.radius
        angle_arcsec = (diameter * 206265) / distance_km
        angle_rad = angle_arcsec / 206265
        return angle_rad

    def apparent_radius_px(self, distance_km, altitude_deg, observer_sky_radius_px):
        # Paso 1: calcular ángulo real en radianes
        angle_rad = self._small_angle_approximation(distance_km)

        # Paso 2: tamaño en pixeles base
        base_px = sin(angle_rad / 2) * observer_sky_radius_px

        # Paso 3: multiplicador visual dinámico según altitud (simula ilusión lunar)
        # El multiplicador es mayor cerca del horizonte (altitud 0°),
        # y se reduce a 1 cerca del cenit (90°).
        alt_factor = max(0, cos(radians(altitude_deg)))  # 1 en horizonte, 0 en cenit
        visual_multiplier = 3 + 2 * alt_factor  # entre 3 y 5

        # Paso 4: aplicar multiplicador y mínimo
        return max(4, base_px * visual_multiplier)

    def get_solar_xy(self, planet, observer, distance_km=149597870):

        latitude = observer.latitude
        current_day = planet.get_current_day()
        m = self.mean_anomaly(current_day / planet.orbital_period)
        ls = self.true_anomaly(m, planet.eccentricity)
        decl = self.declination(ls, planet.epsilon)

        hour_angle = planet.get_hour_angle()
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

    def update(self):
        center_x, center_y = WIDTH // 2, HEIGHT // 2 + 100
        planet = self.parent.get_sprite('Planet')
        observer = self.parent.get_sprite('Observer')

        result, altitude = planet.sun_position()
        self.altitude = altitude
        px, py = 0, 0
        if result:
            self.show()  # hace aparecer al sol cuando está por encima del horizonte
            x, y = result
            multiplier = 1 if observer.facing_north else -1
            px = center_x + int(x * observer.sky_radius_px * multiplier)
            py = center_y - int(y * observer.sky_radius_px)
            self.rect.center = px, py
        else:
            self.hide()  # hace desaparecer al sol cuando está por debajo del horizonte.

        #     if show_arc:
        #         path.append((px, py))
        # else:
        #     if show_arc:
        #         path.clear()
        # 1. Obtener la distancia actual
        distance_km = 149597870  # asumimos que esta función ya existe
        # 3. Convertir ese ángulo en píxeles en pantalla
        sky_radius = observer.sky_radius_px  # por ejemplo, 300 px
        # 4. Forzar un mínimo visible
        radius_px = self.apparent_radius_px(distance_km, altitude, sky_radius)

        # 5. Redimensionar la imagen
        new_size = int(radius_px * 1.5)
        self.image = smoothscale(self.original_image, (new_size, new_size))
        self.rect = self.image.get_rect(center=(px, py))


Star(8)
