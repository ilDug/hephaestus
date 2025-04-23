from typing import Annotated, Literal
import numpy as np
from .node import Node
from ..matrices import RotationMatrix2D, StiffnessMatrix2D
from ..materials import Material, select_material
from ..sections import Section, select_section
from ..loads import DistributedLoad, PointLoad, MomentumLoad, ExternalLoad


class Beam:
    tag: str
    """identficativo della trave"""

    material: Material
    """materiale della trave"""

    section: Section
    """sezione della trave"""

    i: Node
    """il nodo iniziale della trave"""

    j: Node
    """il nodo finale della trave"""

    releases: tuple[bool, bool] = (False, False)
    """rilascio interni della trave"""

    L: int
    """lunghezza della trave in mm"""

    side: Literal["MAJOR", "MINOR"] = "MAJOR"
    """lato della sezione su cui si applica il carico"""

    def __init__(self, start: Node, end: Node):
        """crea una nuova trave tra due nodi"""
        self.i = start
        self.j = end
        self.L = ((self.j.x - self.i.x) ** 2 + (self.j.y - self.i.y) ** 2) ** (1 / 2)
        self.tag = f"{self.i.tag}-{self.j.tag}"

        self.ext_loads: list[ExternalLoad] = []
        """carichi esterni applicati alla trave"""

    def set_material(self, material: str) -> "Beam":
        """imposta il materiale della trave"""
        m = select_material(material)
        self.material = m
        return self

    def set_section(self, section: str) -> "Beam":
        """ "imposta le proprietà della sezione trasversale della trave"""
        s = select_section(section)
        self.section = s
        return self

    def set_internal_releases(
        self, releases: tuple[bool, bool] = (False, False)
    ) -> "Beam":
        """imposta i rilasci interni della trave. True se il rilascio è presente, False altrimenti"""
        self.releases = releases
        return self

    def set_side(self, side: Literal["MAJOR", "MINOR"]) -> "Beam":
        """imposta su quale lato della sezione si applica il carico"""
        if side not in ["MAJOR", "MINOR"]:
            raise ValueError("side must be either 'MAJOR' or 'MINOR'")
        self.side = side
        return self

    def apply_distributed_load(
        self,
        qx: float = None,
        qy: float = None,
    ) -> "Beam":
        """applica un carico distribuito alla trave."""

        # genera un caico distribuito
        # self.dload = DistributedLoad(np.array([qx, qy], dtype=float))
        self.ext_loads.append(DistributedLoad(np.array([qx, qy], dtype=float)))
        return self

    def apply_point_load(self, x: int, fx: float = None, fy: float = None) -> "Beam":
        """applica un carico puntuale alla trave.
        fx: carico in direzione X in kN
        fy: carico in direzione Y in kN
        x: posizione del carico lungo la trave in mm
        """
        raise NotImplementedError(
            "Per ora non è possibile applicare carichi puntuali. Migliorare il modulo di analisi per prendere in considerazion i contributi dei carichi puntuali."
        )

        # controlla se il carico è  nullo
        if not fx and not fy:
            raise ValueError("carico nullo")
        if x > self.L:
            raise ValueError(
                "la posizione del carico deve essere minore della lunghezza della trave"
            )
        if x < 0:
            raise ValueError("la posizione del carico deve essere maggiore di 0")
        # concerte il carico in  N
        fx = fx * 1000 if fx else 0
        fy = fy * 1000 if fy else 0

        # genera un carico puntuale
        pload = PointLoad(np.array([fx, fy], dtype=float), x)
        self.ext_loads.append(pload)
        return self

    def apply_momentum_load(self, x: int, M: float) -> "Beam":
        """applica un momento alla trave.
        M: momento in kNm
        x: posizione del carico lungo la trave in mm
        """
        # controlla se il carico è  nullo
        if not M:
            raise ValueError("carico nullo")
        if x > self.L:
            raise ValueError(
                "la posizione del carico deve essere minore della lunghezza della trave"
            )
        if x < 0:
            raise ValueError("la posizione del carico deve essere maggiore di 0")
        # genera un carico puntuale
        m = M * 1000000 if M else 0
        mload = MomentumLoad(x, m)
        self.ext_loads.append(mload)
        return self

    def stiffness_matrix(self) -> np.ndarray:
        """genera la matrice di rigidezza della trave ruotata nel sistema globale"""
        try:
            # calcola il moment odi inerzia della sezione in base al lato su cui si applica il carico
            I = self.section.Iy if self.side == "MAJOR" else self.section.Iz
            A = self.section.A
            E = self.material.E
            L = self.L
            # stiffness matrix locale
            K = StiffnessMatrix2D(E, A, I, L).with_release(self.releases).matrix()
            R = RotationMatrix2D.x6(self.angle())  # rotation matrix
            # stiffness matrix trasformata nel sistema globale usando la matrice di rotazione
            G = R.T @ K @ R  # [Kg] = [R]^T * [K] * [R]
            return G  # local stiffness matrix in the global system
        except Exception as e:
            err = f"BEAM CLASS: error generating rotated stiffness matrix for beam {self.tag}: {e}"
            print(err)
            raise Exception(err)

    def angle(self) -> float:
        """calcola l'angolo di rotazione della trave in radianti rispetto all'asse x globale"""
        dx = self.j.x - self.i.x
        dy = self.j.y - self.i.y

        if dx == 0 and dy == 0:
            raise ValueError("dx and dy are both 0")

        # analzza i casi in cui dx o dy sono 0
        if dx == 0 and dy > 0:  # trave verticale con verso l'alto
            return np.pi / 2

        if dx == 0 and dy < 0:  # trave verticale con verso il basso
            return (3 / 2) * np.pi

        if dy == 0 and dx > 0:  # trave orizzontale con verso a destra
            return 0

        if dy == 0 and dx < 0:  # trave orizzontale con verso a sinistra
            return np.pi

        # analizza i casi in cui dx o dy sono diversi da 0
        if dx > 0 and dy > 0:  # primo quadrante
            return np.arctan(dy / dx)

        if dx < 0 and dy > 0:  # secondo quadrante
            return np.pi + np.arctan(dy / dx)

        if dx < 0 and dy < 0:  # terzo quadrante
            return np.pi + np.arctan(dy / dx)

        if dx > 0 and dy < 0:  # quarto quadrante
            return 2 * np.pi + np.arctan(dy / dx)

    def equivalent_loads(
        self, by_node: bool = True
    ) -> tuple[np.ndarray, np.ndarray] | np.ndarray:
        """calcola i carichi equivalenti sui nodi della trave dovuti ai carichi sull'elemento"""
        L = np.zeros(6, dtype=float)
        for load in self.ext_loads:
            L += load.solve(self.L, self.angle(), self.releases)
        return (L[:3], L[3:]) if by_node else L  # carichi equivalenti sui nodi i e j

    def nodal_strengths(
        self,
        di: np.ndarray,
        dj: np.ndarray,
    ) -> np.ndarray:
        """calcola le forze interne applicate sugli estremi della trave in base alla soluzione del problema
        di: spostamento globale del nodo i (calcolato dalla risoluzione del frame globale)
        dj: spostamento globale del nodo j  (calcolato dalla risoluzione del frame globale)
        """
        # get node displacement from solution
        d_global = np.hstack((di, dj))

        # rotate displacement vector to local coordinates of the beam
        R = RotationMatrix2D.x6(self.angle())
        d = R @ d_global.reshape(-1, 1)

        E = self.material.E
        A = self.section.A
        I = self.section.Iy if self.side == "MAJOR" else self.section.Iz
        L = self.L

        # matrice di rigidezza locale
        K = StiffnessMatrix2D(E, A, I, L).with_release(self.releases).matrix()
        # carichi equivalenti globali dovuti ai carichi esterni applicati direttamente alla trave
        eq_global = self.equivalent_loads(by_node=False)
        # ruota i carichi equivalenti nel sistema locale della trave
        eq = R @ eq_global.reshape(-1, 1)
        # calcola le forze interne globali
        # [Ni, Ti, Mi, Nj, Tj, Mj] = [K] @ {d} - {eq}
        # (eq è negativo per trasformare le forze sui nodi in quelle sulla trave)
        f = K @ d.reshape(-1, 1) - eq
        f = f.flatten()  # [Ni, Ti, Mi, Nj, Tj, Mj]
        return f  # [Ni, Ti, Mi, Nj, Tj, Mj] (forze interne sui nodi i e j)
