from core.objects import Node, Beam
import numpy as np
from fractions import Fraction


E = 210000
Ix = 3492000  # mm4 HEA100
A = 2124  # mm2 HEA100

n1 = Node(1, (10, 10))
n1.set_restraints(1, 1, 1)

n2 = Node(2, (15, 0))
n2.apply_loads(Fy=-1)

b1 = Beam(n1, n2)
b1.set_material(E).set_section(A, Ix, Ix)

angle_pi_format = f"{b1.rotation_angle() / np.pi:.2f}π"
angle_fraction_format = f"{Fraction(b1.rotation_angle() / np.pi).limit_denominator()}π"

print(f"Rotation angle in π format: {angle_pi_format}")
print(f"Rotation angle in π format: {angle_fraction_format}")

np.set_printoptions(precision=0, floatmode="fixed", suppress=True)
print("Stiffness matrix:")
print(b1.stiffness_matrix())


frame_restraints = (
    np.concatenate([n1.restraints, n2.restraints]).astype(int).reshape(-1, 1)
)
print("Frame restraints:")
print(frame_restraints)

global_stiffness_matrix = b1.stiffness_matrix()
global_stiffness_matrix_aux = global_stiffness_matrix.copy()

# apply restraints
#  setting the rows and columns of the restraints to zero
for i, r in enumerate(frame_restraints):
    if r == 1:
        global_stiffness_matrix_aux[i, :] = 0
        global_stiffness_matrix_aux[:, i] = 0
        global_stiffness_matrix_aux[i, i] = 1


print("Global stiffness matrix aux:")
print(global_stiffness_matrix_aux)
det = np.linalg.det(global_stiffness_matrix_aux)
print(f"Determinant: {det}")
print(f"Dimensione matrice di rigidezza: {global_stiffness_matrix.shape}")

np.set_printoptions(precision=3, floatmode="fixed", suppress=True)
global_stiffness_matrix_inv = np.linalg.inv(global_stiffness_matrix_aux)
print("Inverse global stiffness matrix:")
print(global_stiffness_matrix_inv)


# #############################################################################


external_load_matrix = np.concatenate([n1.load_vector(), n2.load_vector()]).reshape(
    -1, 1
)

# transpose the matrix to get the loads in column format
# external_load_matrix = np.transpose(external_load_matrix)
print("External load matrix:")

print(external_load_matrix)
# dimnsione della matrice di carico esterno
print(f"Dimensione matrice carico esterno: {external_load_matrix.shape}")


# [K] x {d} = {F}
# {d} = [K]^-1 x {F}
displacements_matrix = np.dot(global_stiffness_matrix_aux, external_load_matrix)
print("Displacements matrix:")
print(displacements_matrix)


# [R] = [K] x {d} - {F}
# reactions = np.dot(global_stiffness_matrix, displacements_matrix) - external_load_matrix
kd = np.dot(global_stiffness_matrix, displacements_matrix)
print("Kd:")
print(kd)
reactions = kd - external_load_matrix

print("Reactions:")
print(reactions)

# #############################################################################
