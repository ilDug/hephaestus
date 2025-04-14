from typing import Annotated, Literal
import numpy as np
from .node import Node
from ..matrix import (
    generate_stiffness_matrix_2d,
    generate_rotation_matrix_2d,
    distributed_loads_rotation_matrix_2d,
)
from ..materials import Material
from ..sections import Section
from ..loads import EquivalentLoad, PointLoad, DistributedLoad

class Beam:
    id: str
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

    L: float
    """lunghezza della trave in mm"""

    side: Literal["MAJOR", "MINOR"] = "MAJOR"
    """lato della sezione su cui si applica il carico"""

    external_loads: list[EquivalentLoad] = []
    """lista dei carichi esterni applicati alla trave"""

    def __init__(self, start: Node, end: Node):
        """crea una nuova trave tra due nodi"""
        self.i = start
        self.j = end
        self.L = ((self.j.x - self.i.x) ** 2 + (self.j.y - self.i.y) ** 2) ** (1 / 2)
        self.id = f"{self.i.id}-{self.j.id}"

    def set_material(self, material: Material) -> "Beam":
        """imposta il materiale della trave"""
        self.material = material
        return self

    def set_section(self, section: Section) -> "Beam":
        """ "imposta le proprietà della sezione trasversale della trave"""
        self.section = section
        return self

    def set_internal_releases(self, i: bool = False, j: bool = False) -> "Beam":
        """imposta i rilasci interni della trave"""
        self.releases = (i, j)
        return self

    def set_side(self, side: Literal["MAJOR", "MINOR"]) -> "Beam":
        """imposta su quale lato della sezione si applica il carico"""
        if side not in ["MAJOR", "MINOR"]:
            raise ValueError("side must be either 'MAJOR' or 'MINOR'")
        self.side = side
        return self

    def apply_distributed_load(
        self,
        qxi: float = None,
        qyi: float = None,
        qxj: float = None,
        qyj: float = None,
    ) -> "Beam":
        """applica un carico distribuito in direzione perpendicolare alla trave
        - qi: carico distribuito iniziale in kN/m
        - qj: carico distribuito finale in kN/m
        """
        # controlla se il carico è nullo
        if qxi is None and qyi is None:
            raise ValueError("carico nullo")

        # Se qj è nullo, lo imposta uguale a qi
        if qxj is None:
            qxj = qxi
        if qyj is None:
            qyj = qyi

        # genera un caico distribuito
        dload = DistributedLoad(np.array([qxi, qyi, qxj, qyj], dtype=float))
        self.external_loads.append(dload)
        print(f"carico distribuito {dload.q} kN/m applicato alla trave {self.id}")
        return self

    def apply_point_load(self, x: int, fx: float = None, fy: float = None) -> "Beam":
        """applica un carico puntuale alla trave.
        fx: carico in direzione X in kN
        fy: carico in direzione Y in kN
        x: posizione del carico lungo la trave in mm
        """
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
        self.external_loads.append(pload)
        return self

    def stiffness_matrix_local(self) -> np.ndarray:
        """genera la matrice di rigidezza locale della trave"""
        try:
            inertial_momentum = (
                self.section.Iy if self.side == "MAJOR" else self.section.Iz
            )
            # calcola la matrice di rigidezza locale della trave
            # usando le proprietà della sezione e del materiale
            K = generate_stiffness_matrix_2d(
                self.material.E,
                self.section.A,
                inertial_momentum,
                self.L,
                self.releases,
            )
            return K
        except Exception as e:
            err = f"BEAM CLASS: error generating local stiffness matrix for beam {self.id}: {e}"
            print(err)
            raise Exception(err)

    def stiffness_matrix(self) -> np.ndarray:
        """genera la matrice di rigidezza della trave ruotata nel sistema globale"""
        try:
            K = self.stiffness_matrix_local()  # stiffness matrix locale
            R = self.rotation_matrix()  # rotation matrix
            # stiffness matrix trasformata nel sistema globale usando la matrice di rotazione
            G = R.T @ K @ R  # [Kg] = [R]^T * [K] * [R]
            return G  # local stiffness matrix in the global system
        except Exception as e:
            err = f"BEAM CLASS: error generating rotated stiffness matrix for beam {self.id}: {e}"
            print(err)
            raise Exception(err)

    def rotation_angle(self) -> float:
        """calcola l'angolo di rotazione della trave in radianti"""
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

    def rotation_matrix(self) -> np.ndarray:
        """genera la matrice di rotazione della trave"""
        angle = self.rotation_angle()
        return generate_rotation_matrix_2d(angle)

    def equivalent_loads(self) -> np.ndarray:
        """calcola i carichi equivalenti sui nodi della trave dovuti ai carichi distribuiti"""
        L = np.zeros(6, dtype=float)
        for load in self.external_loads:
            # calcola i carichi equivalenti sui nodi della trave
            # usando la matrice di rigidezza locale e la matrice di rotazione
            L += load.solve(self.L, self.rotation_angle(), self.releases)

        return L[:3], L[3:]  # carichi equivalenti sui nodi i e j
