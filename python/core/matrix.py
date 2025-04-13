import numpy as np


def generate_stiffness_matrix_2d(
    E: int, A: int, I: int, L: float, releases: tuple[bool, bool] = (False, False)
) -> np.ndarray:
    """
    Generates the stiffness matrix for a beam element based on its material
    and geometric properties.
    Parameters:
        E (int): Young's modulus of the material (elastic modulus) in MPa.
        A (int): Cross-sectional area of the beam in mm2.
        I (int): Moment of inertia of the beam's cross-section in mm4.
        L (float): Length of the beam in mm.
        rel_i (bool): Indicates if the initial node is released (default: False).
        rel_j (bool): Indicates if the final node is released (default: False).
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

    match releases:
        case (False, False):
            stiffness_matrix = stiffness_matrix_2d_fixed_fixed_beam(E, A, I, L)
        case (True, False):
            stiffness_matrix = stiffness_matrix_2d_hinged_fixed_beam(E, A, I, L)
        case (False, True):
            stiffness_matrix = stiffness_matrix_2d_fixed_hinged_beam(E, A, I, L)
        case (True, True):
            stiffness_matrix = stiffness_matrix_2d_hinged_hinged_beam(E, A, I, L)

    # arrotodamento a 3 decimali
    # stiffness_matrix = np.round(stiffness_matrix, 3)
    return stiffness_matrix

    # # ##########################################################################

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


def distributed_loads_rotation_matrix_2d(angle: float) -> np.ndarray:
    """
    Genera una matrice di rotazione per ruotare i carichi distribuiti in 2D
    da sistema globale a sistema locale ( e viceversa).
    La matrice di rotazione è una matrice 4x4 che ruota i carichi distribuiti
    lungo la trave.
    """
    s = np.sin(angle)
    c = np.cos(angle)
    R = np.array(
        [
            [c, s, 0, 0],
            [-s, c, 0, 0],
            [0, 0, c, s],
            [0, 0, -s, c],
        ],
        dtype=float,
    )
    return R


# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------


def stiffness_matrix_2d_fixed_fixed_beam(
    E: int, A: int, I: int, L: float
) -> np.ndarray:
    """
    Generates the stiffness matrix for a fixed-fixed beam element
    """
    # ogni gruppo rappresenta una colonna della matrice di rigidezza

    # reazioni dovute allo spostamento assiale del nodo i
    Kniui = E * A / L  # diagonale
    Ktiui = 0
    Kmiui = 0
    Knjui = -E * A / L
    Ktjui = 0
    Kmjui = 0

    # ##########################################################################
    # reazioni dovute allo traslazione trasverale del nodo i
    Knivi = 0
    Ktivi = 12 * E * I / L**3  # diagonale
    Kmivi = 6 * E * I / L**2
    Knjvi = 0
    Ktjvi = -12 * E * I / L**3
    Kmjvi = 6 * E * I / L**2

    # ##########################################################################
    # reazioni dovute alla rotazione del nodo i
    Kniri = 0
    Ktiri = 6 * E * I / L**2
    Kmiri = 4 * E * I / L  # diagonale
    Knjri = 0
    Ktjri = -6 * E * I / L**2
    Kmjri = 2 * E * I / L

    # ##########################################################################
    # reazioni dovute allo spostamento assiale del nodo j
    Kniuj = -E * A / L
    Ktiuj = 0
    Kmiuj = 0
    Knjuj = E * A / L  # diagonale
    Ktjuj = 0
    Kmjuj = 0

    # ##########################################################################
    # reazioni dovute alla traslazione trasversale del nodo j
    Knivj = 0
    Ktivj = -12 * E * I / L**3
    Kmivj = -6 * E * I / L**2
    Knjvj = 0
    Ktjvj = 12 * E * I / L**3  # diagonale
    Kmjvj = -6 * E * I / L**2

    # ##########################################################################
    # reazioni dovute alla rotazione del nodo j
    Knirj = 0
    Ktirj = 6 * E * I / L**2
    Kmirj = 2 * E * I / L
    Knjrj = 0
    Ktjrj = -6 * E * I / L**2
    Kmjrj = 4 * E * I / L  # diagonale

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

    return stiffness_matrix


# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------


def stiffness_matrix_2d_fixed_hinged_beam(
    E: int, A: int, I: int, L: float
) -> np.ndarray:
    """
    Generates the stiffness matrix for a fixed-hinged beam element
    """
    # ogni gruppo rappresenta una colonna della matrice di rigidezza

    # reazioni dovute allo spostamento assiale del nodo i
    Kniui = E * A / L  # diagonale
    Ktiui = 0
    Kmiui = 0
    Knjui = -E * A / L
    Ktjui = 0
    Kmjui = 0

    # ##########################################################################
    # reazioni dovute allo traslazione trasverale del nodo i
    Knivi = 0
    Ktivi = 3 * E * I / L**3  # diagonale
    Kmivi = 3 * E * I / L**2
    Knjvi = 0
    Ktjvi = -3 * E * I / L**3
    Kmjvi = 0

    # ##########################################################################
    # reazioni dovute alla rotazione del nodo i
    Kniri = 0
    Ktiri = 3 * E * I / L**2
    Kmiri = 3 * E * I / L  # diagonale
    Knjri = 0
    Ktjri = -3 * E * I / L**2
    Kmjri = 0

    # ##########################################################################
    # reazioni dovute allo spostamento assiale del nodo j
    Kniuj = -E * A / L
    Ktiuj = 0
    Kmiuj = 0
    Knjuj = E * A / L  # diagonale
    Ktjuj = 0
    Kmjuj = 0

    # ##########################################################################
    # reazioni dovute alla traslazione trasversale del nodo j
    Knivj = 0
    Ktivj = -3 * E * I / L**3
    Kmivj = -3 * E * I / L**2
    Knjvj = 0
    Ktjvj = 3 * E * I / L**3  # diagonale
    Kmjvj = 0

    # ##########################################################################
    # reazioni dovute alla rotazione del nodo j
    Knirj = 0
    Ktirj = 0
    Kmirj = 0
    Knjrj = 0
    Ktjrj = 0
    Kmjrj = 0  # diagonale

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

    return stiffness_matrix


# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------


def stiffness_matrix_2d_hinged_fixed_beam(
    E: int, A: int, I: int, L: float
) -> np.ndarray:
    """
    Generates the stiffness matrix for a hinged-fixed beam element
    """
    # ogni gruppo rappresenta una colonna della matrice di rigidezza

    # reazioni dovute allo spostamento assiale del nodo i
    Kniui = E * A / L  # diagonale
    Ktiui = 0
    Kmiui = 0
    Knjui = -E * A / L
    Ktjui = 0
    Kmjui = 0

    # ##########################################################################
    # reazioni dovute allo traslazione trasverale del nodo i
    Knivi = 0
    Ktivi = 3 * E * I / L**3  # diagonale
    Kmivi = 0
    Knjvi = 0
    Ktjvi = -3 * E * I / L**3
    Kmjvi = 3 * E * I / L**2

    # ##########################################################################
    # reazioni dovute alla rotazione del nodo i
    Kniri = 0
    Ktiri = 0
    Kmiri = 0  # diagonale
    Knjri = 0
    Ktjri = 0
    Kmjri = 0

    # ##########################################################################
    # reazioni dovute allo spostamento assiale del nodo j
    Kniuj = -E * A / L
    Ktiuj = 0
    Kmiuj = 0
    Knjuj = E * A / L  # diagonale
    Ktjuj = 0
    Kmjuj = 0

    # ##########################################################################
    # reazioni dovute alla traslazione trasversale del nodo j
    Knivj = 0
    Ktivj = -3 * E * I / L**3
    Kmivj = 0
    Knjvj = 0
    Ktjvj = 3 * E * I / L**3  # diagonale
    Kmjvj = -3 * E * I / L**2

    # ##########################################################################
    # reazioni dovute alla rotazione del nodo j
    Knirj = 0
    Ktirj = 3 * E * I / L**2
    Kmirj = 0
    Knjrj = 0
    Ktjrj = -3 * E * I / L**2
    Kmjrj = 3 * E * I / L  # diagonale

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

    return stiffness_matrix


# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------


def stiffness_matrix_2d_hinged_hinged_beam(
    E: int, A: int, I: int, L: float
) -> np.ndarray:
    """
    Generates the stiffness matrix for a hinged-hinged beam element
    """
    # ogni gruppo rappresenta una colonna della matrice di rigidezza

    # reazioni dovute allo spostamento assiale del nodo i
    Kniui = E * A / L  # diagonale
    Ktiui = 0
    Kmiui = 0
    Knjui = -E * A / L
    Ktjui = 0
    Kmjui = 0

    # ##########################################################################
    # reazioni dovute allo traslazione trasverale del nodo i
    Knivi = 0
    Ktivi = None  # diagonale
    Kmivi = None
    Knjvi = 0
    Ktjvi = None
    Kmjvi = None

    # ##########################################################################
    # reazioni dovute alla rotazione del nodo i
    Kniri = 0
    Ktiri = None
    Kmiri = None  # diagonale
    Knjri = 0
    Ktjri = None
    Kmjri = None

    # ##########################################################################
    # reazioni dovute allo spostamento assiale del nodo j
    Kniuj = -E * A / L
    Ktiuj = 0
    Kmiuj = 0
    Knjuj = E * A / L  # diagonale
    Ktjuj = 0
    Kmjuj = 0

    # ##########################################################################
    # reazioni dovute alla traslazione trasversale del nodo j
    Knivj = 0
    Ktivj = None
    Kmivj = None
    Knjvj = 0
    Ktjvj = None  # diagonale
    Kmjvj = None

    # ##########################################################################
    # reazioni dovute alla rotazione del nodo j
    Knirj = 0
    Ktirj = None
    Kmirj = None
    Knjrj = 0
    Ktjrj = None
    Kmjrj = None  # diagonale

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

    return stiffness_matrix
