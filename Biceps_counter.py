import numpy as np
import cv2
import mediapipe as mp
import time
import math

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
cap = cv2.VideoCapture("Resources/exercise5.mp4")
prevTime = 0
count = 0
dire = 0

while True:
    success, img = cap.read()
    h, w, c = img.shape

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    p = results.pose_landmarks
    # print(p)

    point = []

    for i, lm in enumerate(results.pose_landmarks.landmark):
        cx, cy = int(lm.x * w), int(lm.y * h)
        point.append([i, cx, cy])

    # print(point)
    if len(point) != 0:

        x1, y1 = point[11][1:]
        x2, y2 = point[13][1:]
        x3, y3 = point[15][1:]

        # print(angle1)

        """cv2.circle(img, (x1, y1), 30, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 30, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 20)
        cv2.circle(img, (x3, y3), 30, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (x2, y2), (x3, y3), (0, 0, 0), 20)"""
        angle = math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
        angle1 = math.degrees(angle)
        # print(angle1)

        per = int(np.interp(angle1, (-50, 300), (0, 100)))
        # print(per,angle1)

        # Check dumbbell curls
        if 80 <= per <= 95:
            if dire == 0:
                count += 0.5
                dire = 1
        if per <= 10:
            if dire == 1:
                count += 0.5
                dire = 0
        # print(count)

    new_h = h // 5
    new_w = w // 5
    resizeImg = cv2.resize(img, (new_w, new_h))
    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime

    # cv2.putText(resizeImg, str(int(fps)), (60, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 4)
    cv2.putText(resizeImg, "Biceps", (60, 190), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 8)
    cv2.putText(resizeImg, str(int(count)), (160, 240), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 6)

    cv2.imshow("Video", resizeImg)
    cv2.waitKey(1)
