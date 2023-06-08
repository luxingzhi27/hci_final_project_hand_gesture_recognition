import time
import cv2 as cv
from HandLandmarks import handLandmarks
from GestureRecognition import gestureRecognition, staticGestureRec
from GestureRecognition import gestureRecognition, staticGestureRec

commands = {1: "OK",
            2: "thumb",
            3: "fist",
            4: "middle",
            5: "spider",
            6: "heart",
            7: "hand",
            8: "right",
            9: "left",
            10: "index",
            11: "ring",
            12: "little"}


def testGestureRecognition():  # 播放影片
    video = cv.VideoCapture(0)

    # fps统计
    cTime = 0
    pTime = 0

    # 摄像头参数设置
    wCap, hCap = 640, 480
    # wCap, hCap = 1280, 720
    video.set(3, wCap)
    video.set(4, hCap)

    # 帧差重心
    preCenter = [wCap / 2, hCap / 2]
    curCenter = [0, 0]

    while True:

        ret, frame = video.read()
        frame = cv.flip(frame, 1)
        if ret:
            # 手部关键点检测
            landmarks = handLandmarks(frame)
            command = 0
            if not isinstance(landmarks, str):
                # 手势命令识别
                curCenter, command = gestureRecognition(
                    frame, landmarks, preCenter)
                preCenter = curCenter

            # 帧率统计
            cTime = time.time()  # 现在的时间
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv.putText(frame, "fps"+str(int(fps)), (20, 50),
                       cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), thickness=2)
            if command != 0:
                cv.putText(frame, commands[command], (400, 50),
                           cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), thickness=2)
            cv.imshow('frame', frame)

            if cv.waitKey(1) == 27:
                break

    video.release()


if __name__ == '__main__':
    testGestureRecognition()
