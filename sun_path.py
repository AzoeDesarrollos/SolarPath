from pygame import init as pg_init, quit as pg_quit, display, time, font, draw, event
from pygame import KEYDOWN, KEYUP, QUIT, K_SPACE, K_a, K_r, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_ESCAPE
from sun.planet_time import PlanetTime
from math import radians, pi
from sun.funciones import *
from sys import exit

# -------- Parámetros del planeta y observador --------
latitude_deg = -34
longitude_deg = 0
obliquity_deg = 23.44
eccentricity = 0.0167
orbital_period = 365.25
sky_radius_px = 400

# -------- Visualización --------
width, height = 800, 600
center_x, center_y = width // 2, height // 2 + 100
# radius = 400

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

# -------- Bucle principal --------
delta_time = 0
dx, dy = 0, 0  # velocidad horizontal y vertical, respectivamente
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
                dy += 1
            elif e.key == K_DOWN:
                dy -= 1
            elif e.key == K_RIGHT:
                dx += 1
            elif e.key == K_LEFT:
                dx -= 1

        elif e.type == KEYUP:
            if e.key in (K_UP, K_DOWN):
                dy = 0
            elif e.key in (K_LEFT, K_RIGHT):
                dx = 0
    # if dy != 0 and (ghost_mode or planet_time.time_speed > 0):
    #     latitude_deg += dy * lat_speed
    latitude_deg += dy * 10 * delta_time  # 20 grados por segundo ajustable

    # Asegurar latitud en rango -180 a +180 con rollover
    if latitude_deg > 180:
        latitude_deg -= 360
    elif latitude_deg < -180:
        latitude_deg += 360

    # longitude_deg += dx * 10 * delta_time  # 20 grados por segundo ajustable

    # # Asegurar latitud en rango -180 a +180 con rollover
    # if latitude_deg > 180:
    #     latitude_deg -= 360
    # elif latitude_deg < -180:
    #     latitude_deg += 360

    horizon_y = center_y
    font_large = font.SysFont(None, 28)
    east_text = font_large.render("Este", True, (0, 0, 0))
    west_text = font_large.render("Oeste", True, (0, 0, 0))

    current_day = planet_time.get_current_day()
    day_frac = current_day / orbital_period
    m = mean_anomaly(day_frac)
    ls = true_anomaly(m, eccentricity)
    decl = declination(ls, epsilon)
    eot = equation_of_time(m, ls, eccentricity, epsilon)

    hour_angle = planet_time.get_hour_angle()  # Ya incluye la hora local
    if not planet_time.real_time_mode:
        hour_angle = planet_time.get_hour_angle() - eot  # Solo se corrige en modo simulado
    result = get_solar_xy(latitude_deg, hour_angle, decl)
    altitude = solar_altitude(latitude_deg, hour_angle, decl)

    draw_dynamic_sky(screen, altitude, width, height, dy)

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
                    line_color=[100, 150, 200], num_longitudinal=30,
                    apertura_ancho=800, divergence_factor=10)

    screen.blit(east_text, (width - 70, horizon_y + 10))
    screen.blit(west_text, (10, horizon_y + 10))

    # Hora solar estimada
    solar_hour = (hour_angle / (2 * pi)) * 24 + 12
    solar_hour = solar_hour % 24
    hours = int(solar_hour)
    minutes = int((solar_hour - hours) * 60)
    abs_lat = abs(latitude_deg % 360)
    lat_display = normalize_latitude(latitude_deg)
    day_text = fuente.render(f"Día del año: {current_day} / {int(orbital_period)}", True, (255, 255, 255))
    time_text = fuente.render(f"Hora solar: {hours:02d}:{minutes:02d}", True, (255, 255, 255))
    lat_text = fuente.render(f"Latitud: {lat_display:.1f}°", True, (255, 255, 255))
    mode_text = fuente.render(f"Modo: {'Real' if planet_time.real_time_mode else 'Simulado'}", True, (255, 255, 255))
    screen.blit(day_text, (10, 10))
    screen.blit(time_text, (10, 40))
    screen.blit(lat_text, (10, 70))
    screen.blit(mode_text, (10, 100))

    display.update()

    delta_time = clock.tick(60) / 1000
    planet_time.update(delta_time)
