from prettytable import PrettyTable, TableStyle
from .solution import FrameSolution
from .elements import Frame
import numpy as np

def report_header()->str:
    """Returns the header for the report."""

    header = """
Note:
    kN = kiloNewton, kNm = kiloNewton meter, mm = millimeter, rad = radian

    RESTRAINTS:
    an X indicates a restrained degree of freedom, a - indicates a free degree of freedom
    a node can be restrained in the horizontal, vertical, and rotational directions
    ordererd as [X X X].
    example: 
    [X X -] is a hinge
    [- - -] is a free node
    [- X -] is a vertical support (horizontal roller)
    [X X X] is a fixed support
    [- - X] is guided support without rotation


    REACTIONS:
    - Hr = Horizontal reaction, 
    - Vr = Vertical reaction, 
    - Mr = Moment reaction

    ACTIONS:
    - Ha = Horizontal action, 
    - Va = Vertical action, 
    - Ma = Moment action

    DISPLACEMENTS:
    - dx = Displacement in the horizontal direction, 
    - dy = Displacement in the vertical direction
    - rz = Rotation around the z-axis
        """
    return header


def report_node_table(frame: FrameSolution) -> str:
    """Returns the node report table."""
    fields = [
        "Node",
        "Coordinates",
        "Restraints",
        "Hr",
        "Vr",
        "Mr",
        "Ha",
        "Va",
        "Ma",
        "dx",
        "dy",
        "rz",
    ]

    # LAMBDAS
    ############################
    restraints_ = (
        lambda x, y, r: f"[{'X' if x else '-'} {'X' if y else '-'} {'X' if r else '-'}]"
    )

    # DATA
    ############################
    n = len(frame.N)

    # crea una matrice vuota di dimensioni (nodi, colonne) con tipo object
    # per contenere i dati del report
    X = np.empty((n, len(fields)), dtype=object)

    # prima riga: nome del nodo (preceduto dalla lettera 'n')
    X[:, 0] = [f"n{node.id}" for node in frame.N]
    # seconda riga: coordinate del nodo
    X[:, 1] = [str(node.coordinates) for node in frame.N]
    # terza riga: vincoli del nodo
    X[:, 2] = [restraints_(*node.restraints) for node in frame.N]
    # quarta riga: reazioni orizzontali del nodo
    X[:, 3] = [f"{(float(frame.R[i,0]))/1000:.1f} kN" for i in range(n)]
    # quinta riga: reazioni verticali del nodo
    X[:, 4] = [f"{(float(frame.R[1,1]))/1000:.1f} kN" for i in range(n)]
    # sesta riga: reazioni momenti del nodo
    X[:, 5] = [f"{(float(frame.R[i,2]))/1000000:.2f} kNm" for i in range(n)]
    # settima riga: azioni orizzontali del nodo
    X[:, 6] = [f"{(float(frame.L[i,0]))/1000:.1f} kN" for i in range(n)]
    # ottava riga: azioni verticali del nodo
    X[:, 7] = [f"{(float(frame.L[i,1]))/1000:.1f} kN" for i in range(n)]
    # nona riga: azioni momenti del nodo
    X[:, 8] = [f"{(float(frame.L[i,2]))/1000000:.2f} kNm" for i in range(n)]
    # decima riga: spostamenti orizzontali del nodo
    X[:, 9] = [f"{float(frame.D[i,0]):.1f} mm" for i in range(n)]
    # undicesima riga: spostamenti verticali del nodo
    X[:, 10] = [f"{float(frame.D[i,1]):.1f} mm" for i in range(n)]
    # dodicesima riga: rotazioni del nodo
    X[:, 11] = [f"{float(frame.D[i,2]):.5f} rad" for i in range(n)]

    # TABLE
    ############################
    node_report_table = PrettyTable()
    node_report_table.set_style(TableStyle.SINGLE_BORDER)
    node_report_table.field_names =fields
    node_report_table.add_rows(X.tolist())

    return node_report_table.get_string()


