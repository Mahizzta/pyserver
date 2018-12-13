
import sys
#Change the following line
sys.path.append('C:\Brugere\Kasper\Downloads\opencv\sources\samples\python')

import cv2

import socket
import time


UDP_IP = "127.0.0.1"
UDP_PORT = 5065

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
#print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
cam=cv2.VideoCapture(0)
last_recorded_time = time.time() # this keeps track of the last time a frame was processed


def shapedetect() :
    img2 = cv2.imread("shapes.jpg", cv2.IMREAD_GRAYSCALE)
    _, threshold = cv2.threshold(img2, 55, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    font = cv2.FONT_HERSHEY_COMPLEX
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        cv2.drawContours(img2, [approx], 0, (0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        M = cv2.moments(cnt)

        if len(approx) == 3:
            cv2.putText(img, "Triangle", (x, y), font, 1, (0))
            print("Found triangle")
            if (M["m00"] != 0):
                cX = float(M["m10"] / M["m00"])
                cY = float(M["m01"] / M["m00"])
                scX = str(cX)
                scY = str(cY)
                scXY = scX + ',' + scY
                sock.sendto(scXY.encode(), (UDP_IP, UDP_PORT))
                print(scXY)

        elif len(approx) > 6:
            cv2.putText(img, "Circle", (x, y), font, 1, (0))
            print("Found circle")
            if (M["m00"] != 0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                scX = str(cX)
                scY = str(cY)
                scXY = scX + ',' + scY
                sock.sendto(scXY.encode(), (UDP_IP, UDP_PORT))
                print(scXY)


        else:
            pass





    #cv2.imshow("shapes", img2)

while True:
    curr_time = time.time() # grab the current time

    # keep these three statements outside of the if statement, so we
    #     can still display the camera/video feed in real time
    suc, img=cam.read()
    #operation on image, it's not important


    if curr_time - last_recorded_time >= 2.0: # it has been at least 2 seconds
        # NOTE: ADD SOME STATEMENTS HERE TO PROCESS YOUR IMAGE VARIABLE, img
        cv2.imwrite("shapes.jpg", img)
        # IMPORTANT CODE BELOW
        last_recorded_time = curr_time
        shapedetect()


