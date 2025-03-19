class Node:
    n: int  # ID del nodo
    c: tuple[float, float]  # coordinate assolute in metri

    x: float  # coordinate assolute in millimetri
    y: float  # coordinate assolute in millimetri

    def __init__(self, id: int, coordinates: tuple[float, float]):
        self.n = id
        self.coordinates = coordinates
        self.x, self.y = coordinates
        print(f"created new node at coordinates {self.coordinates}")

    """
    M0 float # momento esterno applicato (in coordinate globali) in kNm
    V0 float # forza verticale esterna applicata  (in coordinate globali) in kN
    # forza orizzontale esterna applicata ( in coordinate globali) in kN
    H0 float

    dx0 float # spostamento in coordinate globali imposto dall'esterno (in mm)
    dy0 float # spostamento in coordinate globali imposto dall'esterno (in mm)
    dx0 float # spostamento in coordinate globali imposto dall'esterno (in mm)

    rx0 float # rotazione in coordinate globali imposta dell'esterno (in rad)
    ry0 float # rotazione in coordinate globali imposta dell'esterno (in rad)
    rz0 float # rotazione in coordinate globali imposta dell'esterno (in rad)
    """


class Beam:
    Ix: int  # momento d'inerzia in mm4 lungo l'asse x
    Iy: int  # momento d'inerzia in mm4 lungo l'asse y
    E: int  # modulo di elasticità in MPa (acciaio = 210000 MPa, N/mm2)
    A: int  # sezione della trave in mm2
    L: float  # lunghezza della trave in mm

    i: Node  # il nodo iniziale
    j: Node  # il nodo finale

    def __init__(self, start: Node, end: Node):
        """crea una nuova trave tra due nodi"""
        self.i = start
        self.j = end
        self.L = ((self.j.x - self.i.x) ** 2 + (self.j.y - self.i.y) ** 2) ** (1 / 2)
        print(
            f"the length of the beam from node {
              self.i.n} to {self.j.n} is {self.L}m"
        )

    def set_material(self, E: int) -> "Beam":
        """imposta il modulo di elasticità del materiale della trave.
        Valore in N/mm2 o MPa: acciacio = 210000"""
        self.E = E
        return self

    def set_section(self, A: int, Ix: int, Iy: int) -> "Beam":
        """ "imposta le proprietà della sezione trasversale della trave.
        A = area della sezione in mm2,
        Ix = momento d'inerzia in mm4 lungo l'asse x,
        Iy = momento d'inerzia in mm4 lungo l'asse y"""
        self.A = A
        self.Ix = Ix
        self.Iy = Iy
        return self