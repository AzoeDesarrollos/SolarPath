from math import sqrt, sin, cos, tan, asin, acos, atan2, radians, pi
from pygame import draw


def get_phi(latitude_deg):
    return radians(latitude_deg)


def mean_anomaly(day_frac):
    return 2 * pi * day_frac


def true_anomaly(m, e):
    e_anom = m + e * sin(m) * (1 + e * cos(m))
    v = 2 * atan2(sqrt(1 + e) * sin(e_anom / 2),
                  sqrt(1 - e) * cos(e_anom / 2))
    return v


def solar_longitude(v):
    return v


def equation_of_time(m, ls, e, obliquity_rad):
    e_term = -2 * e * sin(m)
    obl_term = tan(obliquity_rad / 2) ** 2 * sin(2 * ls)
    return e_term + obl_term


def equation_of_time_hours(day_of_year):
    # Parámetros aproximados
    b = radians((360 / 365) * (day_of_year - 81))
    eot_minutes = 9.87 * sin(2 * b) - 7.53 * cos(b) - 1.5 * sin(b)
    return eot_minutes / 60  # convertir minutos a horas


def declination(ls, obliquity_rad):
    return asin(sin(obliquity_rad) * sin(ls))


def solar_altitude(latitude, hour_angle, decl):
    phi = radians(latitude)
    return_value = asin(sin(phi) * sin(decl) + cos(phi) * cos(decl) * cos(hour_angle))
    return return_value


def solar_azimuth(latitude, hour_angle, decl, altitude):
    phi = radians(latitude)
    cos_az = (sin(decl) - sin(phi) * sin(altitude)) / (cos(phi) * cos(altitude))
    cos_az = max(-1, min(1, cos_az))
    az = acos(cos_az)
    if hour_angle > 0:
        az = 2 * pi - az
    return az


def small_angle_approximation(radius_km, distance_km):
    diameter = 2 * radius_km  # km
    # ángulo aparente en segundos de arco
    angle_arcsec = (diameter * 206265) / distance_km
    # convertir a radianes
    angle_rad = angle_arcsec / 206265
    return angle_rad


def get_solar_xy(latitude, hour_angle, decl, radius=696340, distance=149597870):
    alt = solar_altitude(latitude, hour_angle, decl)
    solar_radius_rad = small_angle_approximation(radius, distance) / 2  # radio angular (mitad del diámetro angular)

    if alt < -solar_radius_rad:
        return None
    az = solar_azimuth(latitude, hour_angle, decl, alt)
    x = cos(alt) * sin(az)
    y = sin(alt)
    return x, y


def calc_fuga_x(center_x, fuga_width, i, total_lines):
    step = fuga_width / (total_lines / 2)
    return center_x + i * step


def draw_mode7_grid(surface, screen_width, screen_height, center_x, horizon_y,
                    line_color=(100, 150, 200), num_longitudinal=20, num_latitudinal=20,
                    apertura_ancho=400, divergence_factor=1.5):
    """
    Dibuja una cuadrícula con:
    - Líneas longitudinales que convergen hacia una 'línea de fuga' horizontal sobre el horizonte
      (líneas paralelas en el horizonte).
    - Líneas latitudinales horizontales con espaciamiento creciente para efecto perspectiva.
    """

    # Coordenadas de inicio para líneas longitudinales: distribuidas sobre la línea de fuga
    x_start_linea_fuga = center_x - apertura_ancho / 2
    separacion_lineas = apertura_ancho / num_longitudinal

    for i in range(num_longitudinal + 1):
        # Punto inicial sobre la línea de fuga (horizonte)
        x_start = x_start_linea_fuga + i * separacion_lineas
        y_start = horizon_y

        # Punto final en la base (parte inferior) de la pantalla
        # Aquí las líneas se abren divergentes multiplicando la distancia horizontal por divergence_factor
        x_offset = (x_start - center_x) * divergence_factor
        x_end = center_x + x_offset
        y_end = screen_height

        draw.line(surface, line_color, (x_start, y_start), (x_end, y_end), 1)

    # Líneas latitudinales horizontales (curvas de nivel) con espaciamiento creciente hacia abajo
    y = horizon_y + 10
    spacing = 10
    for _ in range(num_latitudinal):
        draw.line(surface, line_color, (0, y), (screen_width, y), 1)
        spacing *= 1.15  # aumenta separación para efecto perspectiva
        y += spacing
        if y > screen_height:
            break


# def draw_latitude_perspective_lines(surface, horizon_y, width, height, center_x,
#                                     line_color=(100, 150, 200), num_lines=10):
#     # Espacio vertical entre líneas horizontales
#     line_spacing = (height - horizon_y) / num_lines
#
#     fuga_width = width // 2  # Distancia desde el centro hacia cada lado para líneas diagonales
#
#     for i in range(1, num_lines + 1):
#         y = horizon_y + i * line_spacing
#
#         # Línea horizontal extendida a todo el ancho (desde 0 hasta width)
#         draw.line(surface, line_color, (0, y), (width, y), 1)
#
#         # Líneas diagonales que van desde los bordes hasta el punto de fuga (center_x, horizon_y)
#         # Desde borde izquierdo hacia punto de fuga
#         draw.line(surface, line_color, (0, y), (center_x, horizon_y), 1)
#         # Desde borde derecho hacia punto de fuga
#         draw.line(surface, line_color, (width, y), (center_x, horizon_y), 1)


# def draw_mode7_grid(surface, latitude, num_lines, width, height, center_x):
#     """
#     Dibuja las líneas horizontales que fugan hacia el horizonte.
#     Parámetros:
#     - surface: superficie de pygame donde dibujar
#     - latitude: latitud (no usada aquí, pero la podés usar para efectos futuros)
#     - num_lines: cantidad de líneas horizontales
#     - width, height: dimensiones de la pantalla
#     - center_x: coordenada x del centro (punto de fuga horizontal)
#     """
#     color = (100, 150, 200)
#     line_spacing = (height // 2) // num_lines  # espacio vertical entre líneas
#     horizon_y = height // 2 + 100  # altura del horizonte, ajustalo si querés
#
#     for i in range(num_lines + 1):
#         y = horizon_y + i * line_spacing
#         # Línea horizontal extendida de izquierda a derecha
#         draw.line(surface, color, (0, y), (width, y), 1)


__all__ = [
    "get_phi",
    "get_solar_xy",
    "mean_anomaly",
    "true_anomaly",
    "solar_longitude",
    "solar_azimuth",
    "solar_altitude",
    "declination",
    "equation_of_time",
    "small_angle_approximation",
    "equation_of_time_hours",
    "draw_mode7_grid",
    # "draw_latitude_perspective_lines"
]
