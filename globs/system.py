from sun.funciones import *


class System:
    star = None
    planet = None

    @classmethod
    def init(cls, star, planet):
        cls.planet = planet
        cls.star = star

    @classmethod
    def update(cls):
        current_day = cls.planet.get_current_day()
        m = mean_anomaly(current_day / cls.planet.orbital_period)
        ls = true_anomaly(m, cls.planet.eccentricity)
        decl = declination(ls, cls.planet.epsilon)
        eot = equation_of_time(m, ls, cls.planet.eccentricity, cls.planet.epsilon)

        hour_angle = cls.planet.get_hour_angle()  # Ya incluye la hora local
        if not cls.planet.real_time_mode:
            hour_angle = cls.planet.get_hour_angle() - eot  # Solo se corrige en modo simulado
        result = get_solar_xy(latitude_deg, hour_angle, decl, cls.star)
        altitude = solar_altitude(latitude_deg, hour_angle, decl)

        if result:
            x, y = result
            px = center_x + int(x * sky_radius_px)
            py = center_y - int(y * sky_radius_px)