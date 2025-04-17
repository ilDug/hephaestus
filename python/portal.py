from core.elements import Frame
from core.materials import select_material
from core.sections import select_section
from core.report import *

# creo una struttura
frame = Frame()

m1 = select_material("S235")
s1 = select_section("IPE100")

n1 = frame.add_node((0, 0))
n2 = frame.add_node((0, 1000))
n3 = frame.add_node((1000, 1000))
n4 = frame.add_node((1500, 1000))
n5 = frame.add_node((2000, 1000))
n6 = frame.add_node((0, 500))

b1 = frame.add_beam(n1, n6)
b2 = frame.add_beam(n2, n3)
b3 = frame.add_beam(n3, n4)
b4 = frame.add_beam(n4, n5)
b5 = frame.add_beam(n3, n6)
b6 = frame.add_beam(n6, n2)

for b in frame.beams:
    b.set_material(m1).set_section(s1)

frame.node(n1).set_restraints(True, True, True)
frame.node(n5).set_restraints(True, True, True)
frame.node(n2).set_restraints(x=True)

frame.node(n4).apply_loads(Fy=-2)
# frame.node(n2).apply_loads(Mz=1)

# b1.apply_distributed_load(qx=0, qy=-10)
# b2.apply_distributed_load(qx=0, qy=-10)
# b1.apply_point_load(fy=-1, x=300)
# b1.apply_momentum_load(x=300, M=1)
# b4.apply_momentum_load(x=100, M=1)


sol = frame.solve()

print(report_node_table(sol))
print(report_node_reactions(sol))
print(report_beam_table(sol))
print(report_beam_actions(sol))
