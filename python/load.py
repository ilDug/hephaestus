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
for input_node in input_frame.nodes:
    n = frame.add_node(tuple(input_node.coordinates))
    frame.node(n).set_restraints(*input_node.restraints)
    frame.node(n).apply_loads(*input_node.loads)

    # cerca nell'input inogni trave se contiene il nome del nodo
    # e se lo contiene lo sostituisce con il nuovo id
    # in modo da non avere conflitti di id
    # for x in range(len(input_frame.beams)):
    #     for y in range(len(input_frame.beams[x].nodes)):
    #         input_frame.beams[x].nodes[y] = (
    #             n
    #             if input_node.id == input_frame.beams[x].nodes[y]
    #             else input_frame.beams[x].nodes[y]
    #         )

# crea le travi
for beam in input_frame.beams:
    label_i = frame.node(beam.nodes[0])
    label_j = frame.node(beam.nodes[1])

    input_beam = (
        frame.add_beam(i.id, j.id)
        .set_material(beam.material)
        .set_section(beam.section)
        .set_internal_releases(beam.releases)
        .set_side(beam.side)
        .apply_distributed_load(beam.loads[0], beam.loads[1])
    )

# print(input_frame)
frame.save_solution("load.txt")
