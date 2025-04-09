from core.elements import Frame
from core.materials import select_material
from core.sections import select_section


# creo una struttura
frame = Frame()

m1 = select_material("S235")
s1 = select_section("HEA100")

n1 = frame.add_node((0, 0))
n2 = frame.add_node((500, 0))
n3 = frame.add_node((1000, 0))

b1 = (
    frame.add_beam(n1, n2)
    .set_material(m1)
    .set_section(s1)
    .set_side("MINOR")
    .set_internal_releases(i=True)
)
b2 = frame.add_beam(n2, n3).set_material(m1).set_section(s1)


frame.node(n1).set_restraints(True, True, True)
frame.node(n3).set_restraints(True, True, True)


frame.node(n2).apply_loads(Fy=-100)


print(frame.generate_node_report())


# for s in secs:
#     print(s.model_dump_json())
