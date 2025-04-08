from core.elements import Frame
from core.materials import S235
from core.sections.section_db import HEA_Sections

# proprietà della trave: materiale e sezione

Ix = 3492000  # mm4 HEA100
A = 2124  # mm2 HEA100

# creo una struttura
# frame = Frame()

# n1 = frame.add_node((0, 0))
# n2 = frame.add_node((500, 0))
# n3 = frame.add_node((1000, 0))

# b1 = frame.add_beam(n1, n2)
# b2 = frame.add_beam(n2, n3)


# for beam in frame.beams:
#     beam.set_material(S235()).set_section(A, Ix, Ix)


# frame.node(n1).set_restraints(True, True, True)
# frame.node(n3).set_restraints(True, True, True)

# frame.node(n2).apply_loads(Fy=-100)


# print(frame.generate_node_report()
#
for s in HEA_Sections:
    s.Iy = s.Iy * 1000000
    s.Wely = s.Wely * 1000
    s.Welz = s.Welz * 1000
    s.Wply = s.Wply * 1000
    s.Wplz = s.Wplz * 1000
    s.J = s.J * 1000
    s.Cw = s.Cw * 1000000

    s.Iy = int(s.Iy)
    s.Wely = int(s.Wely)
    s.Welz = int(s.Welz)
    s.Wply = int(s.Wply)
    s.Wplz = int(s.Wplz)
    s.J = int(s.J)
    s.Cw = int(s.Cw)

for s in HEA_Sections:
    print(s.model_dump_json())
