import numpy as np
import matplotlib.pyplot as plt

# Paramètres du système
m = 0.316     # masse (kg)
k = 48     # raideur du ressort (N/m)
F_f = 0.2 # force de frottement sec (N)
x0 = 0.02    # position initiale (m)
v0 = 0.0     # vitesse initiale (m/s)

# Paramètres de la simulation
dt = 0.001                  # pas de temps (s)
t_max = 3.0                # durée totale (s)
N = int(t_max / dt)         # nombre d'itérations
t = np.linspace(0, t_max, N)

# Initialisation des vecteurs
x = np.zeros(N)
v = np.zeros(N)
a = np.zeros(N)

# Conditions initiales
x[0] = x0
v[0] = v0

# Fonction signe 
def sgn(v):
    if v > 0:
        return 1
    elif v < 0:
        return -1
    else:
        return 0

# Intégration numérique par méthode d’Euler explicite
for i in range(1, N):
    # Calcul de la force de frottement (seulement si la vitesse n'est pas nulle)
    if abs(v[i-1]) > 1e-8:
        f_frott = -F_f * sgn(v[i-1])
    elif abs(k * x[i-1]) > F_f: # relance le mouvement si la force de rappel dépasse le frottement
        f_frott = -F_f * sgn(k * x[i-1])  
    else:
        f_frott = -k * x[i-1]  # équilibre statique, pas de frottement sec (bloqué)
    
    # Accélération
    a[i] = (-k * x[i-1] + f_frott) / m
    
    # Intégration (Euler)
    v[i] = v[i-1] + a[i] * dt
    x[i] = x[i-1] + v[i] * dt

# Affichage
plt.figure(figsize=(10, 6))
plt.plot(t, x, label='Position x(t)')
plt.plot(t, v, label='Vitesse v(t)', linestyle='--')
plt.xlabel('Temps (s)')
plt.ylabel('Valeurs')
plt.title('Mouvement de la caméra ') 
plt.legend()
plt.grid(True)
plt.show()
