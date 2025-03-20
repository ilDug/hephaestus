from .beam import Beam
from .node import Node
import numpy as np

class Frame:

    nodes: list[Node] = []
    beams: list[Beam] = []

    def __init__(self):
        pass

    def add_node(self, coordinates: tuple[float, float]) -> int:
        """Aggiunge un nodo alla struttura"""
        node = Node(len(self.nodes) + 1, coordinates)
        self.nodes.append(node)
        return node.id

    def add_beam(self, n1: int, n2: int) -> Beam:
        """Aggiunge un elemento alla struttura"""
        i = next(node for node in self.nodes if node.id == n1)
        j = next(node for node in self.nodes if node.id == n2)
        beam = Beam(i, j)
        self.beams.append(beam)
        return beam

    def node(self, n: int) -> Node:
        """Restituisce il nodo con ID n"""
        return next(node for node in self.nodes if node.id == n)

    def beam(self, n1: int, n2: int) -> Beam:
        """Restituisce il beam con nodi n1 e n2"""
        names = [f"{n1}-{n2}", f"{n2}-{n1}"]
        return next(beam for beam in self.beams if beam.id in names)

    def restraints_vector(self) -> np.ndarray:
        """Returns the restraints matrix for the frame"""
        return (
            np.concatenate([node.restraints for node in self.nodes])
            .astype(int)
            .reshape(-1, 1)
        )

    def loads_vector(self) -> np.ndarray:
        """Returns the loads vector for the frame"""
        return np.concatenate([node.load_vector() for node in self.nodes]).reshape(
            -1, 1
        )

    def global_stiffness_matrix(self) -> np.ndarray:
        """Returns the global stiffness matrix for the frame"""
        # calculate the size of the matrix : number of nodes * 3
        n = len(self.nodes) * 3

        # initialize the global stiffness matrix with zeros
        K = np.zeros((n, n))

        # add the stiffness matrix of each beam to the global stiffness matrix
        for beam in self.beams:
            i = (beam.i.id - 1) * 3
            j = (beam.j.id - 1) * 3

            # add the stiffness matrix of the beam to the global stiffness matrix
            k_local = beam.stiffness_matrix()

            K[i : i + 3, i : i + 3] += k_local[:3, :3]  # primo quadrante
            K[j : j + 3, j : j + 3] += k_local[3:, 3:]  # quarto quadrante
            K[i : i + 3, j : j + 3] -= k_local[:3, 3:]  # secondo quadrante
            K[j : j + 3, i : i + 3] -= k_local[3:, :3]  # terzo quadrante
        return K

    def displacemets_vector(self) -> np.ndarray:
        """Returns the displacements vector for the frame"""
        # [K] x {d} = {F}
        # {d} = [K]^-1 x {F}

        # calculate the global stiffness matrix, restraints vector, and loads vector
        K = self.global_stiffness_matrix()
        R = self.restraints_vector()
        F = self.loads_vector()

        # setting the rows and columns of the restraints to zero
        # and setting the diagonal to 1 to avoid singular matrix
        # annulla le righe e le colonne della matrice di rigidezza per i nodi vincolati
        Kr = K.copy()
        for i in range(len(R)):
            if R[i] == 1:
                Kr[i, :] = 0
                Kr[:, i] = 0
                Kr[i, i] = 1  # Set diagonal to 1 to avoid singular matrix

        # solve the equation [K] x {d} = {F} for {d}
        D = np.linalg.solve(Kr, F)

        return D
