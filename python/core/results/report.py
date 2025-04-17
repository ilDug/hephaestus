from prettytable import PrettyTable, TableStyle
from ..loads import DistributedLoad, PointLoad, MomentumLoad
from .solution import FrameSolution
import numpy as np


def report_header() -> str:
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
        "Ha",
        "Va",
        "Ma",
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
    # settima riga: azioni orizzontali del nodo
    X[:, 3] = [f"{(float(frame.L[i,0]))/1000:.1f} kN" for i in range(n)]
    # ottava riga: azioni verticali del nodo
    X[:, 4] = [f"{(float(frame.L[i,1]))/1000:.1f} kN" for i in range(n)]
    # nona riga: azioni momenti del nodo
    X[:, 5] = [f"{(float(frame.L[i,2]))/1000000:.2f} kNm" for i in range(n)]

    # TABLE
    ############################
    node_report_table = PrettyTable()
    node_report_table.set_style(TableStyle.SINGLE_BORDER)
    node_report_table.field_names = fields
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


def report_beam_actions(frame: FrameSolution) -> str:
    fields = [
        "Beam",
        "distibuted load [qx, qy]",
        "point load [(fx, fy), x]",
        "moment load [M, x]",
    ]

    d_loads = lambda loads: "| ".join(
        [
            f"(qx:{l.P[0]},qy:{l.P[1]}) kN/m"
            for l in loads
            if isinstance(l, DistributedLoad)
        ]
    )
    p_loads = lambda loads: "| ".join(
        [
            f"(Fx:{l.P[0]/1000:.1f}, Fy:{l.P[1]/1000:.1f}) kN @ {l.x} mm"
            for l in loads
            if isinstance(l, PointLoad)
        ]
    )
    m_loads = lambda loads: "| ".join(
        [
            f"{l.M/1000000:.1f} kNm @ {l.x} mm"
            for l in loads
            if isinstance(l, MomentumLoad)
        ]
    )

    # LAMBDAS
    ############################

    n = len(frame.B)
    X = np.empty((len(frame.B), len(fields)), dtype=object)

    #  nome dell'elemento
    X[:, 0] = [beam.id for beam in frame.B]
    #  carico distribuito della trave
    X[:, 1] = [d_loads(beam.ext_loads) for beam in frame.B]
    #  carico puntuale della trave
    X[:, 2] = [p_loads(beam.ext_loads) for beam in frame.B]
    #  carico momento della trave
    X[:, 3] = [m_loads(beam.ext_loads) for beam in frame.B]

    # TABLE
    ############################
    beam_report_table = PrettyTable()
    beam_report_table.set_style(TableStyle.SINGLE_BORDER)
    beam_report_table.field_names = fields
    beam_report_table.add_rows(X.tolist())

    return beam_report_table.get_string()


def report_node_reactions(frame: FrameSolution):
    fields = [
        "Node",
        "Hr",
        "Vr",
        "Mr",
        "dx",
        "dy",
        "rz",
    ]

    # DATA
    ############################
    n = len(frame.N)

    # crea una matrice vuota di dimensioni (nodi, colonne) con tipo object
    # per contenere i dati del report
    X = np.empty((n, len(fields)), dtype=object)

    # prima riga: nome del nodo (preceduto dalla lettera 'n')
    X[:, 0] = [f"n{node.id}" for node in frame.N]
    # reazioni orizzontali del nodo
    X[:, 1] = [f"{(float(frame.R[i,0]))/1000:.2f} kN" for i in range(n)]
    # reazioni verticali del nodo
    X[:, 2] = [f"{(float(frame.R[i,1]))/1000:.2f} kN" for i in range(n)]
    # reazioni momenti del nodo
    X[:, 3] = [f"{(float(frame.R[i,2]))/1000000:.2f} kNm" for i in range(n)]
    # decima riga: spostamenti orizzontali del nodo
    X[:, 4] = [f"{float(frame.D[i,0]):.3f} mm" for i in range(n)]
    # undicesima riga: spostamenti verticali del nodo
    X[:, 5] = [f"{float(frame.D[i,1]):.3f} mm" for i in range(n)]
    # dodicesima riga: rotazioni del nodo
    X[:, 6] = [f"{float(frame.D[i,2]):.5f} rad" for i in range(n)]

    # TABLE
    ############################
    node_report_table = PrettyTable()
    node_report_table.set_style(TableStyle.SINGLE_BORDER)
    node_report_table.field_names = fields
    node_report_table.add_rows(X.tolist())

    return node_report_table.get_string()
