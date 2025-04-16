from .external_load import ExternalLoad
import numpy as np


class MomentumLoad(ExternalLoad):
    """Implementazione di ExternalLoad per carichi concentrati"""

    x: int
    """posizione del carico concentrato lungo la trave in mm a partire dal nodo i"""

    M: float
    """momento applicato in un punto della trave in Nmm"""

    def __init__(self, x: int, M: float):
        """
        parametri:
            x: posizione del carico concentrato lungo la trave in mm a partire dal nodo i
            M: momento applicato in un punto della trave in Nmm
        """
        self.x = x
        self.M = M

    def __str__(self):
        return f"x={self.x} mm : M={self.M} Nmm"

    def solve(
        self,
        length: int,
        angle: float,
        releases: tuple[bool, bool],
    ) -> np.ndarray:

        l = length
        a = self.x
        b = l - a
        M = self.M
        Ni, Nj = 0, 0

        match releases:
            case (False, False):
                Ti = -6 * M * a * b / l**3
                Mi = -M * b / l * (2 - 3 * b / l)
                Tj = +6 * M * a * b / l**3
                Mj = -M * a / l * (2 - 3 * a / l)
            case (True, False):
                Ti = -3 * M / (2 * l) * (1 - (a**2 / l**2))
                Mi = 0
                Tj = +3 * M / (2 * l) * (1 - (a**2 / l**2))
                Mj = -M / 2 * (1 - 3 * (a**2 / l**2))
            case (False, True):
                Ti = -3 * M / (2 * l) * (1 - (b**2 / l**2))
                Mi = -M / 2 * (1 - 3 * (b**2 / l**2))
                Tj = +3 * M / (2 * l) * (1 - (b**2 / l**2))
                Mj = 0
            case (True, True):
                Ti = -M / l
                Mi = 0
                Tj = M / l
                Mj = 0

        local_eq_loads = np.array([Ni, Ti, Mi, Nj, Tj, Mj], dtype=float)
        return self.to_global(local_eq_loads, -angle)
