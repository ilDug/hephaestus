from core.objects import Node, Beam
import numpy as np

np.set_printoptions(precision=0, floatmode="fixed", suppress=True)

E = 210000
Ix = 1000
A = 320

n1 = Node(1, (0, 0))
n2 = Node(2, (0, 1500))

b1 = Beam(n1, n2)
b1.set_material(E).set_section(A, Ix, Ix)
print(b1.stiffness_matrix())
