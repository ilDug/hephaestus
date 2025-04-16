from core.elements import Frame
from core.materials import select_material
from core.sections import select_section
from core.report import *

# creo una struttura
frame = Frame()

m1 = select_material("S235")
s1 = select_section("HEA100")

n1 = frame.add_node((0, 0))
n2 = frame.add_node((1000, 0))
# n3 = frame.add_node((1000, 0))
# n2 = frame.add_node((500, 0))
# n3 = frame.add_node((1000, 0))

b1 = (
    frame.add_beam(n1, n2)
    .set_material(m1)
    .set_section(s1)
    .set_internal_releases(i=True, j=True)
    # .set_side("MINOR")
)
# b2 = (
#     frame.add_beam(n2, n3)
#     .set_material(m1)
#     .set_section(s1)
#     # .set_internal_releases(j=True)
# )


frame.node(n1).set_restraints(True, True, True)
frame.node(n2).set_restraints(True, True, True)


# frame.node(n2).apply_loads(Fy=-1)
# frame.node(n2).apply_loads(Mz=1)

# b1.apply_distributed_load(qx=0, qy=-10)
# b2.apply_distributed_load(qx=0, qy=-10)
# b1.apply_point_load(fy=-1, x=300)
b1.apply_momentum_load(x=300, M=1)


sol = frame.solve()

# print(report_header())
print(report_node_table(sol))
print(report_beam_table(sol))

# for s in secs:
#     print(s.model_dump_json())
