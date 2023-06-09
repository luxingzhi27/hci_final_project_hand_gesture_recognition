from fingersVector import fingersUp, vectorSize, vectorAngle, mkVector, vectorAngle2
import cv2 as cv


def staticGestureRec(landmark):
    command = 0
    fingers = fingersUp(landmark)
    if (fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1):
        command = 1
        # print("OK")
    if (fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0):
        command = 2
        # print("大拇指")
    if (fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0):
        command = 10
        # print("食指")

    if (fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 1 and fingers[4] == 0):
        command = 11
        # print("无名指")

    if (fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1):
        command = 12
        # print("小拇指")

    if (fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0):
        command = 3
        # print("拳头")

    if (fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0):
        command = 4
        # print("中指")

    if (fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1):
        command = 5
        # print("spider")

    if (fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0
            and vectorSize(landmark[3], landmark[6]) < 20 and vectorAngle(landmark[4], landmark[6], landmark[8]) < 90):
        command = 6
        # print("比心")
    if (fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1):
        command = 7
        # print("手掌")
    return command


def gestureRecognition(frame, landmarks, preCenter):
    # 静态手势识别
    command = staticGestureRec(landmarks)

    # 动态手势识别
    curCenter = landmarks[9]
    cv.circle(frame, curCenter, 10, (0, 255, 255), -1)
    centerVector = mkVector(curCenter, preCenter)  # 构造帧差向量
    curPreSize = vectorSize(preCenter, curCenter)  # 控制手势帧差大小区域
    xAxis = [1, 0]
    angle = vectorAngle2(centerVector, xAxis)  # 控制手势帧差角度区域
    if centerVector[0] > 0 and curPreSize > 180 and angle < 30:
        command = 8
        print("right")

    if centerVector[0] < 0 and curPreSize > 180 and angle > 150:
        command = 9
        print("left")

    return curCenter, command
