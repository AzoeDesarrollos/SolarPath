from pygame import init as pg_init, quit as pg_quit, display, time, font, draw, event
from pygame import KEYDOWN, QUIT, K_SPACE, K_a, K_r, K_UP, K_DOWN, K_ESCAPE
from sun.planet_time import PlanetTime
from math import radians, degrees, pi
from sun.funciones import *
from sys import exit

# -------- Parámetros del planeta y observador --------
latitude_deg = -34
obliquity_deg = 23.44
eccentricity = 0.0167
orbital_period = 365.25
sky_radius_px = 400

# -------- Visualización --------
width, height = 900, 700
center_x, center_y = width // 2, height // 2 + 100
radius = 400

# -------- Inicialización pygame --------
pg_init()
screen = display.set_mode((width, height))
display.set_caption("Movimiento Solar Anual")
clock = time.Clock()
fuente = font.SysFont(None, 24)

planet_time = PlanetTime()
epsilon = radians(obliquity_deg)
show_arc = False
path = []
prev_day = -1


def interpolate_color(c1, c2, t):
    return (
        int(c1[0] * (1 - t) + c2[0] * t),
        int(c1[1] * (1 - t) + c2[1] * t),
        int(c1[2] * (1 - t) + c2[2] * t)
    )


def draw_dynamic_sky(surface, altura):
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
    for dy in range(height):
        ratio = dy / height
        r = int(top[0] * (1 - ratio) + bottom[0] * ratio)
        g = int(top[1] * (1 - ratio) + bottom[1] * ratio)
        b = int(top[2] * (1 - ratio) + bottom[2] * ratio)
        draw.line(surface, (r, g, b), (0, dy), (width, dy))


# -------- Bucle principal --------
while True:
    for e in event.get():
        if (e.type == KEYDOWN and e.key == K_ESCAPE) or e.type == QUIT:
            pg_quit()
            exit()
        elif e.type == KEYDOWN:
            if e.key == K_a:
                show_arc = not show_arc
            elif e.key == K_SPACE:
                planet_time.time_speed = 0 if planet_time.time_speed > 0 else 3
            elif e.key == K_r:
                planet_time.toggle_mode()
            elif e.key == K_UP:
                latitude_deg = min(90, latitude_deg + 1)
            elif e.key == K_DOWN:
                latitude_deg = max(-90, latitude_deg - 1)

    horizon_y = center_y
    font_large = font.SysFont(None, 28)
    east_text = font_large.render("Este", True, (0, 0, 0))
    west_text = font_large.render("Oeste", True, (0, 0, 0))

    current_day = planet_time.get_current_day()
    day_frac = current_day / orbital_period
    m = mean_anomaly(day_frac)
    v = true_anomaly(m, eccentricity)
    ls = solar_longitude(v)
    decl = declination(ls, epsilon)
    eot = equation_of_time(m, ls, eccentricity, epsilon)

    if planet_time.real_time_mode:
        hour_angle = planet_time.get_hour_angle()  # Ya incluye la hora local
    else:
        hour_angle = planet_time.get_hour_angle() - eot  # Solo se corrige en modo simulado
    result = get_solar_xy(latitude_deg, hour_angle, decl)
    altitude = solar_altitude(latitude_deg, hour_angle, decl)

    draw_dynamic_sky(screen, altitude)

    if show_arc and len(path) > 1:
        draw.lines(screen, (255, 200, 0), False, path, 2)

    if result:
        x, y = result
        px = center_x + int(x * sky_radius_px)
        py = center_y - int(y * sky_radius_px)
        draw.circle(screen, (255, 255, 0), (px, py), 8)
        if show_arc:
            path.append((px, py))
    else:
        if show_arc:
            path.clear()
    draw.rect(screen, (0, 200, 100), (0, horizon_y, width, horizon_y))
    num_lines = max(1, time.get_ticks() // 10 % (height // 20))
    draw_mode7_grid(screen, width, height, center_x, horizon_y, latitude_deg,
                    line_color=[100, 150, 200], num_longitudinal=30, num_latitudinal=30,
                    apertura_ancho=800, divergence_factor=10)

    # draw_latitude_perspective_lines(screen, horizon_y, width, height, center_x,
    #                                 line_color=(100, 150, 200), num_lines=10)
    screen.blit(east_text, (width - 70, horizon_y + 10))
    screen.blit(west_text, (10, horizon_y + 10))

    # Hora solar estimada
    solar_hour = (hour_angle / (2 * pi)) * 24 + 12
    solar_hour = solar_hour % 24
    hours = int(solar_hour)
    minutes = int((solar_hour - hours) * 60)

    day_text = fuente.render(f"Día del año: {current_day} / {int(orbital_period)}", True, (255, 255, 255))
    time_text = fuente.render(f"Hora solar: {hours:02d}:{minutes:02d}", True, (255, 255, 255))
    lat_text = fuente.render(f"Latitud: {latitude_deg:.1f}°", True, (255, 255, 255))
    mode_text = fuente.render(f"Modo: {'Real' if planet_time.real_time_mode else 'Simulado'}", True, (255, 255, 255))
    screen.blit(day_text, (10, 10))
    screen.blit(time_text, (10, 40))
    screen.blit(lat_text, (10, 70))
    screen.blit(mode_text, (10, 100))

    display.update()

    delta_time = clock.tick(60) / 1000
    planet_time.update(delta_time)
