import numpy as np

from ..loads import DistributedLoad, PointLoad, MomentumLoad
from .solution import FrameSolution

from core.elements import Beam


class BeamAnalysis:
    """
    A class to analyze the beam data.
    """

    di = np.zeros((1, 3))
    """diaplacement vector of node i"""
    dj = np.zeros((1, 3))
    """diaplacement vector of node j"""
    fi = np.zeros((1, 3))
    """forces vector of node i"""
    fj = np.zeros((1, 3))

    def __init__(self, solutions: FrameSolution):
        self.sol = solutions

    def for_beam(self, beam: Beam) -> "BeamAnalysis":
        """
        Returns the solution for a given beam.
        """
        self.beam = beam
        self.element_displacements()
        self.element_strengths()
        print(self.fx(0))
        print(self.fx(500))
        print(self.fx(1000))

        return self

    def element_displacements(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Returns the displacements for the beam.
        """
        i = self.beam.i.id - 1
        j = self.beam.j.id - 1

        self.di = self.sol.D[i]
        self.dj = self.sol.D[j]
        return self.di, self.dj

    def element_strengths(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Returns the forces on the nodes of the beam.
        """
        f = self.beam.nodal_strengths(self.di, self.dj)
        self.fi = f[:3]
        self.fj = f[3:]
        return self.fi, self.fj

    def fx(self, x: int):
        """
        Returns the axial force at a given point x along the beam.
        """
        if x < 0 or x > self.beam.L:
            raise ValueError("x must be between 0 and the length of the beam")

        Ni, Ti, Mi = self.fi
        # Nj, Tj, Mj = self.fj

        qn, qt = sum(
            [
                l.to_local(self.beam.angle())
                for l in self.beam.ext_loads
                if isinstance(l, DistributedLoad)
            ],
            start=(0, 0),
        )

        fn, ft = sum(
            [
                l.to_local(self.beam.angle())
                for l in self.beam.ext_loads
                if isinstance(l, PointLoad) and x >= l.x
            ],
            start=(0, 0),
        )


        Nx = Ni + qn * x + fn
        Tx = Ti + qt * x + ft
        Mx = Mi + qt * x**2 / 2 + ft * x

        return np.array([Nx, Tx, Mx])