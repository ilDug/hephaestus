from core.objects import Node, Beam, Frame
import numpy as np
from fractions import Fraction

# proprietà della trave: materiale e sezione
E = 210000
Ix = 3492000  # mm4 HEA100
A = 2124  # mm2 HEA100

# creo una struttura
frame = Frame()

n1 = frame.add_node((0, 0))
n2 = frame.add_node((0, 1000))
n3 = frame.add_node((500, 1000))
n4 = frame.add_node((1000, 1000))

b1 = frame.add_beam(n2, n1)
b2 = frame.add_beam(n2, n3)
b3 = frame.add_beam(n4, n3)

for beam in frame.beams:
    beam.set_material(E).set_section(A, Ix, Ix)


frame.node(n1).set_restraints(True, True, True)
frame.node(n4).set_restraints(True, True, True)

frame.node(n3).apply_loads(Fy=-100)


print(frame.generate_node_report())
