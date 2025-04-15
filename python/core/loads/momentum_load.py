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
        if x < 0:
            raise ValueError(
                "x deve essere un valore positivo. x deve essere maggiore di 0"
            )

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
                Ti = 0
                Mi = 0
                Tj = 0
                Mj = 0
            case (False, True):
                Ti = 3 * M * (1 - (b**2 / l**2)) / (2 * l)
                Mi = M * (1 - 3 * (b**2 / l**2)) / 2
                Tj = -Ti
                Mj = 0
            case (True, True):
                Ti = 0
                Mi = 0
                Tj = 0
                Mj = 0

        local_eq_loads = np.array([Ni, Ti, Mi, Nj, Tj, Mj], dtype=float)
        return self.to_global(local_eq_loads, -angle)
