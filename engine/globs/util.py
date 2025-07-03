from pygame import draw, font


def get_intersections(diagonals, horizontals):
    intersections = []
    for y in horizontals:
        row = []
        for m, b in diagonals:
            x = int((y - b) / m) if m != 0 else 400
            row.append((x, y))
        intersections.append(row)
    return intersections


def generate_parallelograms(horizontals, diagonals, intersections):
    parallelograms = []
    for j in range(len(horizontals) - 1):
        for i in range(len(diagonals) - 1):
            p1 = intersections[j][i]  # Superior izquierdo
            p2 = intersections[j][i + 1]  # Superior derecho
            p3 = intersections[j + 1][i + 1]  # Inferior derecho
            p4 = intersections[j + 1][i]  # Inferior izquierdo
            parallelograms.append([p1, p2, p3, p4])
    return parallelograms


def draw_checkerboard_parallelograms(paralelogramos, image):
    fuente = font.SysFont('Verdana', 8)
    paralelogramos_ordenados = sorted(paralelogramos, key=lambda pg: (min(p[1] for p in pg), min(p[0] for p in pg)))

    # Dibujar con patrón de ajedrez
    for idx, (p1, p2, p3, p4) in enumerate(paralelogramos_ordenados):
        centroide = [int((p1[0] + p2[0] + p3[0] + p4[0]) / 4), int((p1[1] + p2[1] + p3[1] + p4[1]) / 4)]
        if idx % 2:
            color = 'black'
        else:
            color = 'white'
        number = fuente.render(str(idx), True, 'black' if color == 'white' else 'white')
        draw.polygon(image, color, ([p1, p2, p3, p4]))
        number_rect = number.get_rect(center=centroide)
        image.blit(number, number_rect)


def draw_paralelograms(diagonals, horizontals, image):
    interseccions = get_intersections(diagonals, horizontals)
    parallelograms = generate_parallelograms(horizontals, diagonals, interseccions)
    draw_checkerboard_parallelograms(parallelograms, image)
