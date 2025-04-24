from core.elements import Frame
from core.materials import select_material
from core.sections import select_section
from core.analysis import *


# creo una struttura
frame = Frame()

m1 = select_material("S235")
s1 = select_section("HEA100")

n1 = frame.add_node((0, 0))
n2 = frame.add_node((500, 0))
n3 = frame.add_node((1000, 0))
# n2 = frame.add_node((500, 0))
# n3 = frame.add_node((1000, 0))

b1 = (
    frame.add_beam(n1, n2)
    .set_material("S235")
    .set_section("HEA100")
    # .set_internal_releases(i=True, j=True)
    # .set_side("MINOR")
)
b2 = (
    frame.add_beam(n2, n3)
    .set_material("S235")
    .set_section("HEA100")
    # .set_internal_releases(j=True)
)


frame.node(n1).set_restraints(True, True, True)
frame.node(n3).set_restraints(True, True, True)

frame.node(n2).apply_loads(Fy=-10)

# frame.node(n2).apply_loads(Fy=-0.7, Fx=-0.7)
# frame.node(n2).apply_loads(Mz=1)

b1.apply_distributed_load(qx=0, qy=-10)
b1.apply_distributed_load(qx=0, qy=-10)
# b1.apply_distributed_load(qx=1, qy=2)
# b1.apply_point_load(fy=-0.707, fx=0.707, x=300)
# b1.apply_momentum_load(x=300, M=1)

b2.apply_distributed_load(qx=0, qy=-10)
# b2.apply_point_load(fy=-1, x=400)
# b2.apply_momentum_load(x=300, M=1)


out = frame.save_solution("simple.txt")
print(out)


# sol: FrameSolution = frame.solve()


# a1 = BeamAnalysis(sol).for_beam(b1)
# print(a1.fx(0))
# print(a1.fx(272.73))
# print(a1.zeros())
# print(a1.maximums())
# print(a1.Momentum())


# a2 = BeamAnalysis(sol).for_beam(b2)
# # print(a2.fx(0))
# # print(a2.fx(500))
# print(a2.zeros())
# print(a2.maximums())


# Plot momentum diagram for b1
# m_diagram_b1 = a1.Momentum() * [1, 1 / 1000000]
# print(m_diagram_b1.round(2).tolist())


# plt.figure(figsize=(10, 6))
# plt.plot(m_diagram_b1[:, 0], m_diagram_b1[:, 1], label="Beam b1 Momentum", color="blue")
# plt.fill_between(m_diagram_b1[:, 0], m_diagram_b1[:, 1], color="blue", alpha=0.2)

# # # Plot momentum diagram for b2
# # x_b2 = [i for i in range(0, int(b2.length()) + 1)]
# # momentum_b2 = [a2.Momentum(x) for x in x_b2]

# # plt.plot(
# #     [x + b1.length() for x in x_b2],
# #     momentum_b2,
# #     label="Beam b2 Momentum",
# #     color="green",
# # )
# # plt.fill_between([x + b1.length() for x in x_b2], momentum_b2, color="green", alpha=0.2)

# # Add labels and legend
# plt.title("Momentum Diagram")
# plt.xlabel("Length (mm)")
# plt.ylabel("Momentum (kNm)")
# plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
# plt.legend()
# plt.grid(True)
# plt.show()
