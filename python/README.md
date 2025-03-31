# Metodo delle rigidezze (matriciale)

Risoluzione matriciale del telaio con il metodo degli **spostamenti**.

## 1 - matrice delle rigidezze locali

Per ogni elemento si genera la matrice delle rigidezze nel sistema di riferimento locale del'asta.

$
\mathbf{K}_{local} = 
\begin{bmatrix}
k_{11} & k_{12} & k_{13} & k_{14} & k_{15} & k_{16} \\
k_{21} & k_{22} & k_{23} & k_{24} & k_{25} & k_{26} \\
k_{31} & k_{32} & k_{33} & k_{34} & k_{35} & k_{36} \\
k_{41} & k_{42} & k_{43} & k_{44} & k_{45} & k_{46} \\
k_{51} & k_{52} & k_{53} & k_{54} & k_{55} & k_{56} \\
k_{61} & k_{62} & k_{63} & k_{64} & k_{65} & k_{66} 
\end{bmatrix}
$

Essa può essere riferita alla configurazione di vincolo INCASTRO-INCASTRO oppure alla configurazione di vincolo CERNIERA-INCASTRO.

La matrice si legge inquesto modo:

Il primo pedice rappresenta quale reazione vincolare nasce in corrispondenza  del nodo e sono ordinate come segue:
  1.  N: azione assiale, 
  2.  T: azione trasversale, 
  3.  M: momento.

Il secondo pedice rappresenta quale spostamento genera l'azione precedentemente descritta e sono ordinati come 
  1. U: spostamento assiale, 
  2. V: spostamento trasversale, 
  3. R: rotazione

Ad esempio,  il termine `k23` rappresenta la reazione vincolare T (forza trasversale) che si genera in corrispondenza del nodo `i` (da 1 a 3 si rifesriscono al nodo `i`, mentre da 4 a 6 si riferiscono al nodo`j`) a seguito di uno di una rotazione R (da 1 a 3 sono gli spostamenti del nodo `i` mentre da 4 a 6  si riferiscono agli spostamenti del nodo `j`) del nodo `j`.

## 2 - matrice di trasformazione

La matrice di trasformazione `T` è una matrice quadrata 6x6 che permette di passare dalla matrice delle rigidezze locali alla matrice delle rigidezze globali. Essa è definita come:

$
\mathbf{T} =
\begin{bmatrix}
0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 \\
\end{bmatrix}
$