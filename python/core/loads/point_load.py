import numpy as np
from .external_load import ExternalLoad


class PointLoad(ExternalLoad):
    """Implementaizone di ExternaLoad per carichi concentrati"""

    P: np.ndarray
    """ carico concentrato applicato in un punto della trave [fx, fy] in N nel sistema globale """

    x: int
    """ posizione del carico concentrato lungo la trave in mm a partire dal nodo i """

    def __init__(self, P: np.ndarray, x: int):
        """
        parametri:
            P: carico concentrato applicato in un punto della trave [fx, fy] in N nel sistema globale
            x: posizione del carico concentrato lungo la trave in mm a partire dal nodo i
        """
        if P.shape != (2,):
            raise ValueError(
                "P deve essere un array di forma (2,). e deve contenre 2 valori [fx, fy]"
            )
        if x < 0:
            raise ValueError(
                "x deve essere un valore positivo. x deve essere maggiore di 0"
            )

        self.P = P
        self.x = x

    def __str__(self):
        return f"x={self.P[0]} kN : y={self.P[1]} kN, x={self.x} mm"

    def solve(
        self,
        length: int,
        angle: float,
        releases: tuple[bool, bool],
    ) -> np.ndarray:

        l = length
        a = self.x
        b = l - a
        # estrai i carichi locali
        fn, ft = self.to_local(angle)

        # AZIONI LONGITUDINALI lungo l'asse della trave
        ##################################
        Ni = fn / 2
        Nj = fn / 2
        axial = np.array([Ni, 0, 0, Nj, 0, 0], dtype=float)
        # AZIONI TRASVERSALI normali all'asse della trave
        ##################################

        match releases:
            case (False, False):
                # incastro-incastro
                Ti = +((ft * b**2) / (l**3)) * (l + 2 * a)
                Mi = +(ft * a * b**2) / l**2
                Tj = +((ft * a**2) / (l**3)) * (l + 2 * b)
                Mj = -(ft * a**2 * b) / l**2

            case (True, False):
                # cerniera-incastro
                Ti = +((ft * b**2) / (2 * l**3)) * (2 * l + a)
                Mi = 0
                Tj = +((ft * a) / (2 * l)) * (3 - (a**2 / l**2))
                Mj = -((ft * b * a) / (2 * l**2)) * (l + a)

            case (False, True):
                # incastro-cerniera
                Ti = +((ft * b) / (2 * l)) * (3 - (b**2 / l**2))
                Mi = +((ft * a * b) / (2 * l**2)) * (l + b)
                Tj = +((ft * a**2) / (2 * l**3)) * (2 * l + b)
                Mj = 0

            case (True, True):
                # cerniera-cerniera
                Ti = +ft * b / l
                Mi = 0
                Tj = +ft * a / l
                Mj = 0

        transverse = np.array([0, Ti, Mi, 0, Tj, Mj], dtype=float)

        local_equivalent_loads = axial + transverse
        # ruota i carichi locali nel sistema globale della trave
        # [Ni, Ti, Mi, Nj, Tj, Mj] => [Xi, Yi, Mi, Xj, Vj, Mj]
        # l'angolo è negativo perchè ripercorre la rotazione all'inverso
        return self.to_global(local_equivalent_loads, -angle)
