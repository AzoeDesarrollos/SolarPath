import time
from math import pi


class PlanetTime:
    def __init__(self, day_length_seconds=86400, year_length_days=365.25):
        self.day_length_seconds = day_length_seconds
        self.year_length_days = year_length_days
        self.current_time = 0.0  # en fracción del día
        self.current_day = 0  # día del año
        self.real_time_mode = False
        self.last_real_timestamp = time.time()
        self.time_speed = 100.0  # 60x en modo simulado

    def toggle_mode(self):
        self.real_time_mode = not self.real_time_mode
        self.last_real_timestamp = time.time()

    def update(self, delta_time):
        if self.real_time_mode:
            now = time.time()
            elapsed = now - self.last_real_timestamp
            self.last_real_timestamp = now
            day_fraction = elapsed / self.day_length_seconds
        else:
            day_fraction = delta_time #* self.time_speed / self.day_length_seconds

        self.current_time += day_fraction

        while self.current_time >= 1.0:
            self.current_time -= 1.0
            self.current_day = (self.current_day + 1) % int(self.year_length_days)

    def get_hour_angle(self):
        return self.current_time  #(self.current_time - 0.5) * 2 * pi  # desde -π a π

    def get_current_day(self):
        return self.current_day