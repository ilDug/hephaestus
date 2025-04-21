import yaml
from pydantic import BaseModel


class InputNode(BaseModel):
    id: str
    coordinates: list[int]  # [x, y]
    restraints: list[bool] = [False, False, False]  # Rx, Ry, Rz
    loads: list[float] = [0, 0, 0]  # Fx, Fy, Mz


class InputBeam(BaseModel):
    id: str
    nodes: list[str]  # [node1, node2]
    material: str
    section: str
    releases: list[bool] = [False, False]  # i, j
    side: str = "MAJOR"  # MINOR, MAJOR
    loads: list[float] = [0, 0]  # qx, qy


class InputFrame(BaseModel):
    """
    Input file for the model.
    """

    materials: list[str]
    sections: list[str]
    nodes: list[InputNode]
    beams: list[InputBeam]
