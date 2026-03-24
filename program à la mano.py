import cv2

cap = cv2.VideoCapture(0)
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
lower = 120
upper = 255

while True:
    # Read the frame    
    _, frame = cap.read()
    # Convert to level of grey
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    n, m = grey_frame.shape
    obj = []

    # filter grey to black and white
    for ligne in range(n):
        for colonne in range(m):
            if lower <= grey_frame[ligne][colonne] <= upper:
                grey_frame[ligne][colonne] = 0
            else:
                grey_frame[ligne][colonne] = 255
                if ligne != n-1 and m-1 != colonne:
                    obj.append([ligne, colonne])

    # contour detection
    contours = []
    for i in range(len(obj)):
        ligne, colonne = obj[i][0], obj[i][1]
        if not grey_frame[ligne][colonne+1] == grey_frame[ligne][colonne-1] == grey_frame[ligne-1][colonne] == grey_frame[ligne+1][colonne] == 255:
            contours.append((ligne, colonne))

    # centre des contours
    for i in range(len(contours)):
        y += contours[i][0]
        x += contours[i][1]
    x = x // n
    y = y // n
 
    # Draw a rectangle at the center of the frame
    cv2.rectangle(frame, (center_x - acceptance_x, center_y - acceptance_y), (center_x + acceptance_x, center_y + acceptance_y), (255, 255, 255), 2)
    cv2.circle(frame, (center_x, center_y), 7, (255, 255, 255), -1)

    #  !!!!!!!!!!!!! IT DEPENDS IF THE CAMERA GIVE A REVERSED IMAGE OR NOT   !!!!!!!!!!!! 
    # By default, I supposed that the camera gives a image wich isn't reverse.
    
    # Left and Right are only reversed graphically
    if x > center_x + acceptance_x:
        cv2.putText(frame, "Right", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # Add the code to turn the camera to the left
    if x < center_x - acceptance_x:
        cv2.putText(frame, "Left", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # Add the code to turn the camera to the right
    if y > center_y + acceptance_y:
        cv2.putText(frame, "Down", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # Add the code to turn the camera to the up
    if y < center_y - acceptance_y:
        # Add the code to turn the camera to the down
        cv2.putText(frame, "Up", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
      
    # Display the frame
    
    cv2.imshow("Frame", frame)
    cv2.imshow("Machine", grey_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == ord('s'):
            cv2.imwrite("image.jpg", frame)
