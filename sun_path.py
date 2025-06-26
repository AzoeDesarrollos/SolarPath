from pygame import init as pg_init, quit as pg_quit, display, time, font, draw, event
from pygame import KEYDOWN, QUIT, K_SPACE, K_a, K_r, K_UP, K_DOWN, K_ESCAPE
from sun.planet_time import PlanetTime
from math import radians, degrees, pi
from sun.funciones import *
from sys import exit

# -------- Parámetros del planeta y observador --------

latitude_deg = -34.6
obliquity_deg = 23.44
eccentricity = 0.0167
orbital_period = 365.25

# -------- Visualización --------

width, height = 900, 700
center_x, center_y = width // 2, height // 2 + 100
radius = 300

# -------- Inicialización pygame --------

pg_init()
screen = display.set_mode((width, height))
display.set_caption("Movimiento Solar Anual")
clock = time.Clock()
fuente = font.SysFont(None, 24)

phi = radians(latitude_deg)
planet_time = PlanetTime(day_length_seconds=86400, year_length_days=365.25)
epsilon = radians(obliquity_deg)


# -------- Funciones astronómicas --------
def interpolate_color(c1, c2, t):
    return (
        int(c1[0] * (1 - t) + c2[0] * t),
        int(c1[1] * (1 - t) + c2[1] * t),
        int(c1[2] * (1 - t) + c2[2] * t)
    )


def draw_dynamic_sky(surface, altura):
    # Altitud en radianes, convertimos a grados
    alt_deg = degrees(altura)

    if alt_deg <= -6:
        # Noche cerrada
        top = (5, 5, 20)
        bottom = (10, 10, 30)
    elif -6 < alt_deg <= 5:
        # Amanecer o anochecer
        mix = (alt_deg + 6) / 11  # de 0 a 1
        top = interpolate_color((5, 5, 20), (200, 100, 50), mix)
        bottom = interpolate_color((10, 10, 30), (255, 120, 60), mix)
    elif 5 < alt_deg <= 30:
        # Sol bajo en cielo
        mix = (alt_deg - 5) / 25
        top = interpolate_color((200, 100, 50), (100, 160, 255), mix)
        bottom = interpolate_color((255, 120, 60), (180, 220, 255), mix)
    else:
        # Sol alto
        top = (100, 160, 255)
        bottom = (180, 220, 255)

    for dy in range(height):
        ratio = dy / height
        r = int(top[0] * (1 - ratio) + bottom[0] * ratio)
        g = int(top[1] * (1 - ratio) + bottom[1] * ratio)
        b = int(top[2] * (1 - ratio) + bottom[2] * ratio)
        draw.line(surface, (r, g, b), (0, dy), (width, dy))


# -------- Simulación --------

current_day = 0
solar_time_total = -pi  # tiempo solar continuo
current_time = -pi  # ángulo horario actual

# time_speed = 0.03
# day_speed = 1

show_arc = False
path = []

# -------- Loop principal --------

while True:
    for e in event.get():
        if (e.type == KEYDOWN and e.key == K_ESCAPE) or e.type == QUIT:
            pg_quit()
            exit()
        elif e.type == KEYDOWN:
            if e.key == K_a:
                show_arc = not show_arc
            elif e.key == K_SPACE:
                planet_time.toggle_pause()
            elif e.key == K_UP:
                latitude_deg = min(90, latitude_deg + 1)
                # phi = get_phi(latitude_deg)
            elif e.key == K_DOWN:
                latitude_deg = max(-90, latitude_deg - 1)
                # phi = get_phi(latitude_deg)
            elif e.key == K_r:
                planet_time.toggle_mode()
    # Línea del horizonte
    horizon_y = center_y

    # Indicadores cardinales
    font_large = font.SysFont(None, 28)
    east_text = font_large.render("Este", True, (0, 0, 0))
    west_text = font_large.render("Oeste", True, (0, 0, 0))

    day_frac = current_day / orbital_period
    m = mean_anomaly(day_frac)
    v = true_anomaly(m, eccentricity)
    ls = solar_longitude(v)
    decl = declination(ls, epsilon)
    eot = equation_of_time(m, ls, eccentricity, epsilon)

    hour_angle = current_time - eot
    result = get_solar_xy(latitude_deg, hour_angle, decl)
    altitude = solar_altitude(latitude_deg, hour_angle, decl)
    draw_dynamic_sky(screen, altitude)
    if result:
        x, y = result
        px = center_x + int(x * radius)
        py = center_y - int(y * radius)
        draw.circle(screen, (255, 255, 0), (px, py), 30)
        if show_arc:
            path.append((px, py))
    else:
        if show_arc:
            path.clear()

    if show_arc and len(path) > 1:
        draw.lines(screen, (255, 200, 0), False, path, 2)

    # Muestra el horizonte
    draw.rect(screen, (0, 200, 100), (0, horizon_y, width, horizon_y))
    screen.blit(east_text, (width - 70, horizon_y + 10))
    screen.blit(west_text, (10, horizon_y + 10))
    # draw_mode7_grid(screen, latitude_deg, pygame.time.get_ticks() // 10 % (height // 20))

    # Mostrar texto
    day_text = fuente.render(f"Día del año: {int(current_day)} / {int(orbital_period)}", True, (255, 255, 255))
    time_hours = (current_time + pi) / (2 * pi) * 24
    time_text = fuente.render(f"Hora solar: {time_hours:.2f} h", True, (255, 255, 255))
    info_text = fuente.render("Presiona 'A' para alternar arco solar", True, (0, 0, 0))
    pause_text = fuente.render("Presiona 'Espacio' para pausar/reanudar", True, (0, 0, 0))
    lat_text = fuente.render(f"Latitud: {latitude_deg:.1f}°", True, (255, 255, 255))
    mode_text = fuente.render(f"Modo: {'Tiempo real' if planet_time.real_time_mode else 'Simulado'}", True,
                              (255, 255, 255))
    screen.blit(mode_text, (10, 130))
    screen.blit(lat_text, (10, 70))
    screen.blit(day_text, (10, 10))
    screen.blit(time_text, (10, 40))
    screen.blit(info_text, (10, height - 60))
    screen.blit(pause_text, (10, height - 30))

    display.update()

    # ------ ACTUALIZAR TIEMPO CORRECTAMENTE ------
    solar_time_total += planet_time.time_speed
    current_time = ((solar_time_total + pi) % (2 * pi)) - pi

    if solar_time_total >= pi:
        solar_time_total -= 2 * pi
        current_day += 1
        if current_day > orbital_period:
            current_day = 0
        path.clear()

    delta_time = clock.tick(60) / 1000
    planet_time.update(delta_time)

    # hour_angle = planet_time.get_hour_angle()
    # current_day = planet_time.get_current_day()
