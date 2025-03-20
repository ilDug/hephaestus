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
n2 = frame.add_node((1500, 0))

b1 = frame.add_beam(1, 2)
b1.set_material(E).set_section(A, Ix, Ix)

frame.node(n1).set_restraints(True, True, True)
frame.node(n2).apply_loads(Fy=-1)

for node in frame.nodes:
    print("the node is:")
    print(node.id, node.coordinates, node.restraints)

for beam in frame.beams:
    print(beam.id, beam.L, beam.E, beam.A, beam.Ix, beam.Iy)
    angle_pi_format = f"{b1.rotation_angle() / np.pi:.2f}π"
    angle_fraction_format = (
        f"{Fraction(b1.rotation_angle() / np.pi).limit_denominator()}π"
    )
    print(f"Rotation angle in π format: {angle_pi_format}")
    print(f"Rotation angle in π  fractional format: {angle_fraction_format}")


# #############################################################################


np.set_printoptions(precision=3, floatmode="fixed", suppress=True)
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

np.set_printoptions(precision=5, floatmode="fixed", suppress=True)
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
