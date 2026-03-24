import cv2
import numpy as np

img = cv2.imread('IMG_6270.jpg')
img = cv2.resize(img, (720, 480))


def Orientation(x, y):
    # on récupére l'angle de la direction du gradient
    if Gradient_x[x,y] == 0:
        theta = 90
        return theta
    theta = np.arctan(Gradient_y[x, y] / Gradient_x[x, y])
    # on le compare avec des directions simples
    angle = [0, 45, 90, 135]
    dist = [abs(theta - angle[i]) for i in range(len(angle))]
    index = dist.index(min(dist))
    # on retourne l'angle le plus proche
    theta = angle[index]
    return theta

# Convert to level of grey
grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img.resize((640, 480))
n, m = grey_img.shape

# apply gaussian blur
blurred = cv2.GaussianBlur(grey_img, (5, 5), 0)

# calcul of the gradient

Sx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
Sy = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

Gradient_x = np.zeros((n, m))
Gradient_y = np.zeros((n, m))

# calcul of the approximation of the gradient
for i in range(1, n-1):
    for j in range(1, m-1):
        Gradient_x[i, j] = np.sum(Sx * grey_img[i-1:i+2, j-1:j+2])
        Gradient_y[i, j] = np.sum(Sy * grey_img[i-1:i+2, j-1:j+2])
        
Gradient = np.sqrt(Gradient_x**2 + Gradient_y**2)

# suppression of the noise

for i in range(1, n-1):
    for j in range(1, m-1):
        theta = Orientation(i, j)
        if theta == 0: #       0° (horizontal)
            if Gradient[i, j] < Gradient[i, j-1] or Gradient[i, j] < Gradient[i, j+1]:
                Gradient[i, j] = 0
        elif theta == 45: #    45° (diagonale montante)
            if Gradient[i, j] < Gradient[i-1, j+1] or Gradient[i, j] < Gradient[i+1, j-1]: # haut droite et bas gauche
                Gradient[i, j] = 0
        elif theta == 90: #    90° (vertical)
            if Gradient[i, j] < Gradient[i-1, j] or Gradient[i, j] < Gradient[i+1, j]:
                Gradient[i, j] = 0
        elif theta == 135: #   135° (diagonale descendante)
            if Gradient[i, j] < Gradient[i-1, j-1] or Gradient[i, j] < Gradient[i+1, j+1]: # haut gauche et bas droite
                Gradient[i, j] = 0

# hystreresis thresholding

# high threshold
high = 0.2 * np.max(Gradient)
# low threshold
low = 0.1 * np.max(Gradient)

def is_contour(x, y):
    # on regarde si les voisins de x, y sont des contours
    if Gradient[x-1, y] > high: #haut
        return True
    elif Gradient[x+1, y] > high: #bas
        return True
    elif Gradient[x, y-1] > high: #gauche
        return True
    elif Gradient[x, y+1] > high: #droite
        return True
    elif Gradient[x-1, y-1] > high: #haut gauche
        return True
    elif Gradient[x-1, y+1] > high: #haut droite
        return True
    elif Gradient[x+1, y+1] > high: #bas droite
        return True
    elif Gradient[x+1, y-1] > high: #bas gauche
        return True
    # si aucun voisin n'est un contour fort
    return False

# on parcourt l'image

for i in range(1, n-1):
    for j in range(1, m-1):
        if Gradient[i, j] > high:
            Gradient[i, j] = 255
        elif Gradient[i, j] < low:
            Gradient[i, j] = 0
        else:
            if is_contour(i, j):
                Gradient[i, j] = 255
            else:
                Gradient[i, j] = 0

# Display the frame

cv2.imshow('Image originale', img)
cv2.imshow('Contours détectés', Gradient )
cv2.waitKey(0)
cv2.destroyAllWindows()
