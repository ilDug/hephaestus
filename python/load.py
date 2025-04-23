from core.elements import Frame
from core.materials import select_material
from core.sections import select_section
from core.analysis import *
from core.load_frame import InputFrame
import json

# creo una struttura
frame = Frame()

# Import YAML library to read the file

# Load the YAML file
with open("load.json", "r") as file:
    load_data = json.load(file)

# Create an instance of InputFrame using the loaded data
input_frame = InputFrame(**load_data)


# crea i nodi
for node in input_frame.nodes:
    n = frame.add_node(tuple(node.coordinates), tag=node.tag)
    frame.node(n).set_restraints(*node.restraints)
    frame.node(n).apply_loads(*node.loads)

# crea le travi
for beam in input_frame.beams:
    i = frame.node(beam.nodes[0])
    j = frame.node(beam.nodes[1])

    b = (
        frame.add_beam(i.tag, j.tag)
        .set_material(beam.material)
        .set_section(beam.section)
        .set_internal_releases(beam.releases)
        .set_side(beam.side)
        .apply_distributed_load(beam.loads[0], beam.loads[1])
    )

# print(input_frame)
frame.save_solution("load.txt")
