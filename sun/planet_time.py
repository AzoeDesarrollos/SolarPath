from datetime import datetime
from math import pi


class PlanetTime:
    def __init__(self, year_length_days=365.25, time_speed=3.0, real_time_mode=False):
        self.year_length_days = year_length_days
        self.time_speed = time_speed
        self.real_time_mode = real_time_mode

        self.current_time = 0.0
        self.previous_time = 0.0
        self.current_day = 0

    def update(self, delta_time):
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
                self.current_day = (self.current_day + 1) % int(self.year_length_days)

    def get_hour_angle(self):
        return self.current_time

    def get_current_day(self):
        return self.current_day

    def toggle_mode(self):
        self.real_time_mode = not self.real_time_mode
