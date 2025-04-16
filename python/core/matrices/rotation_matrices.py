import numpy as np


class RotationMatrix2D:

    @classmethod
    def x6(cls, angle: float) -> np.ndarray:
        """
        Rotation matrix in 2D space around the z-axis.
        - angle: rotation angle in radians
        - returns: 6x6 rotation matrix
        """
        c = np.cos(angle)
        s = np.sin(angle)

        R = np.array(
            [
                [c, s, 0, 0, 0, 0],
                [-s, c, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0],
                [0, 0, 0, c, s, 0],
                [0, 0, 0, -s, c, 0],
                [0, 0, 0, 0, 0, 1],
            ],
            dtype=float,
        )
        return R

    @classmethod
    def x3(cls, angle: float) -> np.ndarray:
        """
        Rotation matrix in 2D space around the z-axis.
        - angle: rotation angle in radians
        - returns: 3x3 rotation matrix
        """
        c = np.cos(angle)
        s = np.sin(angle)

        R = np.array(
            [
                [c, s, 0],
                [-s, c, 0],
                [0, 0, 1],
            ],
            dtype=float,
        )
        return R

    def x2(cls, angle: float) -> np.ndarray:
        """
        Rotation matrix in 2D space around the z-axis.
        - angle: rotation angle in radians
        - returns: 2x2 rotation matrix
        """
        c = np.cos(angle)
        s = np.sin(angle)

        R = np.array(
            [
                [c, s],
                [-s, c],
            ],
            dtype=float,
        )
        return R
