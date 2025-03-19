from core.objects import Node, Beam
import numpy as np
from fractions import Fraction


E = 210000
Ix = 1000
A = 320

n1 = Node(1, (0, 0))
n1.set_restraints(True, True, True)

n2 = Node(2, (750, 1500))
n2.apply_loads(Fy=-10)

b1 = Beam(n1, n2)
b1.set_material(E).set_section(A, Ix, Ix)

angle_pi_format = f"{b1.rotation_angle() / np.pi:.2f}π"
angle_fraction_format = f"{Fraction(b1.rotation_angle() / np.pi).limit_denominator()}π"

print(f"Rotation angle in π format: {angle_pi_format}")
print(f"Rotation angle in π format: {angle_fraction_format}")

np.set_printoptions(precision=0, floatmode="fixed", suppress=True)
print("Stiffness matrix:")
print(b1.stiffness_matrix())

np.set_printoptions(precision=3, floatmode="fixed", suppress=True)
print("Rotation matrix:")
print(b1.rotation_matrix())


# #############################################################################


external_load_matrix = np.concatenate((n1.load_vector(), n2.load_vector()))
# transpose the matrix to get the loads in column format
# external_load_matrix = np.transpose(external_load_matrix)
print("External load matrix:")

print(external_load_matrix)
# dimnsione della matrice di carico esterno
print(f"Dimensione matrice carico esterno: {external_load_matrix.shape}")
