import cv2
import time
import numpy as np
# importing our self based Hand tracking module
import HandTrackingModule as htm
import math

# width and height of camera frame to be displayed
wCam, hCam = 1170, 430

# cTime is current time and pTime is previous time (used for calculating fps later)
cTime = 0
pTime = 0

# capturing video from webcam number 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# creating an object of class handDetector (from htm module)
detector = htm.handDetector(detectionCon=0.7)

# -------------------------------------------------------------------------------------------
# importing the music functions from pycaw library
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# storing max and min volume values
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]



# ----------------------------------------------------------------------------------------------------------------------
# for any doubts in the functions called for the object of htm (i.e. detector), you can refer to its file HandTrackingModule.py
# doing operations on each frame captured till stop button is pressed
while True:
    success, img = cap.read()

    # called findHands function of detector variable (it will display boundaries and connections on hand)
    img = detector.findHands(img)

    # called findPosition function to store position of various 20 dimensions of hand in a list (named lmList),
    # and to get minimum and maximum width and height for rectangle outside hand
    lmList, bbox = detector.findPosition(img, draw=True)

    # if there is no hand in frame,then list is empty so don't proceed
    if len(lmList) != 0:

        # calculating area of box
        area = (bbox[2] - bbox[0])*(bbox[3] - bbox[1])

        # storing dimensions of the fingers by which we will change volume
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        # displaying a circle on the tip of both fingers and a line joining them for length
        cv2.circle(img, (x1, y1), 12, (88, 2, 194), cv2.FILLED)
        cv2.circle(img, (x2, y2), 12, (88, 2, 194), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (102, 55, 96), 2)

        # mid-point of images
        cx, cy = (x1 + x2)//2, (y1+y2)//2

        # calculating length between both required fingers
        length = math.hypot(x1-x2, y1-y2)
        print(area)
        # Normalizing lengths and checked for a give distance, length = 280, area = 70000 to compare ratios of length and area
        cmpLen = 190
        cmpArea = 140000

        # normalized length
        length = (210*area)/cmpArea
        print(length)

        # minimum length after which volume becomes 0 and will not decrease further even if length is decreased
        # drawing a dot to show we have reached minima volume
        if length < 140:
            cv2.circle(img, (cx, cy), 12, (16, 16, 18), cv2.FILLED)
            cv2.putText(img, "Muted", (10, 500), cv2.FONT_HERSHEY_PLAIN, 1.5, (18, 216, 250), 2)


        # --------------------------------------------------------------------------------------------------------------
        # Convert Volume
        # we will change only when we will get command from outside
        # so we will check for out little finger if it is down then no change else change on the basis of length
        # If little finger is down set volume

        # y coordinates of little finger's upper and lower part
        litUp = lmList[20][2]
        litdown = lmList[19][2]

        # change if command given inform of little finger shape
        if(litUp < litdown):
            # print(length)
            vol = np.interp(length, [140, 210], [minVol, maxVol])
            per = max(0, int(((vol + 35)/35)*100))
            text = 'Volume : ' + str(per) + '%'
            volume.SetMasterVolumeLevel(vol, None)
            cv2.putText(img, text, (10, 80), cv2.FONT_HERSHEY_PLAIN, 1.5, (233, 245, 7), 2)

    cv2.putText(img, "WELCOME CHAMP !!", (345,30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (7, 229, 245), 2)
    cv2.putText(img, "For best experience stay 1.5 feets away", (185,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (7, 29, 245), 2)


    cv2.imshow("Img", img)
    cv2.waitKey(1)

