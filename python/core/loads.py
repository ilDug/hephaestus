import numpy as np 


def equivalent_beam_loads_vector_2d_fixed_fixed(q: np.ndarray, l: int) -> np.ndarray:
    """calcola i carichi equivalenti sui nodi della trave dovuti ai carichi distribuiti
    - qni : carico distribuito longituidinale sul nodo i in N/mm
    - qti : carico distribuito trasversale sul nodo i in N/mm
    - qnj : carico distribuito longituidinale sul nodo j in N/mm
    - qtj : carico distribuito trasversale sul nodo j in N/mm
    - l : lunghezza della trave in mm

    Returns:
        np.ndarray: carichi equivalenti sui nodi i e j
        [Ni, Ti, Mi, Nj, Tj, Mj] in N e Nmm
    """

    qni, qti, qnj, qtj = q
    eq_loads = np.zeros(6, dtype=float)  # [Ni, Ti, Mi, Nj, Tj, Mj]

    # AZIONI LONGITUDINALI lungo l'asse della trave
    ##################################
    # carico totale
    N = (qni + qnj) / 2 * l
    Ni = N / 2
    Nj = N / 2

    # AZIONI TRASVERSALI normali all'asse della trave
    ##################################
    # calcola il delta di carico
    delta_qt = qtj - qti

    # calcola la parte costante (rettangolare)
    qt = max(qti, qtj) - delta_qt

    # carichi dovuti alla parte costante del carico
    Ti = -qt * l / 2
    Mi = -qt * l**2 / 12
    Tj = -qt * l / 2
    Mj = +qt * l**2 / 12

    constants = np.array([Ni, Ti, Mi, Nj, Tj, Mj], dtype=float)

    # calcola i carichi dovuti alla parte variabile del carico
    Ti = -3 / 20 * delta_qt * l
    Mi = -1 / 30 * delta_qt * l**2
    Tj = -7 / 20 * delta_qt * l
    Mj = +1 / 20 * delta_qt * l**2

    # se il nodo j non è il  nodo con il carico maggiore, scambia i valori
    if qti > qtj:
        Ti, Mi, Tj, Mj = Tj, Mj, Ti, Mi

    variables = np.array([Ni, Ti, Mi, Nj, Tj, Mj], dtype=float)

    # somma le due parti
    eq_loads = constants + variables
    return eq_loads
