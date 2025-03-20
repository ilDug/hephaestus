import numpy as np
from .node import Node
from ..matrix import generate_stiffness_matrix_2d, generate_rotation_matrix_2d


class Beam:
    id: str  # identificativo della trave
    Ix: int  # momento d'inerzia in mm4 lungo l'asse x
    Iy: int  # momento d'inerzia in mm4 lungo l'asse y
    E: int  # modulo di elasticità in MPa (acciaio = 210000 MPa, N/mm2)
    A: int  # sezione della trave in mm2
    L: float  # lunghezza della trave in mm

    i: Node  # il nodo iniziale
    j: Node  # il nodo finale

    def __init__(self, start: Node, end: Node):
        """crea una nuova trave tra due nodi"""
        self.i = start
        self.j = end
        self.L = ((self.j.x - self.i.x) ** 2 + (self.j.y - self.i.y) ** 2) ** (1 / 2)
        self.id = f"{self.i.id}-{self.j.id}"
        print(f"the length of the beam `{self.id}` is {self.L}mm")

    def set_material(self, E: int) -> "Beam":
        """imposta il modulo di elasticità del materiale della trave.
        Valore in N/mm2 o MPa: acciacio = 210000"""
        self.E = E
        return self

    def set_section(self, A: int, Ix: int, Iy: int) -> "Beam":
        """ "imposta le proprietà della sezione trasversale della trave.
        A = area della sezione in mm2,
        Ix = momento d'inerzia in mm4 lungo l'asse x,
        Iy = momento d'inerzia in mm4 lungo l'asse y"""
        self.A = A
        self.Ix = Ix
        self.Iy = Iy
        return self

    def stiffness_matrix(self) -> np.ndarray:
        """genera la matrice di rigidezza della trave"""
        try:
            sm = generate_stiffness_matrix_2d(self.E, self.A, self.Ix, self.L)
        except Exception as e:
            print(f"error generating stiffness matrix: {e}")
            sm = None
        return sm

    def rotation_angle(self) -> float:
        """calcola l'angolo di rotazione della trave in radianti"""
        dx = self.j.x - self.i.x
        dy = self.j.y - self.i.y
        if dx == 0:
            return np.pi / 2
        if dy == 0:
            return 0
        else:
            return np.arctan(dy / dx)

    def rotation_matrix(self) -> np.ndarray:
        """genera la matrice di rotazione della trave"""
        angle = self.rotation_angle()
        return generate_rotation_matrix_2d(angle)
