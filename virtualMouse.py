# if changing devices

# python 3.7.9 or lower
# add python 2 as a virtual environment
# install mediapipe(V 0.8.8)
# install openCV-python
# install autopy (need python 3.7.9 or lower)


import cv2
import time
import numpy as np
import autopy
import HandTrackingModule as htm
from time import sleep
import pyautogui
pyautogui.FAILSAFE = False

# Dimensions of camera window
camW = 640
camH = 480

# FPS variables
pTime = 0
cTime = 0

# Start Camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, camW)
cap.set(4, camH)

scrW, scrH = autopy.screen.size()
# print(scrW, scrH)

# Pink box size
frameR = 120

# mouse motion smoothening variable
smoothen = 6

plocX, plocY = 0, 0
clocX, clocY = 0, 0

detector = htm.handDetector(maxHands=1)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    img = cv2.flip(img, 1)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        # print(fingers)

        cv2.rectangle(img, (frameR, frameR), (camW - frameR, camH - frameR), (255, 0, 255), 2)

        # if fingers[1] == 1 and fingers[2] == 0:

        x3 = np.interp(x1, (frameR, camW - frameR), (0, scrW))
        y3 = np.interp(y1, (frameR, camH - frameR), (0, scrH))

        # to smoothen mouse movement
        clocX = plocX + (x3 - plocX) / smoothen
        clocY = plocY + (y3 - plocY) / smoothen

        autopy.mouse.move(scrW - clocX, clocY)

        plocX, plocY = clocX, clocY

        # finding length between 2 points
        length, img, _ = detector.findDistance(4, 5, img)
        # print(length)

        if length < 30:
        #   autopy.mouse.click()
            pyautogui.click()







    # FPS Display
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
