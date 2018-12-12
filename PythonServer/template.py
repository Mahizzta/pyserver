import cv2
from matplotlib import pyplot as plt
import numpy as np

cap = cv2.VideoCapture(0)  # Webcam Capture

while (True):

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

    for i in range(3):
        template = cv2.imread('images/face.png', 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(gray, template, cv2.TM_SQDIFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        top_left = min_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(frame, top_left, bottom_right, 255, 1)
        cv2.putText(frame, 'Detected Face ID: ' + str(i), (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))
        print(str(top_left[0]) + ", " + str(top_left[1]-10))
      #  M = cv2.moments(i)
       # cX = int(M["m10"] / M["m00"])
       # cY = int(M["m01"] / M["m00"])
        print('cX' + ',' + 'cY')
    cv2.imshow('Test', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()