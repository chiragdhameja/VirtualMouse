# if changing devices

# python 3.8
# install mediapipe
# install openCV-python
# install autopy
# install pyautogui
# install PyCaw


# import math
import cv2
import time
import numpy as np
import autopy
import HandTrackingModule as htm
# from time import sleep
import pyautogui
# import speech_recognition as speech
# from threading import *
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
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

# Pink box size
frameH = 80
frameH2 = 230
frameW = 120

# mouse motion smoothening variable
smoothen = 5

plocX, plocY = 0, 0
clocX, clocY = 0, 0

detector = htm.handDetector(maxHands=1)

lsingleClickFlag = False
rsingleClickFlag = False
dbsingleClickFlag = False

mouseHoldFlag = False



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()

minVol = int(volRange[0])
maxVol = int(volRange[1])

# sr = speech.Recognizer()
# print("Waiting for command...")

while True:

    # with speech.Microphone(device_index=2) as mic:
    #     t1 = Thread(target=audio.start)
    #
    #     audio = sr.listen(mic)
    #     query = sr.recognize_google(audio, language='eng-in')
    #     wake_up = "proton"
    #
    #     if wake_up in query:
    #         print("inside")
    #         wakeAudio = sr.listen(mic)
    #         command = sr.recognize_google(wakeAudio, language='eng-in')
    #
    #
    #         if 'start' in command:
    #             print(command)
    #             gc_mode = True
    #
    #         elif 'stop' in command:
    #             print(command)
    #             gc_mode = False


    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    img = cv2.flip(img, 1)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        #li = detector.findHands(img)[0]

        m1, n1 = lmList[5][1:]
        m2, n2 = lmList[17][1:]


        size = (n2 - n1) ** 2 + (m2 - m1) ** 2


        #print(size)

        cv2.rectangle(img, (frameW, frameH), (camW - frameW, camH - frameH2), (255, 0, 255), 2)

        x3 = np.interp(x1, (frameW, camW - frameW), (0, scrW))
        y3 = np.interp(y1, (frameH, camH - frameH2), (0, scrH))

        # to smoothen mouse movement
        clocX = plocX + (x3 - plocX) / smoothen
        clocY = plocY + (y3 - plocY) / smoothen

        autopy.mouse.move(scrW - clocX, clocY)
        #pyautogui.moveTo(scrW - clocX, clocY)

        plocX, plocY = clocX, clocY



        if size > 4500:
            point = 30
            lpoint = 35
            distance = "< 1m"
        elif size < 4500 and size > 2000:
            point = 15
            lpoint = 20
            distance = ">= 1m"
        elif size <= 2000:
            point = 10
            lpoint = 15
            distance = "> 2m"

        #print("distance is ", distance)

        # finding length between 2 points
        #for left-click
        lclklength, img, _ = detector.findDistance(4, 12, img)

        if lclklength < lpoint and lsingleClickFlag != True:
            lsingleClickFlag = True
            pyautogui.click()

        elif lclklength > lpoint:
            lsingleClickFlag = False


        #for right-click
        rclklength, img, _ = detector.findDistance(4, 16, img)

        if rclklength < point and rsingleClickFlag != True:
            rsingleClickFlag = True
            pyautogui.rightClick()

        elif rclklength > point:
            rsingleClickFlag = False

        # for double-click
        dbclklength, img, _ = detector.findDistance(4, 20, img)

        if dbclklength < point and dbsingleClickFlag != True:
            dbsingleClickFlag = True
            pyautogui.doubleClick()

        elif dbclklength > point:
            dbsingleClickFlag = False

        if lmList[8][2] > lmList[5][2] and lmList[12][2] > lmList[9][2] and lmList[16][2] > lmList[13][2] and lmList[20][2] > lmList[17][2] and lmList[4][2] < lmList[1][2]:

            # hand range = 250, 80
            # vol range = -64, 0

            lmList[4][2]
            handRange = [80, 250]
            cvtVol = [maxVol, minVol]

            volLength = lmList[4][2]
            vol = np.interp(volLength, handRange, cvtVol)
            #print(vol)
            volume.SetMasterVolumeLevel(vol, None)
            actVol = [0,100]
            actVol1 = np.interp(vol, cvtVol, actVol)
            #print("Volume is: ",actVol1)

        # if lmList[8][2] > lmList[0][2]:
        #     break





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
