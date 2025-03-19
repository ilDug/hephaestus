import numpy as np


class Node:
    n: int  # ID del nodo
    c: tuple[float, float]  # coordinate assolute in metri

    x: float  # coordinate assolute in millimetri
    y: float  # coordinate assolute in millimetri
    coordinates: tuple[float, float]  # coordinate assolute in millimetri

    restraints: tuple[bool, bool, bool] = (
        False,
        False,
        False,
    )  # vicoli (x, y, rz)

    M0: float = 0  # momento esterno applicato (in coordinate globali) in kNm
    V0: float = 0  # forza verticale esterna applicata  (in coordinate globali) in kN
    H0: float = 0  # forza orizzontale esterna applicata ( in coordinate globali) in kN

    def __init__(self, id: int, coordinates: tuple[float, float]):
        self.n = id
        self.coordinates = coordinates
        self.x, self.y = coordinates
        print(f"created new node at coordinates {self.coordinates}")

    def set_restraints(self, x: bool, y: bool, rz: bool):
        """Set GLOBAL restraints for the node. True = fix; False = free"""
        self.restraints = (x, y, rz)
        print(
            f"set restraints for node {self.n}. Global translation x: {'fixed' if x else 'free'}, Global translation y: {'fixed' if y else 'free'}, Global rotation rz: {'fixed' if rz else 'free'}"
        )

    def apply_loads(self, Fx: float = 0, Fy: float = 0, Mz: float = 0):
        """Apply loads to the node. Fx, Fy, Mz in kN and kNm"""
        self.H0, self.V0, self.M0 = Fx * 1000, Fy * 1000, Mz * 1000
        print(
            f"applied loads to node {self.n}. Fx: {(self.H0/1000):.02}kN, Fy: {(self.V0/1000):.02}kN, Mz: {(self.M0/1000):.02}kNm"
        )

    def load_vector(self) -> np.ndarray:
        """Returns the load vector for the node"""
        return np.array([[self.H0, self.V0, self.M0]], dtype=float)

    # dx0 float # spostamento in coordinate globali imposto dall'esterno (in mm)
    # dy0 float # spostamento in coordinate globali imposto dall'esterno (in mm)
    # dx0 float # spostamento in coordinate globali imposto dall'esterno (in mm)

    # rx0 float # rotazione in coordinate globali imposta dell'esterno (in rad)
    # ry0 float # rotazione in coordinate globali imposta dell'esterno (in rad)
    # rz0 float # rotazione in coordinate globali imposta dell'esterno (in rad)
