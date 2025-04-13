import numpy as np 


def equivalent_beam_loads_vector_2d_fixed_fixed(qi: float, qj:float, l:int) -> np.ndarray:
    """calcola i carichi equivalenti sui nodi della trave dovuti ai carichi distribuiti
    - qi : carico distribuito sul nodo i in N/mm
    - qj : carico distribuito sul nodo j in N/mm
    - l : lunghezza della trave in mm
    """

    # calcola il delta di carico
    dq = abs(qj-qi)

    # calcola la parte costante
    q = max(qi, qj) - dq

    # carichi dovuti alla parte costante del carico
    Cni = 0 
    Cti = -q * l / 2
    Cmi = -q * l**2 / 12
    Cnj = 0
    Ctj = -q * l / 2
    Cmj = +q * l**2 / 12

    constants = np.array([
        Cni, Cti, Cmi,
        Cnj, Ctj, Cmj
    ], dtype=float)

    # calcola i carichi dovuti alla parte variabile del carico
    Vni = 0
    Vti = -3 / 20 * dq * l
    Vmi = -1 / 30 * dq * l**2
    Vnj = 0
    Vtj = -7 / 20 * dq * l
    Vmj = +1 / 20 * dq * l**2

    # se il nodo j non è il  nodo con il carico maggiore, scambia i valori
    if qi > qj:
        Vni, Vti, Vmi, Vnj, Vtj, Vmj = Vnj, Vtj, Vmj, Vni, Vti, Vmi

    variables = np.array([Vni, Vti, Vmi, Vnj, Vtj, Vmj], dtype=float)

    # riprtiscine i carichi equivalenti su ciascuno dei nodi
    return constants + variables
