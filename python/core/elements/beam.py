from typing import Annotated, Literal
import numpy as np
from .node import Node
from ..matrix import generate_stiffness_matrix_2d, generate_rotation_matrix_2d
from ..materials import Material
from ..sections import Section


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

    i_release: bool = False
    """rilascio del nodo iniziale"""
    j_release: bool = False
    """rilascio del nodo finale"""

    L: float
    """lunghezza della trave in mm"""

    side: Literal["MAJOR", "MINOR"] = "MAJOR"
    """lato della sezione su cui si applica il carico"""

    def __init__(self, start: Node, end: Node):
        """crea una nuova trave tra due nodi"""
        self.i = start
        self.j = end
        self.L = ((self.j.x - self.i.x) ** 2 + (self.j.y - self.i.y) ** 2) ** (1 / 2)
        self.id = f"{self.i.id}-{self.j.id}"
        print(f"the length of the beam `{self.id}` is {self.L}mm")

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
        self.i_release = i
        self.j_release = j
        return self

    def set_side(self, side: Literal["MAJOR", "MINOR"]) -> "Beam":
        """imposta su quale lato della sezione si applica il carico"""
        if side not in ["MAJOR", "MINOR"]:
            raise ValueError("side must be either 'MAJOR' or 'MINOR'")
        self.side = side
        return self

    # def apply_distributed_load(
    #     self, qi: float, qj: float = None, start: int = 0, end: int = None
    # ) -> "Beam":
    #     """applica un carico distribuito alla trave
    #     qi = carico iniziale in N/mm
    #     qj = carico finale in N/mm (default = None, carico uniforme)
    #     start = posizione iniziale del carico distribuito in mm (default = 0)
    #     end = posizione finale del carico distribuito in mm (default = None, lunghezza della trave)
    #     """
    #     if end is None:
    #         end = self.L

    #     if qj is None:
    #         qj = qi

    #     return self

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
                self.i_release,
                self.j_release,
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
        if dx == 0 and dy > 0:
            return np.pi / 2

        if dx == 0 and dy < 0:
            return (3 / 2) * np.pi

        if dy == 0 and dx > 0:
            return 0

        if dy == 0 and dx < 0:
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
