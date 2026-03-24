import numpy as np
import numpy.random as rd

N = 100000

H = [12.8, 12.7, 10.9, 12.0, 11.4, 11.0, 13.0, 10.1, 11.7]
u_H = 2e-3
L = 28e-2
u_L = 1e-3

L_sim = rd.normal(L, u_L, N)

f = []
u_f = []

for i in range(len(H)):
    H_sim = rd.normal(H[i] * 10**-2, u_H, N)
    f_sim = H_sim/(L_sim**2-H_sim**2)**0.5
    u_f.append(np.std(f_sim, ddof = 1))
    f.append(np.mean(f_sim))

print("K :", np.mean(f))
print("u_K:", np.mean(u_f))