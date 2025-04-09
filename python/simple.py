from core.elements import Frame
from core.materials import S235
from core.sections.section_db import secs

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


for s in secs:
    print(s.model_dump_json())
