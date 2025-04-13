from typing import Annotated, Literal
import numpy as np
from .node import Node
from ..matrix import generate_stiffness_matrix_2d, generate_rotation_matrix_2d
from ..materials import Material
from ..sections import Section
from ..loads import *

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

    dload: tuple[float, float] = (0, 0)
    """carico distribuito iniziale e finale in direzione perpendicolare alla trave in kN/m"""

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

    def apply_distributed_load(self, qi: float, qj: float = None) -> "Beam":
        """applica un carico distribuito in direzione perpendicolare alla trave
        - qi: carico distribuito iniziale in kN/m
        - qj: carico distribuito finale in kN/m
        """
        # controlla se il carico è nullo
        if qi == 0 and (qj is None or qj == 0):
            raise ValueError("qi and qj cannot be both 0")

        # Se qj è nullo, lo imposta uguale a qi
        if qj is None:
            qj = qi

        # converte da kN/m a N/mm
        qi = qi * 1e3 / 1e3
        qj = qj * 1e3 / 1e3

        # imposta i carichi distribuiti
        self.dload = (qi, qj)

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

        # carichi equivalenti nel sistema locale
        qi, qj = self.dload
        L = self.L

        match self.releases:
            case (False, False):
                eq_loads = equivalent_beam_loads_vector_2d_fixed_fixed(qi, qj, L)
            case (False, True):
                pass
            case (True, False):
                pass
            case (True, True):
                pass

        # ruota i carichi equivalenti nel sistema globale
        R = self.rotation_matrix()
        # carichi equivalenti trasformati nel sistema globale usando la matrice di rotazione
        G = R @ eq_loads.reshape(-1, 1)
        # il vettore dei carichi deve essere un  vettore con una sola riga
        G = G.flatten()

        return G[:3], G[3:]  # carichi equivalenti sui nodi i e j
