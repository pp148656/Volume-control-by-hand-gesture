import cv2
import mediapipe as mp
import time

# ----------------------------------------------------------------------------------------------------------------------
# handDetector class which contains all the functions required for hand processing
class handDetector():

    # self is a keyword which is used to access the variables inside the class

    # __init__ function is used for initialization of class's variables and must be declared first above all functions of that class
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    # draws connections between 20 landmarks of palm (can refer to mediapipe documentation for info about landmarks)
    def findHands(self, img, draw=True):

        # converting to RBG as it is required format for determination of hands' dimensions
        imgRBG = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRBG)

        # find landmarks and if they exist draw connections between them
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img


    # returns list of landmarks based on id, x, and y coordinates and a box for surrounding hand
    def findPosition(self, img, handNo=0, draw=True):

        # list for x and y coordinates of landmarks
        xList = []
        yList = []

        # list for bounding box boundaries
        bbox = []
        self.lmList = []

        # storing all infos about landmarks to be used later
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                xList.append(cx)
                yList.append(cy)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)

            bbox = xmin, ymin, xmax, ymax

            # drawing bounding box
            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1]- 20), (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)

            xmin = min(self.lmList[17])
            bbox = xmin, ymin, xmax, ymax
        return self.lmList, bbox


