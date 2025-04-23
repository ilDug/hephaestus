import numpy as np


class Node:
    id: int
    """ID del nodo"""

    tag: str
    """tag del nodo"""

    x: float
    """ascissa assoluta in millimetri """

    y: float
    """ordinata assoluta in millimetri """

    coordinates: tuple[float, float]
    """coordinate assolute in millimetri """

    restraints: list[int, int, int] = [0, 0, 0]
    """vincoli (x, y, rz) in coordinate globali (1 = vincolato, 0 = libero) """

    loads: np.ndarray = np.array([0.0, 0.0, 0.0], dtype=float)
    """carichi (Fx, Fy, Mz) in coordinate globali (N, N, Nm)"""

    def __init__(self, id: int, tag: str, coordinates: tuple[float, float]):
        self.id = id
        self.tag = tag
        self.coordinates = coordinates
        self.x, self.y = coordinates

    def set_restraints(
        self, x: int | bool = False, y: int | bool = False, rz: int | bool = False
    ):
        """Set GLOBAL restraints for the node. True = fix; False = free"""
        x = int(bool(x))
        y = int(bool(y))
        rz = int(bool(rz))
        self.restraints = [x, y, rz]

    def apply_loads(self, Fx: float = 0, Fy: float = 0, Mz: float = 0):
        """Apply loads to the node. Fx, Fy, Mz in kN and kNm"""
        self.loads = np.array([Fx * 1000, Fy * 1000, Mz * 1000000], dtype=float)
