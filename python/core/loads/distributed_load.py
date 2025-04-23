import numpy as np
from .external_load import ExternalLoad


class DistributedLoad(ExternalLoad):
    """implementazione di ExternalLoad per un carico distribuito Costate"""

    P: np.ndarray
    """carico distribuito costante lungo la trave [qx, qy] in N/mm nelle coordinate globali"""

    def __init__(self, q: np.ndarray) -> None:
        """
        Inizializza la classe con i carichi distribuiti costanti [qx, qy] in N/mm nel sistema globale
        """
        # controlla che l'array q abbia la forma corretta
        if q.shape != (2,):
            raise ValueError(
                "q deve essere un array di forma (2,). e deve contenre 2 valori [qx, qy]"
            )
        self.P = q

    def __str__(self) -> str:
        """restituisce una stringa di rappresentazione della classe"""
        match self.P:
            case [0, 0]:
                return "---"
            case [0, qy] if qy != 0:
                return f"qy:{qy:.1f} kN/m"
            case [qx, 0] if qx != 0:
                return f"qx:{qx:.1f} kN/m"
            case [qx, qy] if qx != 0 and qy != 0:
                return f"qx:{qx:.1f},qy:{qy:.1f} kN/m"

    def solve(
        self,
        length: int,
        angle: float,
        releases: tuple[bool, bool],
    ) -> np.ndarray:

        l = length
        # estrai i valori dal parametro q
        qn, qt = self.to_local(angle)

        # AZIONI LONGITUDINALI lungo l'asse della trave
        ##################################
        Ni = qn * l / 2
        Nj = qn * l / 2

        axial = np.array([Ni, 0, 0, Nj, 0, 0], dtype=float)

        # AZIONI TRASVERSALI normali all'asse della trave
        ##################################
        match releases:
            case (False, False):
                Ti = qt * l / 2
                Mi = qt * l**2 / 12
                Tj = qt * l / 2
                Mj = -qt * l**2 / 12

            case (True, False):
                Ti = qt * l * 3 / 8
                Mi = 0
                Tj = qt * l * 5 / 8
                Mj = -qt * l**2 / 8

            case (False, True):
                Ti = qt * l * 5 / 8
                Mi = qt * l**2 / 8
                Tj = qt * l * 3 / 8
                Mj = 0

            case (True, True):
                Ti = qt * l / 2
                Mi = 0
                Tj = qt * l / 2
                Mj = 0

        transverse = np.array([0, Ti, Mi, 0, Tj, Mj], dtype=float)

        # somma i carichi equivalenti
        local_eq_loads = axial + transverse
        # ruota i carichi locali nel sistema globale della trave
        # [Ni, Ti, Mi, Nj, Tj, Mj] => [Xi, Yi, Mi, Xj, Vj, Mj]
        # l'angolo è negativo perchè ripercorre la rotazione all'inverso
        return self.to_global(local_eq_loads, -angle)
