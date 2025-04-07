from .beam import Beam
from .node import Node
import numpy as np
from numpy.dtypes import StringDType
from prettytable import PrettyTable


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
        start = next(node for node in self.nodes if node.id == i)
        end = next(node for node in self.nodes if node.id == j)
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

    def restraints(self) -> np.ndarray:
        """Returns the restraints matrix for the frame"""
        return (
            np.concatenate(
                [node.restraints for node in self.nodes]
            )  # concatenates the restraints of all nodes
            .astype(int)  # converts the restraints to integers
            .reshape(-1, 1)  # reshapes the restraints to a column vector
        )

    def loads(self) -> np.ndarray:
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

    def displacemets(self) -> np.ndarray:
        """Returns the displacements vector for the frame"""
        # [K] x {d} = {F}
        # {d} = [K]^-1 x {F}

        # calculate the global stiffness matrix, restraints vector, and loads vector
        K = self.global_stiffness_matrix()
        R = self.restraints()
        F = self.loads()

        # setting the rows and columns of the restraints to zero
        # and setting the diagonal to 1 to avoid singular matrix
        # annulla le righe e le colonne della matrice di rigidezza per i nodi vincolati
        Kr = K.copy()
        for i in range(len(R)):
            if R[i] == 1:
                Kr[i, :] = 0
                Kr[:, i] = 0
                Kr[i, i] = 1  # Set diagonal to 1 to avoid singular matrix

        # inverte i gradi di libertà con i gradi di vincolo in modo da
        # annullare  le righe  del vettore dei carichi per i nodi vincolati
        _R = np.logical_not(R).astype(int)

        # annulla le righe del vettore dei carichi per i nodi vincolati
        _F = _R * F

        # solve the equation [K] x {d} = {F} for {d}
        D = np.linalg.solve(Kr, _F)
        return D

    def reactions(self) -> np.ndarray:
        """Solves the frame"""
        # [A] = [K] x {d} - {F}

        # calculate the global stiffness matrix, restraints vector, and loads vector
        K = self.global_stiffness_matrix()
        F = self.loads()
        D = self.displacemets()

        # [A] è il vettore colonna che contiene le reazioni vincolari
        A = K @ D - F
        return A

    def generate_node_report(self):
        A = self.reactions()
        D = self.displacemets()
        L = self.loads()

        restraints_ = (
            lambda x, y, r: f"[{'X' if x else '-'} {'X' if y else '-'} {'X' if r else '-'}]"
        )

        X = np.empty((len(self.nodes), 12), dtype=object)

        X[:, 0] = [f"n{node.id}" for node in self.nodes]
        X[:, 1] = [str(node.coordinates) for node in self.nodes]
        X[:, 2] = [restraints_(*node.restraints) for node in self.nodes]
        X[:, 3] = [f"{(float(A[i]))/1000:.1f} kN" for i in range(0, len(A), 3)]
        X[:, 4] = [f"{(float(A[i]))/1000:.1f} kN" for i in range(1, len(A), 3)]
        X[:, 5] = [f"{(float(A[i]))/1000000:.2f} kNm" for i in range(2, len(A), 3)]
        X[:, 6] = [f"{(float(L[i]))/1000:.1f} kN" for i in range(0, len(L), 3)]
        X[:, 7] = [f"{(float(L[i]))/1000:.1f} kN" for i in range(1, len(L), 3)]
        X[:, 8] = [f"{(float(L[i]))/1000000:.2f} kNm" for i in range(2, len(L), 3)]
        X[:, 9] = [f"{float(D[i]):.1f} mm" for i in range(0, len(D), 3)]
        X[:, 10] = [f"{float(D[i]):.1f} mm" for i in range(1, len(D), 3)]
        X[:, 11] = [f"{float(D[i]):.5f} rad" for i in range(2, len(D), 3)]

        note = """
Note:
    kN = kiloNewton, kNm = kiloNewton meter, mm = millimeter, rad = radian

    RESTRAINTS:
    an X indicates a restrained degree of freedom, a - indicates a free degree of freedom
    a node can be restrained in the horizontal, vertical, and rotational directions
    ordererd as [X X X].
    example: 
    [X X -] is a hinge
    [- - -] is a free node
    [- X -] is a vertical support (horizontal roller)
    [X X X] is a fixed support
    [- - X] is guided support without rotation


    REACTIONS:
    - Hr = Horizontal reaction, 
    - Vr = Vertical reaction, 
    - Mr = Moment reaction

    ACTIONS:
    - Ha = Horizontal action, 
    - Va = Vertical action, 
    - Ma = Moment action

    DISPLACEMENTS:
    - dx = Displacement in the horizontal direction, 
    - dy = Displacement in the vertical direction
    - rz = Rotation around the z-axis
        """

        table = PrettyTable()
        table.field_names = [
            "Node",
            "Coordinates",
            "Restraints",
            "Hr",
            "Vr",
            "Mr",
            "Ha",
            "Va",
            "Ma",
            "dx",
            "dy",
            "rz",
        ]
        table.add_rows(X.tolist())

        return note + "\n" + table.get_string()
