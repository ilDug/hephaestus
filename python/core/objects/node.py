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

    
    # M0 float # momento esterno applicato (in coordinate globali) in kNm
    # V0 float # forza verticale esterna applicata  (in coordinate globali) in kN
    # # forza orizzontale esterna applicata ( in coordinate globali) in kN
    # H0 float

    # dx0 float # spostamento in coordinate globali imposto dall'esterno (in mm)
    # dy0 float # spostamento in coordinate globali imposto dall'esterno (in mm)
    # dx0 float # spostamento in coordinate globali imposto dall'esterno (in mm)

    # rx0 float # rotazione in coordinate globali imposta dell'esterno (in rad)
    # ry0 float # rotazione in coordinate globali imposta dell'esterno (in rad)
    # rz0 float # rotazione in coordinate globali imposta dell'esterno (in rad)
    
