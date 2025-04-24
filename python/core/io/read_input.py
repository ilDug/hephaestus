from ..elements import Frame
from .input_models import InputFrame
import json

def parse_input_frame(source: dict) -> Frame:
    """
    Parse the input frame data from a dictionary and create a Frame object.
    """
    
    # Create an instance of InputFrame using the loaded data
    input_frame = InputFrame(**source)

    # Create a Frame object
    frame = Frame()

    # Create nodes
    for node in input_frame.nodes:
        n = frame.add_node(tuple(node.coordinates), tag=node.tag)
        frame.node(n).set_restraints(*node.restraints)
        frame.node(n).apply_loads(*node.loads)

    # Create beams
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

    return frame