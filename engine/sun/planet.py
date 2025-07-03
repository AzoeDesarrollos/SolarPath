from engine.globs import WIDTH, HEIGHT, Renderer, SpriteHandler, draw_paralelograms
from math import radians, pi, asin, sin, cos
from pygame import Surface, draw
from datetime import datetime
from .base_class import Base


class Planet(Base):
    obliquity_deg = 23.44
    eccentricity = 0.0167
    orbital_period = 365.25
    name = "Planet"

    def __init__(self, horizon_y):
        super().__init__()
        self.image = Surface([WIDTH, horizon_y])
        self.color = [0, 200, 100]
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=[0, horizon_y])

        self.layer = 2
        self.time_speed = 0.1
        self.real_time_mode = False

        self.current_time = 0.0
        self.previous_time = 0.0
        self.current_day = 0

        Renderer.add_sprite(self)
        SpriteHandler.add_sprite(self)

        self.drawn = False

    @property
    def epsilon(self):
        return radians(self.obliquity_deg)

    @staticmethod
    def get_divergence(x: float, y: float, base_divergence=1.0, amplitude=0.5, frequency=0.005):
        """simula ondas de terreno"""

        return base_divergence + amplitude * sin(x * frequency + y * frequency)

    def draw_mode7_grid(self, num_longitudinal=30, num_latitudinal=30, divergence_factor=10):
        observer = self.parent.get_sprite('Observer')
        center_x = self.rect.centerx
        ecuaciones_long = []
        ecuaciones_lat = []
        # --- Líneas longitudinales (sin cambios) ---
        # base_divergence = self.get_divergence(observer.y)
        divergence = divergence_factor if observer.facing_north else -divergence_factor
        x_start_linea_fuga = center_x - self.rect.width / 2
        separacion_lineas = self.rect.width / num_longitudinal

        line_color = 0, 0, 0
        for i in range(1, num_longitudinal + 1):
            x_start = x_start_linea_fuga + i * separacion_lineas
            x_offset = (x_start - center_x) * divergence
            x_end = center_x + x_offset
            x1, x2 = x_start, x_end
            y1, y2 = 0, 600
            if x2 - x1 != 0:
                m = (y2 - y1) / (x2 - x1)
                n = y1 - m * x1
            else:
                m = 0
                n = y2 - m * x2

            ecuaciones_long.append([round(m, 3), round(n, 3)])
            draw.line(self.image, line_color, (x1, y1), (x2, y2))

        # --- Líneas latitudinales (scroll vertical realista) ---
        spacing = 20  # espaciado entre líneas

        # Usar scroll_y para mover el piso
        scroll_y = observer.scroll_y % spacing  # solo el desfase visible
        base_y = -scroll_y

        for i in range(num_latitudinal):
            y = base_y + i * spacing
            ecuaciones_lat.append(y)
            draw.line(self.image, line_color, (0, y), (WIDTH, y))

        draw_paralelograms(ecuaciones_long, ecuaciones_lat, self.image)

    def draw(self):
        observer = self.parent.get_sprite('Observer')
        if observer.moviendose or not self.drawn:
            self.image.fill(self.color)
            self.draw_mode7_grid()
            self.drawn = True

    def update_time(self, delta_time):
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

    def sun_position(self):
        star = self.parent.get_sprite('Star')
        observer = self.parent.get_sprite('Observer')
        latitude_deg = observer.latitude

        current_day = self.get_current_day()
        m = star.mean_anomaly(current_day / self.orbital_period)
        ls = star.true_anomaly(m, self.eccentricity)
        decl = star.declination(ls, self.epsilon)
        eot = star.equation_of_time(m, ls, self.eccentricity, self.epsilon)

        hour_angle = self.get_hour_angle()  # Ya incluye la hora local
        if not self.real_time_mode:
            hour_angle = self.get_hour_angle() - eot  # Solo se corrige en modo simulado
        result = star.get_solar_xy(self, observer)
        altitude = self.solar_altitude(latitude_deg, hour_angle, decl)
        return result, altitude

    def get_hour_angle(self):
        return self.current_time

    def get_current_day(self):
        return self.current_day

    def toggle_mode(self):
        self.real_time_mode = not self.real_time_mode

    def solar_altitude(self, latitude, hour_angle, decl):
        latitude = self.normalize_latitude(latitude)[0]
        phi = radians(latitude)
        return_value = asin(sin(phi) * sin(decl) + cos(phi) * cos(decl) * cos(hour_angle))
        return return_value

    def lon_to_map_x(self, lon_deg):
        mapa = self.parent.get_sprite('mapa')
        if lon_deg > 180:
            lon_deg -= 360
        elif lon_deg < -180:
            lon_deg += 360
        shifted_lon = (lon_deg + 180) % 360
        x = int(shifted_lon / 360 * mapa.width)
        return x

    def lat_to_map_y(self, lat_deg):
        """
        Convierte una latitud en grados a la coordenada Y en la imagen del mapa.
        """
        mapa = self.parent.get_sprite('mapa')
        lat = max(-90, min(90, lat_deg))
        y = int((90 - lat) / 180 * mapa.height)
        return y

    @staticmethod
    def screen_x_to_lon(cx, screen_width, observer_lon_deg):
        lon_offset = ((cx - screen_width // 2) / screen_width) * 360
        lon = observer_lon_deg + lon_offset
        if lon > 180:
            lon -= 360
        elif lon < -180:
            lon += 360
        return lon

    @staticmethod
    def normalize_latitude(lat):
        lat = lat % 360
        if lat > 180:
            lat -= 360
        facing_north = True
        if lat > 90:
            lat = 180 - lat
            facing_north = False
        elif lat < -90:
            lat = -180 - lat
            facing_north = False
        return lat, facing_north

    @staticmethod
    def normalize_longitude(lon):
        lon = lon % 360
        if lon > 180:
            lon -= 360
        return lon

    def update(self):
        observer = self.parent.get_sprite('Observer')
        delta_time = observer.delta_time
        self.update_time(delta_time)
        self.draw()


Planet(HEIGHT // 2 + 100)
