class Observer:
    latitude = -34
    longitude_deg = 0
    sky_radius_px = 400

    is_observer = True
    delta_time = 0

    parent = None

    @classmethod
    def init(cls):
        cls.x = 0
        cls.y = 0

    @classmethod
    def move(cls, dx, dy):
        cls.x = dx
        cls.y = dy
        latitude_deg = cls.latitude

        latitude_deg += dy * 10 * cls.delta_time  # 20 grados por segundo ajustable

        # Asegurar latitud en rango -180 a +180 con rollover
        if latitude_deg > 180:
            latitude_deg -= 360
        elif latitude_deg < -180:
            latitude_deg += 360