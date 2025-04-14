import numpy as np


class DistributedLoad:
    """implementazioen di EquivalentLoad per un carico distribuito costano o linearmente variabile"""

    q: np.ndarray
    """carico distribuito costante lungo la trave [qxi, qyi, qxj, qyj] in N/mm nelle coordinate globali"""

    # def __init__(self, length:int, angle: float,  releases: tuple[bool, bool] = (False, False)):
    #     """
    #     Inizializza la classe con la lunghezza della trave e l'angolo di inclinazione e i rilasci nodali.
    #     La lunghezza della trave è in mm, l'angolo è in radianti.
    #     I rilasci si rifieriscono ai nodi i e j della trave.
    #     Se il rilascio è True, il nodo è una cerniera.
    #     Se il rilascio è False, il nodo è un incastro.
    #     """
    #     self.length = length
    #     self.angle = angle
    #     self.releases = releases

    def __init__(self, q: np.ndarray) -> None:
        """
        Inizializza la classe con i carichi distribuiti costanti [qxi, qyi, qxj, qyj] in N/mm nel sistema globale
        """
        # controlla che l'array q abbia la forma corretta
        if q.shape != (4,):
            raise ValueError(
                "q deve essere un array di forma (4,). e deve contenre 4 valori [qxi, qyi, qxj, qyj]"
            )
        self.q = q

    def to_local(self, angle: float) -> np.ndarray:
        """
        Ruota i carichi globali nel sistema locale della trave.
        [qxi, qyi, qxj, qyj] => [qni, qti, qnj, qtj]
        """
        c = np.cos(angle)
        s = np.sin(angle)

        # matrice di rotazione per il carico distribuito
        R = np.array(
            [
                [c, s, 0, 0],
                [-s, c, 0, 0],
                [0, 0, c, s],
                [0, 0, -s, c],
            ],
            dtype=float,
        )
        # calcola i carichi ruotati nel sistema locale della trave
        # [qxi, qyi, qxj, qyj] => [qni, qti, qnj, qtj]
        local_loads = R @ self.q.reshape(-1, 1)
        # il vettore dei carichi deve essere un  vettore con una sola riga
        local_loads = local_loads.flatten()
        return local_loads

    def to_global(self, loads: np.ndarray, angle: float) -> np.ndarray:
        """
        Ruota i carichi locali nel sistema globale della trave.
        [Ni, Ti, Mi, Nj, Tj, Mj] => [Xi, Yi, Mi, Xj, Vj, Mj]
        """
        # controlla che l'array loads abbia la forma corretta
        if loads.shape != (6,):
            raise ValueError(
                "loads deve essere un array di forma (6,). e deve contenre 6 valori [Ni, Ti, Mi, Nj, Tj, Mj]"
            )

        c = np.cos(angle)
        s = np.sin(angle)

        R = np.array(
            [
                [c, s, 0, 0, 0, 0],
                [-s, c, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0],
                [0, 0, 0, c, s, 0],
                [0, 0, 0, -s, c, 0],
                [0, 0, 0, 0, 0, 1],
            ],
            dtype=float,
        )

        # calcola i carichi ruotati nel sistema globale della trave
        # [Ni, Ti, Mi, Nj, Tj, Mj] => [Xi, Yi, Mi, Xj, Vj, Mj]
        global_loads = R @ loads.reshape(-1, 1)
        # il vettore dei carichi deve essere un  vettore con una sola riga
        global_loads = global_loads.flatten()
        return global_loads

    def solve(
        self,
        length: int,
        angle: float,
        releases: tuple[bool, bool],
    ) -> np.ndarray:

        # estrai i valori dal parametro q
        qni, qti, qnj, qtj = self.to_local(angle)

        # AZIONI LONGITUDINALI lungo l'asse della trave
        ##################################
        # carico totale dovuto alla forza assiale (trapezio)
        N = (qni + qnj) / 2 * length
        # ogni nodo ha la metà del carico totale assiale
        Ni = N / 2
        Nj = N / 2

        axial = np.array([Ni, 0, 0, Nj, 0, 0], dtype=float)

        # AZIONI TRASVERSALI normali all'asse della trave
        ##################################

        # calcola il delta di carico trasversale, in valore assoluto
        delta_qt = abs(qtj - qti)

        # calcola la parte costante (rettangolare)
        qt = max(qti, qtj) - delta_qt

        # carichi dovuti alla parte COSTANTE del carico
        match releases:
            case (False, False):
                Tic = qt * length / 2
                Mic = qt * length**2 / 12
                Tjc = qt * length / 2
                Mjc = -qt * length**2 / 12

            case (True, False):
                Tic = qt * length * 3 / 8
                Mic = 0
                Tjc = qt * length * 5 / 8
                Mjc = -qt * length**2 / 8

            case (False, True):
                Tic = qt * length * 5 / 8
                Mic = qt * length**2 / 8
                Tjc = qt * length * 3 / 8
                Mjc = 0

            case (True, True):
                Tic = qt * length / 2
                Mic = 0
                Tjc = qt * length / 2
                Mjc = 0

        constants = np.array([0, Tic, Mic, 0, Tjc, Mjc], dtype=float)

        # calcola i carichi dovuti alla parte VARIABILE del carico
        match releases:
            case (False, False):
                Tiv = 3 / 20 * delta_qt * length
                Miv = 1 / 30 * delta_qt * length**2
                Tjv = 7 / 20 * delta_qt * length
                Mjv = -1 / 20 * delta_qt * length**2

            case (True, False):
                Tiv = 0
                Miv = 0
                Tjv = 0
                Mjv = 0

            case (False, True):
                Tiv = 0
                Miv = 0
                Tjv = 0
                Mjv = 0

            case (True, True):
                Tiv = 0
                Miv = 0
                Tjv = 0
                Mjv = 0

        # se il nodo j non è il  nodo con il carico maggiore, scambia i valori
        if qti > qtj:
            Tiv, Miv, Tjv, Mjv = Tjv, Mjv, Tiv, Miv

        variables = np.array([0, Tiv, Miv, 0, Tjv, Mjv], dtype=float)

        # somma i carichi equivalenti
        local_eq_loads = axial + constants + variables
        # ruota i carichi locali nel sistema globale della trave
        # [Ni, Ti, Mi, Nj, Tj, Mj] => [Xi, Yi, Mi, Xj, Vj, Mj]
        # l'angolo è negativo perchè ripercorre la rotazione all'inverso
        return self.to_global(local_eq_loads, -angle)
