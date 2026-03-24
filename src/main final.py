from serial import *
import cv2
from math import sqrt
from time import sleep, time
import numpy as np
from commande_slider import *


cap = cv2.VideoCapture(1)
# Set camera resolution
cap.set(3, 720)
cap.set(4, 480)
_, frame = cap.read()
rows, cols, _ = frame.shape
center_x = int(cols/2)
center_y = int(rows/2)
acceptance_x = 50
acceptance_y = 20
x, y = center_x, center_y

colors = {"blue": [94, 80, 2, 126, 255, 255],
          "beige": [0, 64, 21, 116, 205, 128],
          "white": [0, 0, 255, 73, 101, 255],
          "pink": [126, 179, 167, 193, 255, 255],
          "yellow":  [0, 116, 206, 33, 198, 255],
          "light_green":  [31, 31, 172, 68, 198, 255],
          "orange": [7, 134, 54, 69, 255, 255],
          "black": [0, 0, 0, 255, 255, 10],
          "green": [20, 95, 36, 94, 154, 186],
          "red": [2, 146, 76, 255, 255, 255]
         }

# set slider
temps = 0.1 # en s ; c'est le temps entre de réaction du slider
v_max = 0.125 # en m/s
rot_max = 9.3 # en rad/s
v = 0.1
d_max = 1.25
is_linked, slider_port = find_Slider()
if is_linked: # si le slider est branché
    ser = Serial(port=slider_port, baudrate=115200, timeout=1)
else:
    print("Slider non branché")
    raise SystemExit("Slider not connected")
# on attend que la liaison se fait
time.sleep(1)
# on vérifie que le slider est opérationnel
swrite(ser, "?#")
if sread(ser, 2) != "OK":
    pass
# on se place à l'origine
origine(ser)
pos = 0
sleep(2)
# On vide la ligne de réponse du slider, une fois à l'origine, du cache 
sread(ser, 8)

while True:
    try:
        color = str(input("Which color do you want to track?")).lower().strip()
        np.array(colors[color][:3])
        break
    except:
        print("Choose a color among those one: blue, beige, white, pink, yellow, light_green, orange, black")
    

while True:
    start = now = time.time()
    # Read the frame    
    _, frame = cap.read()
    # Convert to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    low_color = np.array(colors[color][:3])
    high_color = np.array(colors[color][3:])
    
    # Create a mask
    mask = cv2.inRange(hsv_frame, low_color, high_color)
    
    # Creation of the object's contours
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 1000:
            cv2.drawContours(frame, contour, -1, (0, 255, 0), -1)
            # draw the rectangle containing the object
            borders = max(contours, key=cv2.contourArea)
            x, y, obj_width, obj_height = cv2.boundingRect(borders)
            cv2.rectangle(frame, (x, y), (x + obj_width, y + obj_height), (0, 0, 255), 3)
            # Calcul of the center of the object
            M = cv2.moments(contour)
            if M["m00"] != 0:
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])
                # Draw a circle at the center of the object and write the position
                cv2.circle(frame, (x, y), 7, (255, 255, 255), -1)

    
    # Draw a rectangle at the center of the frame
    cv2.rectangle(frame, (center_x - acceptance_x, center_y - acceptance_y), (center_x + acceptance_x, center_y + acceptance_y), (255, 255, 255), 2)
    cv2.circle(frame, (center_x, center_y), 7, (255, 255, 255), -1)
    
    #  !!!!!!!!!!!!! IT DEPENDS IF THE CAMERA GIVE A REVERSED IMAGE OR NOT   !!!!!!!!!!!! 
    # By default, I supposed that the camera gives a reversed image because I'm using my frontal camera
    dist = 0.03

    # Left and Right are only reversed graphically
    if x > center_x + acceptance_x:
        cv2.putText(frame, "Right", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # Add the code to turn the camera to the left
        if pos - dist >= 0:
            pos -= dist
        translation(ser, v, pos)
    elif x < center_x - acceptance_x:
        cv2.putText(frame, "Left", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # Add the code to turn the camera to the right
        print("gauche")
        if pos + dist < d_max:
            pos += dist
        translation(ser, v, pos)
    else:
        translation(ser, v, pos)
    temps = dist/v
    print("pos :", pos)
        
    # affichage du flux vidéo pendant le déplacement
    while now - start <= temps:
        now = time.time()
        _, frame = cap.read()
        cv2.rectangle(frame, (center_x - acceptance_x, center_y - acceptance_y), (center_x + acceptance_x, center_y + acceptance_y), (255, 255, 255), 2)
        cv2.circle(frame, (center_x, center_y), 7, (255, 255, 255), -1)
        cv2.putText(frame, "Moving...", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(frame, "Position: " + str(pos), (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow("Frame", frame)
 
    # Display the frame
    cv2.imshow("Frame", frame)
    # Boucle exit condition
    key = cv2.waitKey(1)
    if key == 27: # press esc to exit
        break 
    elif key == ord('s'):
            cv2.imwrite("saved_image.jpg", frame)
            cv2.imwrite("saved_blue_mask.jpg", mask)
    
cap.release()
cv2.destroyAllWindows() 