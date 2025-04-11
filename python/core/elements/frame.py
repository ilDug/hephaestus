from .beam import Beam
from .node import Node
import numpy as np
from ..solution import FrameSolution

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

    def add_beam(self, i: int, j: int) -> Beam:
        """Aggiunge un elemento alla struttura"""
        start = self.node(i)
        end = self.node(j)
        beam = Beam(start, end)
        self.beams.append(beam)
        return beam

    def node(self, n: int) -> Node:
        """Restituisce il nodo con ID n"""
        return next(node for node in self.nodes if node.id == n)

    def beam(self, n1: int, n2: int) -> Beam:
        """Restituisce il beam con nodi n1 e n2"""
        names = [f"{n1}-{n2}", f"{n2}-{n1}"]
        return next(beam for beam in self.beams if beam.id in names)

    def restraints(self, by_node: bool = True) -> np.ndarray:
        """Returns the restraints matrix for the frame"""

        # concatenates the restraints of all nodes to a matrix of size (n, 3)
        restraints = np.vstack([n.restraints for n in self.nodes]).astype(int)

        # if by_node == False it reshapes the restraints to a vector of size (n, 1)
        return restraints if by_node else restraints.reshape(-1, 1)

    def loads(self, by_node: bool = True) -> np.ndarray:
        """Returns the loads vector for the frame"""

        # concatenates the loads of all nodes to a matrix of size (n, 3)
        loads = np.vstack([n.loads for n in self.nodes])

        # if by_node == False it reshapes the loads to a vector of size (n, 1)
        return loads if by_node else loads.reshape(-1, 1)

    def global_stiffness_matrix(self) -> np.ndarray:
        """Returns the global stiffness matrix for the frame"""
        # calculate the size of the matrix : number of nodes * 3
        n = len(self.nodes) * 3

        # initialize the global stiffness matrix with zeros
        K = np.zeros((n, n))

        try:
            # add the stiffness matrix of each beam to the global stiffness matrix
            for beam in self.beams:
                i = (beam.i.id - 1) * 3
                j = (beam.j.id - 1) * 3

                # add the stiffness matrix of the beam to the global stiffness matrix
                k_local = beam.stiffness_matrix()

                K[i : i + 3, i : i + 3] += k_local[:3, :3]  # primo quadrante
                K[j : j + 3, j : j + 3] += k_local[3:, 3:]  # quarto quadrante
                K[i : i + 3, j : j + 3] += k_local[:3, 3:]  # secondo quadrante
                K[j : j + 3, i : i + 3] += k_local[3:, :3]  # terzo quadrante
            return K
        except Exception as e:
            print(f"FRAME CLASS: Error in global stiffness matrix: {e}")
            raise ValueError(f"Error in global stiffness matrix: {e}")

    def displacements(self, by_node: bool = True) -> np.ndarray:
        """Returns the displacements vector for the frame"""
        # [K] x {d} = {F}
        # {d} = [K]^-1 x {F}

        # calculate the global stiffness matrix, restraints vector, and loads vector
        K = self.global_stiffness_matrix()
        X = self.restraints(by_node=False)
        L = self.loads(by_node=False)

        # setting the rows and columns of the restraints to zero
        # and setting the diagonal to 1 to avoid singular matrix
        # annulla le righe e le colonne della matrice di rigidezza per i nodi vincolati
        Kr = K.copy()
        for i in range(len(X)):
            if X[i] == 1:
                Kr[i, :] = 0
                Kr[:, i] = 0
                Kr[i, i] = 1  # Set diagonal to 1 to avoid singular matrix

        # inverte i gradi di libertà con i gradi di vincolo in modo da
        # annullare  le righe  del vettore dei carichi per i nodi vincolati
        R = np.logical_not(X).astype(int)

        # annulla le righe del vettore dei carichi per i nodi vincolati
        F = R * L

        # solve the equation [K] x {d} = {F} for {d}
        D = np.linalg.solve(Kr, F)

        # reshape the displacements vector to a matrix of size (n, 3) if by_node is True
        # altrimenti restituisce il vettore colonna di spostamenti di dimensione (n, 1)
        return D if not by_node else D.reshape(-1, 3)

    def reactions(self, by_node: bool = True) -> np.ndarray:
        """Solves the frame"""
        # [A] = [K] x {d} - {F}

        # calculate the global stiffness matrix, restraints vector, and loads vector
        K = self.global_stiffness_matrix()
        F = self.loads(by_node=False)
        D = self.displacements(by_node=False)

        # [A] è il vettore colonna che contiene le reazioni vincolari
        A = K @ D - F

        # reshape the reactions vector to a matrix of size (n, 3) if by_node is True
        # altrimenti restituisce il vettore colonna di reazioni di dimensione (n, 1)
        return A if not by_node else A.reshape(-1, 3)

    def solve(self) -> FrameSolution:
        """Solves the frame and returns the solution object grouped by node
        - the restraints vector X
        - the load vector L
        - the reactions vector R
        - the displacements vector D,
        """
        # nodes list
        N = self.nodes
        # beams list
        B = self.beams
        # restraints array
        X = self.restraints()
        # loads array
        L = self.loads()
        # reactions array
        R = self.reactions()
        # displacements array
        D = self.displacements()

        return FrameSolution(N, B, X, L, R, D)
