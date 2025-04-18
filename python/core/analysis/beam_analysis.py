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
    """forces vector of node j"""

    def __init__(self, solutions: FrameSolution):
        self.sol = solutions

    def for_beam(self, beam: Beam) -> "BeamAnalysis":
        """
        Returns the solution for a given beam.
        """
        self.beam = beam

        # ritrova gli index dei nodi
        i = beam.i.id - 1
        j = beam.j.id - 1

        # ritrova gl ispostamenti dei nodi
        self.di = self.sol.D[i]
        self.dj = self.sol.D[j]

        # calcola le forze sui nodi della trave
        f = self.beam.nodal_strengths(self.di, self.dj)
        self.fi = f[:3]
        self.fj = f[3:]

        # print(f"fi: {self.fi}")
        # print(f"fj: {self.fj}")

        return self

    def fx(self, x: int):
        """
        Returns the axial force, the shear and the bending moment at a given point x along the beam.
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

        # fn, ft = sum(
        #     [
        #         l.to_local(self.beam.angle())
        #         for l in self.beam.ext_loads
        #         if isinstance(l, PointLoad) and x >= l.x
        #     ],
        #     start=(0, 0),
        # )

        Nx = -Ni - qn * x
        Tx = -Ti - qt * x
        Mx = Ti * x + qt * x**2 / 2 - Mi

        return np.array([Nx, Tx, Mx], dtype=float)

    def maximums(self) -> float:
        """
        Returns the maximum shear force along the beam.
        """

        ascisse = np.linspace(0, self.beam.L, int(self.beam.L + 1), dtype=int)
        strengths = np.array([self.fx(x) for x in ascisse])

        axial = strengths[:, 0].flatten()
        shear = strengths[:, 1].flatten()
        moment = strengths[:, 2].flatten()

        # max_axial = np.max(axial)
        # min_axial = np.min(axial)
        axial_abs_max = np.max(np.abs(axial))

        # max_shear = np.max(shear)
        # min_shear = np.min(shear)
        shear_abs_max = np.max(np.abs(shear))

        # max_moment = np.max(moment)
        # min_moment = np.min(moment)
        moment_abs_max = np.max(np.abs(moment))

        x_Amax = int(np.argmax(axial))

        x_Tmax = int(np.argmax(shear))

        x_Mmax = int(np.argmax(moment))

        return np.array(
            [
                [x_Amax, axial_abs_max],
                [x_Tmax, shear_abs_max],
                [x_Mmax, moment_abs_max],
            ],
            dtype=int,
        )  # (x, y) pairs

    def zeros(self):
        """
        Returns the zeros of the beam.
        """
        ascisse = np.linspace(0, self.beam.L, int(self.beam.L + 1), dtype=int)
        strengths = np.array([self.fx(x) for x in ascisse])

        axial = strengths[:, 0]
        shear = strengths[:, 1]
        moment = strengths[:, 2]

        shear_zeros = []
        axial_zeros = []
        moment_zeros = []

        for i in range(len(ascisse) - 1):  # loop through the shear array
            if shear[i] * shear[i + 1] < 0:  # check if the sign changes
                x0, x1 = ascisse[i], ascisse[i + 1]
                y0, y1 = shear[i], shear[i + 1]
                # Interpolazione lineare per trovare lo zero
                x_zero = x0 - y0 * (x1 - x0) / (y1 - y0)
                shear_zeros.append(int(x_zero))

            # check if the sign changes
            if axial[i] * axial[i + 1] < 0:
                x0, x1 = ascisse[i], ascisse[i + 1]
                y0, y1 = axial[i], axial[i + 1]
                # Interpolazione lineare per trovare lo zero
                x_zero = x0 - y0 * (x1 - x0) / (y1 - y0)
                axial_zeros.append(int(x_zero))

            if moment[i] * moment[i + 1] < 0:
                x0, x1 = ascisse[i], ascisse[i + 1]
                y0, y1 = moment[i], moment[i + 1]
                # Interpolazione lineare per trovare lo zero
                x_zero = x0 - y0 * (x1 - x0) / (y1 - y0)
                moment_zeros.append(int(x_zero))

        return axial_zeros, shear_zeros, moment_zeros  # shape

    def Axial(self):
        """
        Returns the axial force diagram along the beam.
        """
        ascisse = np.linspace(0, self.beam.L, int(self.beam.L + 1), dtype=int)
        strengths = np.array([self.fx(x) for x in ascisse])

        axial = strengths[:, 0]
        diagram = np.zeros((len(ascisse), 2), dtype=int)
        diagram[:, 0] = ascisse
        diagram[:, 1] = axial
        return diagram

    def Shear(self):
        """
        Returns the shear force diagram along the beam.
        """
        ascisse = np.linspace(0, self.beam.L, int(self.beam.L + 1), dtype=int)
        strengths = np.array([self.fx(x) for x in ascisse])

        shear = strengths[:, 1]
        diagram = np.zeros((len(ascisse), 2), dtype=int)
        diagram[:, 0] = ascisse
        diagram[:, 1] = shear
        return diagram

    def Momentum(self):
        """
        Returns the bending moment diagram along the beam.
        """
        ascisse = np.linspace(0, self.beam.L, int(self.beam.L + 1), dtype=int)
        strengths = np.array([self.fx(x) for x in ascisse])

        moment = strengths[:, 2]
        diagram = np.zeros((len(ascisse), 2), dtype=int)
        diagram[:, 0] = ascisse
        diagram[:, 1] = moment
        return diagram
