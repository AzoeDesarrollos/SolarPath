from math import sqrt, sin, cos, tan, asin, acos, atan2, radians, degrees, pi
from pygame import draw


# def get_phi(latitude_deg):
#     return radians(latitude_deg)


def mean_anomaly(day_frac):
    return 2 * pi * day_frac


def true_anomaly(m, e):
    e_anom = m + e * sin(m) * (1 + e * cos(m))
    v = 2 * atan2(sqrt(1 + e) * sin(e_anom / 2),
                  sqrt(1 - e) * cos(e_anom / 2))
    return v


# def solar_longitude(v):
#     return v


def equation_of_time(m, ls, e, obliquity_rad):
    e_term = -2 * e * sin(m)
    obl_term = tan(obliquity_rad / 2) ** 2 * sin(2 * ls)
    return e_term + obl_term


# def equation_of_time_hours(day_of_year):
#     # Parámetros aproximados
#     b = radians((360 / 365) * (day_of_year - 81))
#     eot_minutes = 9.87 * sin(2 * b) - 7.53 * cos(b) - 1.5 * sin(b)
#     return eot_minutes / 60  # convertir minutos a horas


def declination(ls, obliquity_rad):
    return asin(sin(obliquity_rad) * sin(ls))


def solar_altitude(latitude, hour_angle, decl):
    latitude = normalize_latitude(latitude)
    phi = radians(latitude)
    return_value = asin(sin(phi) * sin(decl) + cos(phi) * cos(decl) * cos(hour_angle))
    return return_value


def _solar_azimuth(latitude, hour_angle, decl, altitude):
    phi = radians(latitude)
    cos_az = (sin(decl) - sin(phi) * sin(altitude)) / (cos(phi) * cos(altitude))
    cos_az = max(-1, min(1, cos_az))
    az = acos(cos_az)
    if hour_angle > 0:
        az = 2 * pi - az
    return az


def _small_angle_approximation(radius_km, distance_km):
    diameter = 2 * radius_km  # km
    # ángulo aparente en segundos de arco
    angle_arcsec = (diameter * 206265) / distance_km
    # convertir a radianes
    angle_rad = angle_arcsec / 206265
    return angle_rad


def get_solar_xy(latitude, hour_angle, decl, radius=696340, distance=149597870):
    alt = solar_altitude(latitude, hour_angle, decl)
    solar_radius_rad = _small_angle_approximation(radius, distance) / 2  # radio angular (mitad del diámetro angular)

    if alt < -solar_radius_rad:
        return None
    az = _solar_azimuth(latitude, hour_angle, decl, alt)
    x = cos(alt) * sin(az)
    y = sin(alt)
    return x, y


# def calc_fuga_x(center_x, fuga_width, i, total_lines):
#     step = fuga_width / (total_lines / 2)
#     return center_x + i * step


def draw_mode7_grid(surface, screen_width, screen_height, center_x, horizon_y, latitude_deg,
                    line_color, num_longitudinal=20, num_latitudinal=180,
                    apertura_ancho=400, divergence_factor=1.5):
    # --- Líneas longitudinales (sin cambios) ---
    x_start_linea_fuga = center_x - apertura_ancho / 2
    separacion_lineas = apertura_ancho / num_longitudinal

    for i in range(num_longitudinal + 1):
        x_start = x_start_linea_fuga + i * separacion_lineas
        y_start = horizon_y

        x_offset = (x_start - center_x) * divergence_factor
        x_end = center_x + x_offset
        y_end = screen_height
        draw.line(surface, line_color, (x_start, y_start), (x_end, y_end), 1)

    # --- Líneas latitudinales ---
    # Definir espaciado fijo entre líneas
    spacing = 20  # espaciado constante, NO creciente

    # Convertir latitud a factor de desplazamiento
    lat_factor = (latitude_deg + 90) / 180  # de 0 (sur) a 1 (norte)
    max_shift = 400
    shift = (lat_factor - 0.5) * 2 * max_shift  # -400 a +400

    # Centrar la grilla en la línea del horizonte + shift
    base_y = horizon_y + shift

    # Generar muchas líneas alrededor de base_y, hacia arriba y abajo
    for i in range(-num_latitudinal // 2, num_latitudinal // 2 + 1):
        y = base_y + i * spacing
        if horizon_y <= y <= screen_height:
            draw.line(surface, line_color, (0, y), (screen_width, y), 2)


def interpolate_color(c1, c2, t):
    return (
        int(c1[0] * (1 - t) + c2[0] * t),
        int(c1[1] * (1 - t) + c2[1] * t),
        int(c1[2] * (1 - t) + c2[2] * t)
    )


def draw_dynamic_sky(surface, altura, width, height, dy):
    alt_deg = degrees(altura)
    if alt_deg <= -6:
        top, bottom = (5, 5, 20), (10, 10, 30)
    elif -6 < alt_deg <= 5:
        mix = (alt_deg + 6) / 11
        top = interpolate_color((5, 5, 20), (200, 100, 50), mix)
        bottom = interpolate_color((10, 10, 30), (255, 120, 60), mix)
    elif 5 < alt_deg <= 30:
        mix = (alt_deg - 5) / 25
        top = interpolate_color((200, 100, 50), (100, 160, 255), mix)
        bottom = interpolate_color((255, 120, 60), (180, 220, 255), mix)
    else:
        top, bottom = (100, 160, 255), (180, 220, 255)
    for cy in range(height):
        ratio = dy / height
        r = int(top[0] * (1 - ratio) + bottom[0] * ratio)
        g = int(top[1] * (1 - ratio) + bottom[1] * ratio)
        b = int(top[2] * (1 - ratio) + bottom[2] * ratio)
        draw.line(surface, (r, g, b), (0, cy), (width, cy))


def normalize_latitude(lat):
    lat = lat % 360
    if lat > 180:
        lat -= 360
    if lat > 90:
        lat = 180 - lat
    elif lat < -90:
        lat = -180 - lat
    return lat


__all__ = [
    "get_solar_xy",
    "mean_anomaly",
    "true_anomaly",
    "solar_altitude",
    "declination",
    "equation_of_time",
    "draw_mode7_grid",
    "normalize_latitude",
    "draw_dynamic_sky"
]
