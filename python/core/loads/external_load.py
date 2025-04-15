import numpy as np
from typing import Protocol


class ExternalLoad(Protocol):
    """
    Interfaccia per i carichi equivalenti sui nodi di una trave.
    La classe deve implementare il metodo solve() che calcola i carichi equivalenti
    sui nodi della trave in funzione dei carichi applicati sulla trave.
    """

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
        pass

    def to_local(self, angle: float) -> np.ndarray:
        """
        Ruota i carichi globali nel sistema locale della trave.
        """
        pass

    def to_global(self, angle: float) -> np.ndarray:
        """
        Ruota i carichi locali nel sistema globale della trave.
        """
        pass
