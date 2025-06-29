from globs.constantes import WIDTH, HEIGHT
from sun.funciones import *
from pygame.sprite import Sprite
from pygame import Surface, draw
from math import radians, pi
from datetime import datetime


class Planet(Sprite):
    obliquity_deg = 23.44
    eccentricity = 0.0167
    orbital_period = 365.25

    is_observer = False
    parent = None

    def __init__(self, horizon_y):
        super().__init__()
        self.image = Surface([WIDTH, horizon_y])
        self.color = [0, 200, 100]
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=[0, horizon_y])

        self.time_speed = 0.03
        self.real_time_mode = False

        self.current_time = 0.0
        self.previous_time = 0.0
        self.current_day = 0

    @property
    def epsilon(self):
        return radians(self.obliquity_deg)

    def draw_mode7_grid(self, center_x, latitude_deg,
                        num_longitudinal=30, num_latitudinal=180,
                        apertura_ancho=800, divergence_factor=10):
        # --- Líneas longitudinales (sin cambios) ---
        x_start_linea_fuga = center_x - apertura_ancho / 2
        separacion_lineas = apertura_ancho / num_longitudinal

        line_color = 100, 150, 200
        for i in range(num_longitudinal + 1):
            x_start = x_start_linea_fuga + i * separacion_lineas

            x_offset = (x_start - center_x) * divergence_factor
            x_end = center_x + x_offset
            draw.line(self.image, line_color, (x_start, 0), (x_end, HEIGHT), 1)

        # --- Líneas latitudinales ---
        # Definir espaciado fijo entre líneas
        spacing = 20  # espaciado constante, NO creciente

        # Convertir latitud a factor de desplazamiento
        lat_factor = (latitude_deg + 90) / 180  # de 0 (sur) a 1 (norte)
        max_shift = 400
        shift = (lat_factor - 0.5) * 2 * max_shift  # -400 a +400

        # Centrar la grilla en la línea del horizonte + shift
        base_y = 0 + shift

        # Generar muchas líneas alrededor de base_y, hacia arriba y abajo
        for i in range(-num_latitudinal // 2, num_latitudinal // 2 + 1):
            y = base_y + i * spacing
            if 0 <= y <= HEIGHT:
                draw.line(self.image, line_color, (0, y), (WIDTH, y), 2)

    def draw(self, center_x, latitude_deg):
        self.image.fill(self.color)
        self.draw_mode7_grid(center_x, latitude_deg)
        return self.image

    def update(self, delta_time, **kwargs):
        self.previous_time = self.current_time

        if self.real_time_mode:
            now = datetime.now()
            hora_decimal = now.hour + now.minute / 60 + now.second / 3600
            # Ángulo horario sin corrección (12h = 0)
            hour_angle = (hora_decimal - 12) / 12.0 * pi
            self.current_time = hour_angle
            self.current_day = now.timetuple().tm_yday
        else:
            self.current_time += delta_time * self.time_speed
            self.current_time = ((self.current_time + pi) % (2 * pi)) - pi
            if self.current_time < self.previous_time:
                self.current_day = (self.current_day + 1) % int(self.orbital_period)

    def sun_position(self, latitude_deg, star):
        current_day = self.get_current_day()
        m = mean_anomaly(current_day / self.orbital_period)
        ls = true_anomaly(m, self.eccentricity)
        decl = declination(ls, self.epsilon)
        eot = equation_of_time(m, ls, self.eccentricity, self.epsilon)

        hour_angle = self.get_hour_angle()  # Ya incluye la hora local
        if not self.real_time_mode:
            hour_angle = self.get_hour_angle() - eot  # Solo se corrige en modo simulado
        result = get_solar_xy(latitude_deg, hour_angle, decl, star)
        altitude = solar_altitude(latitude_deg, hour_angle, decl)
        return result, altitude

    def get_hour_angle(self):
        return self.current_time

    def get_current_day(self):
        return self.current_day

    def toggle_mode(self):
        self.real_time_mode = not self.real_time_mode
