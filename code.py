# First we are going to capture the background video frame
# Second we Tell the code to recognize the red color
# We need to generate a mask
# We need to create the final output to create a magical output

import cv2
import numpy as np
import time

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))


# Starting the Camera

cap = cv2.VideoCapture(0)
time.sleep(2)

# Store our bg

bg = 0

# Capture the background for 60 frames
for i in range(60):
    ret,bg = cap.read()

bg = np.flip(bg , axis = 1)

while(cap.isOpened()):
    ret , img = cap.read()

    if not ret:
        break

    img = np.flip(img , axis = 1)

    # Convert BGR -> HSV(Hue Saturation Value)
    hsv = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    lower_red = np.array([0 , 120 , 50])
    upper_red = np.array([10 , 255 , 255])
    mask1 = cv2.inRange(hsv , lower_red , upper_red)
    lower_red = np.array([170 , 120 , 70])
    upper_red = np.array([180 , 255 , 255])
    mask2 = cv2.inRange(hsv , lower_red , upper_red)
    mask1 = mask1 + mask2

    mask1 = cv2.morphologyEx(mask1 , cv2.MORPH_OPEN , np.ones((3 , 3) , np.uint8))
    mask1 = cv2.morphologyEx(mask1 , cv2.MORPH_DILATE , np.ones((3 , 3) , np.uint8))

    # What is not in mask1 will be stored in mask2
    # bitwise operator -> works on 0 , 1
    mask2 = cv2.bitwise_not(mask1)
    res1 = cv2.bitwise_and(img , img , mask = mask2)
    res2 = cv2.bitwise_and(bg , bg , mask = mask1)

    final_output = cv2.addWeighted(res1 , 1 , res2 , 1 , 0)
    output_file.write(final_output)

    cv2.imshow("Magic" , final_output)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()
