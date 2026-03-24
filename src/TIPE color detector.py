import cv2
import numpy as np

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
# Add the other colors
# They are one my personnal discord server

while True:
    try:
        color = str(input("Which color do you want to track?")).lower().strip()
        np.array(colors[color][:3])
        break
    except:
        print("Choose a color among those one: blue, beige, white, pink, yellow, light_green, orange, black")


while True:
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


    # Left and Right are only reversed graphically
    if x > center_x + acceptance_x:
        cv2.putText(frame, "Right", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # Add the code to turn the camera to the left
        print("droite")
    elif x < center_x - acceptance_x:
        cv2.putText(frame, "Left", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # Add the code to turn the camera to the right
        print("gauche")
    if y > center_y + acceptance_y:
        cv2.putText(frame, "Up", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # Add the code to turn the camera to the up
    if y < center_y - acceptance_y:
        # Add the code to turn the camera to the down
        cv2.putText(frame, "Down", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    
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