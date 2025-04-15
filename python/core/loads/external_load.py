import numpy as np
from abc import ABC, abstractmethod


class ExternalLoad(ABC):
    """
    Interfaccia per i carichi equivalenti sui nodi di una trave.
    La classe deve implementare il metodo solve() che calcola i carichi equivalenti
    sui nodi della trave in funzione dei carichi applicati sulla trave.
    """

    @abstractmethod
    def solve(
        self,
        length: int,
        angle: float,
        releases: tuple[bool, bool],
    ) -> np.ndarray:
        """
        Calcola i carichi equivalenti sui nodi della trave in funzione dei carichi applicati sulla trave.
        parametri:
            length: lunghezza della trave in mm
            angle: angolo di inclinazione della trave in radianti
            releases: rilasci sul nodo i e sul nodo j. default: incastro-incastro
            Se il rilascio è True, il nodo è una cerniera.
            Se il rilascio è False, il nodo è un incastro.
        Restituisce:
            carichi equivalenti sui nodi i e j [Ni, Ti, Mi, Nj, Tj, Mj] in N e Nmm nel sistema globale
        """

    def to_local(self, angle: float) -> np.ndarray:
        """
        Ruota i carichi globali nel sistema locale della trave.
        [fx, fy] => [fn, ft]
        """

        c = np.cos(angle)
        s = np.sin(angle)

        # matrice di rotazione per il carico concentrato
        R = np.array(
            [
                [c, s],
                [-s, c],
            ],
            dtype=float,
        )
        # calcola i carichi ruotati nel sistema locale della trave
        # [fx, fy] => [fn, ft]
        local_loads = R @ self.P.reshape(-1, 1)
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
