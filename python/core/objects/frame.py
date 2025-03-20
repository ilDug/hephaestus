from .beam import Beam
from .node import Node


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
