import numpy as np


def generate_stiffness_matrix_2d(
    E: int, A: int, I: int, L: float, ri: bool = True, rj: bool = False
) -> np.ndarray:
    """
    Generates the stiffness matrix for a beam element based on its material
    and geometric properties.
    Parameters:
        E (int): Young's modulus of the material (elastic modulus) in MPa.
        A (int): Cross-sectional area of the beam in mm2.
        I (int): Moment of inertia of the beam's cross-section in mm4.
        L (float): Length of the beam in mm.
        ri (bool): Indicates if the initial node is released (default: False).
        rj (bool): Indicates if the final node is released (default: False).
    Returns:
        numpy.ndarray: A 6x6 stiffness matrix representing the beam's
        stiffness in local coordinates.
    Raises:
        ValueError: If any of the input parameters (E, A, I, L) are None.
    Notes:
        The stiffness matrix is calculated based on the beam's axial,
        shear, and bending properties. The matrix is symmetric and
        represents the relationship between forces/moments and
        displacements/rotations at the beam's two ends.
    Symbols:
        i: Initial node of the beam.
        j: Final node of the beam.
        Kn: Axial stiffness.
        Kt: Shear stiffness.
        Km: Bending stiffness.
        u: Displacement in the axial direction.
        v: Displacement in the transverse direction.
        r: Rotation.
    """

    if None in [E, A, I, L]:
        raise ValueError("Some properties of the beam are not set")

    # reazioni assiali sul nodo i
    Kniui = E * A / L  # dovuto alllo spostamento assiale del nodo i
    Knivi = 0
    Kniri = 0
    Kniuj = -E * A / L  # dovuto allo spostamento assiale del nodo j
    Knivj = 0
    Knirj = 0

    # ##########################################################################
    match (ri, rj):
        case (False, False):
            # reazioni trasversali sul nodo i
            Ktiui = 0
            Ktivi = 12 * E * I / L**3  # dovuto alla traslazione trasversale del nodo i
            Ktiri = 6 * E * I / L**2  # dovuto alla rotazione del nodo i
            Ktiuj = 0
            Ktivj = -12 * E * I / L**3  # dovuto alla traslazione trasversale del nodo j
            Ktirj = 6 * E * I / L**2  # dovuto alla rotazione del nodo j
        case (True, True):
            # reazioni trasversali sul nodo i
            Ktiui = 0
            Ktivi = 0  # dovuto alla traslazione trasversale del nodo i
            Ktiri = 0  # dovuto alla rotazione del nodo i
            Ktiuj = 0
            Ktivj = 0  # dovuto alla traslazione trasversale del nodo j
            Ktirj = 0  # dovuto alla rotazione del nodo j
        case (True, False):
            # reazioni trasversali sul nodo i
            Ktiui = 0
            Ktivi = 3 * E * I / L**3  # dovuto alla traslazione trasversale del nodo i
            Ktiri = 0  # dovuto alla rotazione del nodo i
            Ktiuj = 0
            Ktivj = -3 * E * I / L**3  # dovuto alla traslazione trasversale del nodo j
            Ktirj = 3 * E * I / L**2  # dovuto alla rotazione del nodo j
        case (False, True):
            # reazioni trasversali sul nodo i
            Ktiui = 0
            Ktivi = 3 * E * I / L**3  # dovuto alla traslazione trasversale del nodo i
            Ktiri = 3 * E * I / L**2  # dovuto alla rotazione del nodo i
            Ktiuj = 0
            Ktivj = -3 * E * I / L**3  # dovuto alla traslazione trasversale del nodo j
            Ktirj = 0  # dovuto alla rotazione del nodo j

    # ##########################################################################
    match (ri, rj):
        case (False, False):
            # momenti flettenti sul nodo i
            Kmiui = 0
            Kmivi = 6 * E * I / L**2  # dovuto alla traslazione trasversale del nodo i
            Kmiri = 4 * E * I / L  # dovuto alla rotazione del nodo i
            Kmiuj = 0
            Kmivj = -6 * E * I / L**2  # dovuto alla traslazione trasversale del nodo j
            Kmirj = 2 * E * I / L  # dovuto alla rotazione del nodo j
        case (True, True):
            # momenti flettenti sul nodo i
            Kmiui = 0
            Kmivi = 0  # dovuto alla traslazione trasversale del nodo i
            Kmiri = 0  # dovuto alla rotazione del nodo i
            Kmiuj = 0
            Kmivj = 0  # dovuto alla traslazione trasversale del nodo j
            Kmirj = 0  # dovuto alla rotazione del nodo j
        case (True, False):
            # momenti flettenti sul nodo i
            Kmiui = 0
            Kmivi = 0  # dovuto alla traslazione trasversale del nodo i
            Kmiri = 0  # dovuto alla rotazione del nodo i
            Kmiuj = 0
            Kmivj = 0  # dovuto alla traslazione trasversale del nodo j
            Kmirj = 0  # dovuto alla rotazione del nodo j
        case (False, True):
            # momenti flettenti sul nodo i
            Kmiui = 0
            Kmivi = 3 * E * I / L**2  # dovuto alla traslazione trasversale del nodo i
            Kmiri = 3 * E * I / L  # dovuto alla rotazione del nodo i
            Kmiuj = 0
            Kmivj = -3 * E * I / L**2  # dovuto alla traslazione trasversale del nodo j
            Kmirj = 0  # dovuto alla rotazione del nodo j

    # ##########################################################################
    # reazioni assiali sul nodo j
    Knjui = -E * A / L  # dovuto allo spostamento assiale del nodo i
    Knjvi = 0
    Knjri = 0
    Knjuj = E * A / L  # dovuto allo spostamento assiale del nodo j
    Knjvj = 0
    Knjrj = 0

    # ##########################################################################
    match (ri, rj):
        case (False, False):
            # reazioni trasversali sul nodo j
            Ktjui = 0
            Ktjvi = -12 * E * I / L**3  # dovuto alla traslazione trasversale del nodo i
            Ktjri = -6 * E * I / L**2  # dovuto alla rotazione del nodo i
            Ktjuj = 0
            Ktjvj = 12 * E * I / L**3  # dovuto alla traslazione trasversale del nodo j
            Ktjrj = -6 * E * I / L**2  # dovuto alla rotazione del nodo j
        case (True, True):
            # reazioni trasversali sul nodo j
            Ktjui = 0
            Ktjvi = 0  # dovuto alla traslazione trasversale del nodo i
            Ktjri = 0  # dovuto alla rotazione del nodo i
            Ktjuj = 0
            Ktjvj = 0  # dovuto alla traslazione trasversale del nodo j
            Ktjrj = 0  # dovuto alla rotazione del nodo j
        case (True, False):
            # reazioni trasversali sul nodo j
            Ktjui = 0
            Ktjvi = -3 * E * I / L**3  # dovuto alla traslazione trasversale del nodo i
            Ktjri = 0  # dovuto alla rotazione del nodo i
            Ktjuj = 0
            Ktjvj = 3 * E * I / L**3  # dovuto alla traslazione trasversale del nodo j
            Ktjrj = -3 * E * I / L**2  # dovuto alla rotazione del nodo j
        case (False, True):
            # reazioni trasversali sul nodo j
            Ktjui = 0
            Ktjvi = -3 * E * I / L**3  # dovuto alla traslazione trasversale del nodo i
            Ktjri = -3 * E * I / L**2  # dovuto alla rotazione del nodo i
            Ktjuj = 0
            Ktjvj = 3 * E * I / L**3  # dovuto alla traslazione trasversale del nodo j
            Ktjrj = 0  # dovuto alla rotazione del nodo j

    # ##########################################################################
    match (ri, rj):
        case (False, False):
            # momenti flettenti sul nodo j
            Kmjui = 0
            Kmjvi = 6 * E * I / L**2  # dovuto alla traslazione trasversale del nodo i
            Kmjri = 2 * E * I / L  # dovuto alla rotazione del nodo i
            Kmjuj = 0
            Kmjvj = -6 * E * I / L**2  # dovuto alla traslazione trasversale del nodo j
            Kmjrj = 4 * E * I / L  # dovuto alla rotazione del nodo j
        case (True, True):
            # momenti flettenti sul nodo j
            Kmjui = 0
            Kmjvi = 0  # dovuto alla traslazione trasversale del nodo i
            Kmjri = 0  # dovuto alla rotazione del nodo i
            Kmjuj = 0
            Kmjvj = 0  # dovuto alla traslazione trasversale del nodo j
            Kmjrj = 0  # dovuto alla rotazione del nodo j
        case (True, False):
            # momenti flettenti sul nodo j
            Kmjui = 0
            Kmjvi = 3 * E * I / L**2  # dovuto alla traslazione trasversale del nodo i
            Kmjri = 0  # dovuto alla rotazione del nodo i
            Kmjuj = 0
            Kmjvj = -3 * E * I / L**2  # dovuto alla traslazione trasversale del nodo j
            Kmjrj = 3 * E * I / L  # dovuto alla rotazione del nodo j
        case (False, True):
            # momenti flettenti sul nodo j
            Kmjui = 0
            Kmjvi = 0  # dovuto alla traslazione trasversale del nodo i
            Kmjri = 0  # dovuto alla rotazione del nodo i
            Kmjuj = 0
            Kmjvj = 0  # dovuto alla traslazione trasversale del nodo j
            Kmjrj = 0  # dovuto alla rotazione del nodo j

    # ##########################################################################

    stiffness_matrix = np.array(
        [
            [Kniui, Knivi, Kniri, Kniuj, Knivj, Knirj],
            [Ktiui, Ktivi, Ktiri, Ktiuj, Ktivj, Ktirj],
            [Kmiui, Kmivi, Kmiri, Kmiuj, Kmivj, Kmirj],
            [Knjui, Knjvi, Knjri, Knjuj, Knjvj, Knjrj],
            [Ktjui, Ktjvi, Ktjri, Ktjuj, Ktjvj, Ktjrj],
            [Kmjui, Kmjvi, Kmjri, Kmjuj, Kmjvj, Kmjrj],
        ],
        dtype=float,
    )

    # arrotodamento a 3 decimali
    stiffness_matrix = np.round(stiffness_matrix, 0)
    np.set_printoptions(precision=1, suppress=True)
    print("stiffness matrix:")
    print(stiffness_matrix)
    return stiffness_matrix

    #     [EA/L,      0,              0,          -EA/L,      0,              0],
    #     [0,         12EI/L**3,      6EI/L**2,   0,          -12EI/L**3,     6EI/L**2],
    #     [0,         6EI/L**2,       4EI/L,      0,          -6EI/L**2,      2EI/L],
    #     [-EA/L,     0,              0,          EA/L,       0,              0],
    #     [0,         -12EI/L**3,     -6EI/L**2,  0,          12EI/L**3,      -6EI/L**2],
    #     [0          6EI/L**2,       2EI/L,      0,          -6EI/L**2,      4EI/L]

    #     [EA/L,      0,              0,          -EA/L,      0,              0],
    #     [0,         12EI/L**3,      6EI/L**2,   0,          -12EI/L**3,     6EI/L**2],
    #     [0,         6EI/L**2,       4EI/L,      0,          -6EI/L**2,      2EI/L],
    #     [-EA/L,     0,              0,          EA/L,       0,              0],
    #     [0,         -12EI/L**3,     -6EI/L**2,  0,          12EI/L**3,      -6EI/L**2],
    #     [0          6EI/L**2,       2EI/L,      0,          -6EI/L**2,      4EI/L]


# #############################################################################


def generate_rotation_matrix_2d(angle: float) -> np.ndarray:
    """
    Generates the rotation matrix for a 2D beam element based on the
    rotation angle.
    Parameters:
        angle (float): The rotation angle in radians.
    Returns:
        numpy.ndarray: A 6x6 rotation matrix representing the beam's
        rotation in local coordinates.
    Notes:
        The rotation matrix is used to transform the stiffness matrix
        from local to global coordinates.
    Symbols:
        theta: Rotation angle.
        c: Cosine of the rotation angle.
        s: Sine of the rotation angle.
    """
    c = np.cos(angle)
    s = np.sin(angle)

    rotation_matrix = np.array(
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

    return rotation_matrix
