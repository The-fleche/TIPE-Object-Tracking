import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rd

N = 1000000

l_0 = 2.7e-2 # en mètres
L = 7.0e-2 # en mètres
u_L = 1e-3 # en mètres
m = 200e-3 # en kilogramme
u_m = 1e-4 # en kilogramme
g  = 9.81


L1 = [2.7e-2, 3.2e-2, 3.7e-2, 4.2e-2, 4.7e-2, 5.9e-2, 7e-2]
L2 = [2.7e-2, 3.2e-2, 3.7e-2, 4.2e-2, 4.8e-2, 5.8e-2, 6.9e-2]  
m = [0, 25e-3, 50e-3, 75e-3, 100e-3, 150e-3, 200e-3]

#L_0_sim = rd.normal(l_0, u_L, N)
K = []
u_K = []

for i in range(1, len(L1)):
    L_sim = rd.normal(L1[i], u_L, N)    
    m_sim = rd.normal(m[i], u_m, N)
    K_sim = (m_sim * g) / (L_sim - l_0)
    u_K.append(np.std(K_sim, ddof = 1))
    K.append(np.mean(K_sim))
    
print("K :", np.mean(K))
print("u_K:", np.mean(u_K))