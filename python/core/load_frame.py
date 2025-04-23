import yaml
from pydantic import BaseModel


class InputNode(BaseModel):
    tag: str
    """identificativo del nodo"""
    coordinates: list[int]  # [x, y]
    """coordinate del nodo"""
    restraints: list[bool] = [False, False, False]  # Rx, Ry, Rz
    """vincoli del nodo"""
    loads: list[float] = [0, 0, 0]  # Fx, Fy, Mz
    """carichi sterni applicati al nodo"""  # [Fx, Fy, Mz]


class InputBeam(BaseModel):
    nodes: list[str]  # [node1, node2]
    """tags dei nodi della trave"""
    material: str
    """materiale della trave"""
    section: str
    """sezione della trave"""
    releases: list[bool] = [False, False]  # i, j
    """rilascio interno della trave"""
    side: str = "MAJOR"  # MINOR, MAJOR
    """lato della sezione su cui si applica il carico"""
    loads: list[float] = [0, 0]  # qx, qy
    """carichi distribuiti applicati alla trave"""  # [qx, qy]


class InputFrame(BaseModel):
    """
    Input file for the model.
    """
    nodes: list[InputNode]
    beams: list[InputBeam]
