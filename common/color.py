def mix_color(color1, color2, weight):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int(r1 * weight + r2 * (1 - weight))
    g = int(g1 * weight + g2 * (1 - weight))
    b = int(b1 * weight + b2 * (1 - weight))
    return r, g, b


BLACK = (0, 0, 0)
WOOD = (222, 184, 135)
BURGUNDY = (120, 0, 30)
WHITE = (255, 251, 240)


MILD_BLACK = mix_color(WOOD, BLACK, 0.8)
MILD_WHITE = mix_color(WOOD, WHITE, 0.8)
MILD_BURGUNDY = mix_color(WOOD, BURGUNDY, 0.8)
