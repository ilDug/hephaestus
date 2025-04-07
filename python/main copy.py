from core.elements import Node, Beam, Frame
import numpy as np
from fractions import Fraction

# proprietà della trave: materiale e sezione
E = 210000
Ix = 3492000  # mm4 HEA100
A = 2124  # mm2 HEA100

# creo una struttura
frame = Frame()

n1 = frame.add_node((0, 0))
n2 = frame.add_node((500, 0))
n3 = frame.add_node((1000, 0))


b1 = frame.add_beam(i=n1, j=n2)
b2 = frame.add_beam(i=n2, j=n3)

for beam in frame.beams:
    beam.set_material(E).set_section(A, Ix, Ix)


frame.node(n1).set_restraints(True, True, True)
frame.node(n3).set_restraints(False, True, False)


frame.node(n2).apply_loads(Fy=-1)


# for node in frame.nodes:
#     print("the node is:")
#     print(node.id, node.coordinates, node.restraints)

np.set_printoptions(precision=3, suppress=True)

for beam in frame.beams:
    print(beam.id, beam.L, beam.E, beam.A, beam.Ix, beam.Iy)
    angle_pi_format = f"{b1.rotation_angle() / np.pi:.2f}π"
    angle_fraction_format = (
        f"{Fraction(b1.rotation_angle() / np.pi).limit_denominator()}π"
    )
    print(f"Rotation angle in π format: {angle_pi_format}")
    print(f"Rotation angle in π  fractional format: {angle_fraction_format}")
    print(f"Stiffness matrix for beams `{beam.id}`:")
    print(beam.stiffness_matrix())

# #############################################################################


print("Frame restraints:")
print(frame.restraints())

print("Frame loads:")
print(frame.loads())

np.set_printoptions(precision=0, suppress=True)
print(f"Global stiffness matrix, with size: {frame.global_stiffness_matrix().shape}")
global_stiffness_matrix = frame.global_stiffness_matrix()
print(global_stiffness_matrix)


np.set_printoptions(precision=5, suppress=True)
print("displacements:")
print(frame.displacemets())

np.set_printoptions(precision=0, suppress=True)

print("Reazioni vincolari:")
print(frame.reactions().round(1))

print(frame.generate_node_report())