def report_beam_table(frame: FrameSolution) -> str:
    """Returns the beam report table."""

    fields = [
        "Beam",
        "Length",
        "Material",
        "Section",
        "Side",
        "Releases",
    ]
    # LAMBDAS
    ############################
    releases_ = lambda rel: f"{'O' if rel[0] else '-'} {'O' if rel[1] else '-'}"

    # DATA
    ############################

    # crea una matrice vuota di dimensioni (nodi, colonne) con tipo object
    # per contenere i dati del report
    X = np.empty((len(frame.B), len(fields)), dtype=object)

    # prima riga: nome dell'elemento (preceduto dalla lettera 'n')
    X[:, 0] = [beam.id for beam in frame.B]
    # seconda riga: lunghezza del nodo
    X[:, 1] = [f"{int(beam.L)} mm" for beam in frame.B]
    # terza riga: nome del materiale
    X[:, 2] = [beam.material.name for beam in frame.B]
    # quarta riga: nome della sezione
    X[:, 3] = [beam.section.profile for beam in frame.B]
    # quinta riga: lato su cui agisce il carico della sezione
    X[:, 4] = [beam.side for beam in frame.B]
    # sesta riga: rilasci interni della trave
    X[:, 5] = [releases_(beam.releases) for beam in frame.B]

    # TABLE
    ############################
    beam_report_table = PrettyTable()
    beam_report_table.set_style(TableStyle.SINGLE_BORDER)
    beam_report_table.field_names = fields
    beam_report_table.add_rows(X.tolist())

    return beam_report_table.get_string()

    # # crea una matrice vuota di dimensioni (nodi, colonne) con tipo object
    # # per contenere i dati del report
    # X = np.empty((len(frame.N), len(fields)), dtype=object)

    # # prima riga: nome del nodo (preceduto dalla lettera 'n')
    # X[:, 0] = [f"n{node.id}" for node in frame.N]
    # # seconda riga: coordinate del nodo
    # X[:, 1] = [str(node.coordinates) for node in frame.N]
    # # terza riga: vincoli del nodo
    # X[:, 2] = [restraints_(*node.restraints) for node in frame.N]
    # # quarta riga: reazioni orizzontali del nodo
    # X[:, 3] = [f"{(float(frame.R[i]))/1000:.1f} kN" for i in range(0, len(frame.R), 3)]
    # # quinta riga: reazioni verticali del nodo
    # X[:, 4] = [f"{(float(frame.R[i]))/1000:.1f} kN" for i in range(1, len(frame.R), 3)]
    # # sesta riga: reazioni momenti del nodo
    # X[:, 5] = [
    #     f"{(float(frame.R[i]))/1000000:.2f} kNm" for i in range(2, len(frame.R), 3)
    # ]
    # # settima riga: azioni orizzontali del nodo
    # X[:, 6] = [f"{(float(frame.L[i]))/1000:.1f} kN" for i in range(0, len(frame.L), 3)]
    # # ottava riga: azioni verticali del nodo
    # X[:, 7] = [f"{(float(frame.L[i]))/1000:.1f} kN" for i in range(1, len(frame.L), 3)]
    # # nona riga: azioni momenti del nodo
    # X[:, 8] = [
    #     f"{(float(frame.L[i]))/1000000:.2f} kNm" for i in range(2, len(frame.L), 3)
    # ]
    # # decima riga: spostamenti orizzontali del nodo
    # X[:, 9] = [f"{float(frame.D[i]):.1f} mm" for i in range(0, len(frame.D), 3)]
    # # undicesima riga: spostamenti verticali del nodo
    # X[:, 10] = [f"{float(frame.D[i]):.1f} mm" for i in range(1, len(frame.D), 3)]
    # # dodicesima riga: rotazioni del nodo
    # X[:, 11] = [f"{float(frame.D[i]):.5f} rad" for i in range(2, len(frame.D), 3)]
