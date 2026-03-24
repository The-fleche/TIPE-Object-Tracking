import matplotlib.pyplot as plt
import numpy as np

# Données expérimentales
L1 = [2.7, 3.2, 3.7, 4.2, 4.7, 5.7, 7]
L2 = [2.7, 3.2, 3.7, 4.2, 4.8, 5.8, 6.9]  
m = [0, 25e-3, 50e-3, 75e-3, 100e-3, 150e-3, 200e-3]
g  = 9.81

# Conversion en mètres
L1 = np.array(L1) * 1e-2
L2 = np.array(L2) * 1e-2
m = np.array(m)

# Incertitudes 
delta_L = 0.1e-2  # 0.1 cm d'incertitude sur les longueurs
delta_m = 0.1e-3  # 0.1 g d'incertitude sur la masse

# Calcul des grandeurs utiles
F = m * g
elong1 = L1 - L1[0]
elong2 = L2 - L2[0]

# Incertitudes sur F et élongations
delta_F = delta_m * g
delta_elong = delta_L

# Tracé avec barres d’erreur
plt.errorbar(elong1, F, xerr=delta_F, yerr=delta_elong, fmt='x', label='élongation ressort 1', color='blue', capsize=3)
plt.errorbar(elong2, F, xerr=delta_F, yerr=delta_elong, fmt='x', label='élongation ressort 2', color='orange', capsize=3)

a, b = np.polyfit(elong1, F, 1)
print(a, b)

a,b = np.polyfit(elong2, F, 1)
print(a, b)

plt.plot(elong1, a * elong1 + b, label='Régression ressort 1', color='blue', linestyle='--')

# Mise en forme du graphique
plt.xlabel("Force (N)")
plt.ylabel("Élongation (cm)")
plt.title("Élongation des ressorts en fonction de la force")
plt.legend()
plt.grid(True)
plt.show()
