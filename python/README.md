# Metodo delle rigidezze (matriciale)

Risoluzione matriciale del telaio con il metodo degli **spostamenti**.

## 1 - matrice delle rigidezze locali

Per ogni elemento si genera la matrice delle rigidezze nel sistema di riferimento locale del'asta.

$
\mathbf{K}_{local} = 
\begin{bmatrix}
K_{N_iu_i} & K_{N_iv_i} & K_{N_ir_i} & K_{N_iu_j} & K_{N_iv_j} & K_{N_ir_j} \\
K_{T_iu_i} & K_{T_iv_i} & K_{T_ir_i} & K_{T_iu_j} & K_{T_iv_j} & K_{T_ir_j} \\
K_{M_iu_i} & K_{M_iv_i} & K_{M_ir_i} & K_{M_iu_j} & K_{M_iv_j} & K_{M_ir_j} \\
K_{N_ju_i} & K_{N_jv_i} & K_{N_jr_i} & K_{N_ju_j} & K_{N_jv_j} & K_{N_jr_j} \\
K_{T_ju_i} & K_{T_jv_i} & K_{T_jr_i} & K_{T_ju_j} & K_{T_jv_j} & K_{T_jr_j} \\
K_{M_ju_i} & K_{M_jv_i} & K_{M_jr_i} & K_{M_ju_j} & K_{M_jv_j} & K_{M_jr_j}
\end{bmatrix}
$

Essa può essere riferita alla configurazione di vincolo INCASTRO-INCASTRO oppure alla configurazione di vincolo CERNIERA-INCASTRO.

La matrice si legge inquesto modo:

Il primo pedice rappresenta quale reazione vincolare nasce in corrispondenza  del nodo e sono ordinate come segue:
  1.  N: azione assiale, 
  2.  T: azione trasversale, 
  3.  M: momento.

Il secondo pedice rappresenta quale spostamento genera l'azione precedentemente descritta e sono ordinati come 
  1. **u**: spostamento assiale, 
  2. **v**: spostamento trasversale, 
  3. **r**: rotazione

Ad esempio,  il termine $K_{T_ir_j}$ rappresenta la reazione vincolare `T` (forza trasversale) che si genera in corrispondenza del nodo `i`  a seguito di uno di una rotazione `r` del nodo `j`.

## 2 - matrice di trasformazione

La matrice di trasformazione `R` è una matrice quadrata 6x6 che permette di passare dalla matrice delle rigidezze locali alla matrice delle rigidezze globali. Essa è definita come:

$
\mathbf{R} =
\begin{bmatrix}
0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 \\
\end{bmatrix}
$


```
            
            |                                           |
 Ni Ti Mi   |———————————————————————————————————————————|   Nj Tj Mj
            |                                           |
                                         

```