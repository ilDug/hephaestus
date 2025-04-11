from dataclasses import dataclass
from core.elements import Node, Beam
import numpy as np


@dataclass
class FrameSolution:
    """Class for storing the solution of the frame analysis."""

    nodes: list[Node]
    """List of nodes in the frame."""
    @property
    def N(self) -> list[Node]:
        """List of nodes in the frame."""
        return self.nodes

    beams: list[Beam]
    """List of beams in the frame."""
    @property
    def B(self) -> list[Beam]:
        """List of beams in the frame."""
        return self.beams


    restraints: np.ndarray
    """Restraints vector for the frame. arranged by node"""
    @property
    def X(self) -> np.ndarray:
        """Restraints vector for the frame. arranged by node"""
        return self.restraints
    
    loads: np.ndarray
    """Loads vector for the frame. arranged by node"""
    @property
    def L(self) -> np.ndarray:
        """Loads vector for the frame. arranged by node"""
        return self.loads
    
    reactions: np.ndarray
    """Reactions vector for the frame. arranged by node"""
    @property
    def R(self) -> np.ndarray:
        """Reactions vector for the frame. arranged by node"""
        return self.reactions
    
    displacements: np.ndarray
    """Displacements vector for the frame. arranged by node"""
    @property
    def D(self) -> np.ndarray:
        """Displacements vector for the frame. arranged by node"""
        return self.displacements
    
        

    def save(self):
        """Saves the solution to a file."""
        pass

    def load(self):
        """Loads the solution from a file."""
        pass
