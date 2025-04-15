def momentum_fixed_fixed(x: int, M: float):
    l = 1000
    a = x
    b = l - a

    Ti = -6 * M * a * b / l**3
    Mi = -M * b / l * (2 - 3 * b / l)
    Tj = +6 * M * a * b / l**3
    Mj = -M * a / l * (2 - 3 * a / l)


def momentum_fixed_hinged(x: int, M: float):
    l = 1000
    a = x
    b = l - a

    Ti = 3 * M * (1 - (b**2 / l**2)) / (2 * l)
    Mi = M * (1 - 3 * (b**2 / l**2)) / 2
    Tj = -Ti
    Mj = 0
