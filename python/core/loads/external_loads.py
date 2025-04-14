from abc import abstractmethod
import numpy as np
from typing import Protocol


class ExternalLoad(Protocol):
    def to_local(self, angle: float):
        """
        Ruota i carichi globali nel sistema locale della trave.
        """
        pass


class DistributedConstantLoad(ExternalLoad):
    """
    Carico distribuito costante lungo la trave.
    La classe deve implementare il metodo to_local() che calcola i carichi locali
    in funzione dei carichi globali applicati alla trave.
    """
    q: np.ndarray
    """carico distribuito costante lungo la trave [qx, qy] in N/mm nelle coordinate globali"""


    def __init__(self, q: np.ndarray) -> None:
        """
        Inizializza la classe con i carichi distribuiti costanti [qn, qt] in N/mm
        """
        # controlla che l'array q abbia la forma corretta
        if q.shape != (2,):
            raise ValueError(
                "q deve essere un array di forma (2,). e deve contenre 2 valori [qn, qt]"
            )
        self.q = q

    def to_local(self, angle: float) -> np.ndarray:
        """
        Ruota i carichi globali nel sistema locale della trave.
        """
        s = np.sin(angle)
        c = np.cos(angle)
        # matrice di rotazione per il carico distribuito
        R = np.array(
            [
                [c, s],
                [-s, c],
            ],
            dtype=float,    
        )

        # calcola i carichi ruotati nel sistema locale della trave
        # [qn, qt] => [qni, qti]
        local_loads = R @ self.q.reshape(-1, 1)
        # il vettore dei carichi deve essere un  vettore con una sola riga
        local_loads = local_loads.flatten()
        return local_loads
    

class DistributedLinearLoad(ExternalLoad):
    """
    Carico distribuito lineare lungo la trave.
    La classe deve implementare il metodo to_local() che calcola i carichi locali
    in funzione dei carichi globali applicati alla trave.
    """
    q: np.ndarray
    """carico distribuito lineare lungo la trave [qx] in N/mm nelle coordinate globali"""

    def __init__(self, q: np.ndarray) -> None:
        """
        Inizializza la classe con i carichi distribuiti lineari [qn, qt] in N/mm
        """
        # controlla che l'array q abbia la forma corretta
        if q.shape != (4,):
            raise ValueError(
                "q deve essere un array di forma (4,). e deve contenre 4 valori [qni, qti, qnj, qtj]"
            )
        self.q = q