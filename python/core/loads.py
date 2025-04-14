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
    # controlla che l'array q abbia la forma corretta
    if q.shape != (4,):
        raise ValueError(
            "q deve essere un array di forma (4,). e deve contenre 4 valori [qni, qti, qnj, qtj]"
        )
    # controlla che l'array q sia di tipo float
    if not issubclass(q.dtype.type, np.floating):
        raise TypeError("q deve essere un array di tipo float")

    # estrai i valori dal parametro q
    qni, qti, qnj, qtj = q

    # genera l'array dei carichi equivalenti vuoto.
    eq_loads = np.zeros(6, dtype=float)  # [Ni, Ti, Mi, Nj, Tj, Mj]

    # AZIONI LONGITUDINALI lungo l'asse della trave
    ##################################
    # carico totale dovuto alla forza assiale (trapezio)
    N = (qni + qnj) / 2 * l
    # ogni nodo ha la metà del carico totale assiale
    Ni = N / 2
    Nj = N / 2

    axial = np.array([Ni, 0, 0, Nj, 0, 0], dtype=float)
    # AZIONI TRASVERSALI normali all'asse della trave
    ##################################
    # calcola il delta di carico trasversale, in valore assoluto
    delta_qt = abs(qtj - qti)

    # calcola la parte costante (rettangolare)
    qt = max(qti, qtj) - delta_qt

    # carichi dovuti alla parte costante del carico
    Tic = +qt * l / 2
    Mic = +qt * l**2 / 12
    Tjc = +qt * l / 2
    Mjc = -qt * l**2 / 12

    constants = np.array([0, Tic, Mic, 0, Tjc, Mjc], dtype=float)

    # calcola i carichi dovuti alla parte variabile del carico
    Tiv = 3 / 20 * delta_qt * l
    Miv = 1 / 30 * delta_qt * l**2
    Tjv = 7 / 20 * delta_qt * l
    Mjv = -1 / 20 * delta_qt * l**2

    # se il nodo j non è il  nodo con il carico maggiore, scambia i valori
    if qti > qtj:
        Tiv, Miv, Tjv, Mjv = Tjv, Mjv, Tiv, Miv

    variables = np.array([0, Tiv, Miv, 0, Tjv, Mjv], dtype=float)

    # somma le due parti
    eq_loads = constants + variables
    return eq_loads
