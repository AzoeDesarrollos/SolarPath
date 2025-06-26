import time
from math import pi


class PlanetTime:
    def __init__(self, day_length_seconds=86400, year_length_days=365.25):
        self.day_length_seconds = day_length_seconds
        self.year_length_days = year_length_days
        self.current_time = -pi  # en fracción del día
        self.current_day = 0  # día del año
        self.real_time_mode = False
        self.last_real_timestamp = time.time()
        self.time_speed = 0.03  # 60x en modo simulado

    def toggle_mode(self):
        self.real_time_mode = not self.real_time_mode
        self.last_real_timestamp = time.time()

    def toggle_pause(self):
        if self.time_speed > 0:
            self.time_speed = 0
        else:
            self.time_speed = 0.03

    def update(self, delta_time):
        if self.real_time_mode:
            now = time.time()
            elapsed = now - self.last_real_timestamp
            self.last_real_timestamp = now
            day_fraction = elapsed / self.day_length_seconds
            self.current_time += day_fraction
        else:
            self.current_time += ((delta_time + pi) % (2 * pi)) - pi

        # while self.current_time >= 1.0:
        #     self.current_time -= 1.0
        #     self.current_day = (self.current_day + 1) % int(self.year_length_days)

    def get_hour_angle(self):
        # return_value = (self.current_time - 0.5) * 3600
        return_value = (self.current_time - 0.5) * 2 * pi  # desde -π a π
        print(return_value)
        return return_value

    def get_current_day(self):
        return self.current_day