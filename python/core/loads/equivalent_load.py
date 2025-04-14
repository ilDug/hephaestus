from abc import abstractmethod
import numpy as np
from typing import Protocol









class EquivalentLoad():
    """
    Interfaccia per i carichi equivalenti sui nodi di una trave.
    La classe deve implementare il metodo solve() che calcola i carichi equivalenti
    sui nodi della trave in funzione dei carichi applicati sulla trave.
    """

    def solve(self, loads: np.ndarray) -> None:
        """
        Calcola i carichi equivalenti sui nodi della trave in funzione dei carichi applicati sulla trave.
        Il parametro loads è da intendersi come carichi nel sistema locale della trave
        """
        


        

class EquivalentLoadBase:
    """
    Classe che calcola i carichi equivalenti sui nodi i e j di una trave
    in funzione dei carichi applicati sulla trave (definiti nel sistema locale).
    La classe calcola i carichi equivalenti sui nodi in un sistema di riferimento locale.
    La trave è definita da due nodi i e j, e da una lunghezza l.
    """

    loads = np.zeros(6, dtype=float)
    """carichi equivalenti sui nodi i e j. [Ni, Ti, Mi, Nj, Tj, Mj] in N e Nmm"""

    releases = (False, False)
    """rilasci sul nodo i e sul nodo j. default: incastro-incastro"""

    angle: float 
    """angolo di inclinazione della trave in radianti"""

    length: int  
    """lunghezza della trave in mm"""

    def __init__(self, length:int, angle: float,  releases: tuple[bool, bool] = (False, False)):
        """
        Inizializza la classe con la lunghezza della trave e l'angolo di inclinazione e ri rilasci nodali.
        La lunghezza della trave è in mm, l'angolo è in radianti.
        I rilasci si rifieriscono ai nodi i e j della trave.
        Se il rilascio è True, il nodo è una cerniera.
        Se il rilascio è False, il nodo è un incastro.
        """
        self.length = length
        self.angle = angle
        self.releases = releases

    def to_local(self, Xi:float, Yi:float, Xj:float, Yj:float) -> np.ndarray:
        """
        Ruota i carichi globali nel sistema locale della trave.
        Parametri:
            global_loads: array di carichi globali [Xi, Yi, Xj, Vj]

        Restituisce:
            local_loads: array di carichi locali [Ni, Ti,  Nj, Tj]
        """
        c = np.cos(self.angle)
        s = np.sin(self.angle)

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

        global_loads = np.array([Xi, Yi, Xj, Yj], dtype=float)

        # calcola i carichi ruotati nel sistema locale della trave
        local_loads = R @ global_loads.reshape(-1, 1)
        # il vettore dei carichi deve essere un  vettore con una sola riga
        local_loads = local_loads.flatten()
        return local_loads

    def to_global(self, local_loads: np.ndarray) -> np.ndarray:
        """
        Ruota i carichi locali nel sistema globale della trave.
        [Ni, Ti, Mi, Nj, Tj, Mj] => [Xi, Yi, Mi, Xj, Vj, Mj]

        Parametri:
            local_loads: array di carichi locali [Ni, Ti, Mi, Nj, Tj, Mj]
        """

        c = np.cos(self.angle)
        s = np.sin(self.angle)

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
        global_loads =  R @ local_loads.reshape(-1, 1)
        # il vettore dei carichi deve essere un  vettore con una sola riga
        global_loads = global_loads.flatten()

    @abstractmethod
    def solve(self, loads: np.ndarray) -> None:
        """
        Calcola i carichi equivalenti sui nodi della trave in funzione dei carichi applicati sulla trave.
        Il parametro loads è da intendersi come carichi nel sistema locale della trave
        """


class EquivalentDistributedCostantLoad(EquivalentLoadBase):

    def solve(self, q:np.ndarray) -> None:
        """
        Calcola i carichi equivalenti sui nodi della trave dovuti ai carichi distribuiti (LOCALI) costanti .
        Parametri:
            q: carico distribuito costante in N/mm nel sistema di riferimento locale della trave [qn, qt]

        Restituisce:
            carichi equivalenti sui nodi i e j [Ni, Ti, Mi, Nj, Tj, Mj] in N e Nmm
        """

        # controlla che l'array q abbia la forma corretta
        if q.shape != (2,):
            raise ValueError(
                "q deve essere un array di forma (2,). e deve contenre 2 valori [qn, qt]"
            )
        # controlla che l'array q sia di tipo float
        if not issubclass(q.dtype.type, np.floating):
            raise TypeError("q deve essere un array di tipo float")

        # estrai i valori dal parametro q
        qn, qt = q


        # AZIONI LONGITUDINALI lungo l'asse della trave
        ##################################
        #  carico totale in direzione assiale (rettangolo)
        N = qn * self.length
        # ogni nodo ha la metà del carico totale assiale
        Ni = N / 2
        Nj = N / 2

        axial = np.array([Ni, 0, 0, Nj, 0, 0], dtype=float)

        # AZIONI TRASVERSALI normali all'asse della trave
        ##################################

        match self.releases:
            case (False, False):
                Tic = +qt * self.length / 2
                Mic = +qt * self.length**2 / 12
                Tjc = +qt * self.length / 2
                Mjc = -qt * self.length**2 / 12

            case (True, False):
                Tic = +qt * self.length * 3 / 8
                Mic = 0
                Tjc = +qt * self.length * 5 / 8
                Mjc = -qt * self.length**2 / 8

            case (False, True):
                Tic = +qt * self.length * 5 / 8
                Mic = +qt * self.length**2 / 8
                Tjc = +qt * self.length * 3 / 8
                Mjc = 0

            case (True, True):
                Tic = +qt * self.length / 2
                Mic = 0
                Tjc = +qt * self.length / 2
                Mjc = 0

        transverse = np.array([0, Tic, Mic, 0, Tjc, Mjc], dtype=float)

        # somma i carichi equivalenti
        self.loads  += axial + transverse
