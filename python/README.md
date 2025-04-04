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

### 1.1 - matrice delle rigidezze locali per un'asta **INCASTRO-INCASTRO**

$
\mathbf[K_{\times-\times}] =
\begin{bmatrix}
\frac{EA}{L} & \, & 0 & \, & 0 & \, & -\frac{EA}{L} & \, & 0 & \, & 0 \\[10pt]
0 & \, & \frac{12EI}{L^3} & \, & \frac{6EI}{L^2} & \, & 0 & \, & -\frac{12EI}{L^3} & \, & \frac{6EI}{L^2} \\[10pt]
0 & \, & \frac{6EI}{L^2} & \, & \frac{4EI}{L} & \, & 0 & \, & -\frac{6EI}{L^2} & \, & \frac{2EI}{L} \\[10pt]
-\frac{EA}{L} & \, & 0 & \, & 0 & \, & \frac{EA}{L} & \, & 0 & \, & 0 \\[10pt]
0 & \, & -\frac{12EI}{L^3} & \, & -\frac{6EI}{L^2} & \, & 0 & \, & \frac{12EI}{L^3} & \, & -\frac{6EI}{L^2} \\[10pt]
0 & \, & \frac{6EI}{L^2} & \, & \frac{2EI}{L} & \, & 0 & \, & -\frac{6EI}{L^2} & \, & \frac{4EI}{L}
\end{bmatrix}
$

### 1.2 - matrice delle rigidezze locali per un'asta **CERNIERA-INCASTRO**

$
\mathbf[K_{\odot-\times}] =
\begin{bmatrix}
\frac{EA}{L} & \, & 0 & \, & 0 & \, & -\frac{EA}{L} & \, & 0 & \, & 0 \\[10pt]
0 & \, & \frac{3EI}{L^3} & \, & 0 & \, & 0 & \, & -\frac{3EI}{L^3} & \, & \frac{3EI}{L^2} \\[10pt]
0 & \, & 0 & \, & 0 & \, & 0 & \, & 0 & \, & 0 \\[10pt]
-\frac{EA}{L} & \, & 0 & \, & 0 & \, & \frac{EA}{L} & \, & 0 & \, & 0 \\[10pt]
0 & \, & -\frac{3EI}{L^3} & \, & 0 & \, & 0 & \, & \frac{3EI}{L^3} & \, & -\frac{3EI}{L^2} \\[10pt]
0 & \, & \frac{3EI}{L^2} & \, & 0 & \, & 0 & \, & -\frac{3EI}{L^2} & \, & \frac{3EI}{L}
\end{bmatrix}
$

### 1.3 - matrice delle rigidezze locali per un'asta **INCASTRO-CERNIERA**

$
\mathbf[K_{\times-\odot}] =
\begin{bmatrix}
\frac{EA}{L} & \, & 0 & \, & 0 & \, & -\frac{EA}{L} & \, & 0 & \, & 0 \\[10pt]
0 & \, & \frac{3EI}{L^3} & \, & \frac{3EI}{L^2} & \, & 0 & \, & -\frac{3EI}{L^3} & \, & 0 \\[10pt]
0 & \, & \frac{3EI}{L^2} & \, & \frac{3EI}{L} & \, & 0 & \, & -\frac{3EI}{L^2} & \, & 0 \\[10pt]
-\frac{EA}{L} & \, & 0 & \, & 0 & \, & \frac{EA}{L} & \, & 0 & \, & 0 \\[10pt]
0 & \, & -\frac{3EI}{L^3} & \, & -\frac{3EI}{L^2} & \, & 0 & \, & \frac{3EI}{L^3} & \, & 0 \\[10pt]
0 & \, & 0 & \, & 0 & \, & 0 & \, & 0 & \, & 0 
\end{bmatrix}
$

## 2 - matrice di trasformazione

La matrice di trasformazione `R` è una matrice quadrata 6x6 che permette di passare dalla matrice delle rigidezze locali alla matrice delle rigidezze globali. Essa è definita come:

$
\mathbf{R} =
\begin{bmatrix}
0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 \\
\end{bmatrix}
$


## 3 - matrice delle rigidezze globali