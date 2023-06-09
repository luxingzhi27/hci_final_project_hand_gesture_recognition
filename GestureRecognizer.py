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


class GestureRecognizer:
    def __init__(self, wCap=640, hCap=480) -> None:
        self.commands = {1: "OK",
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
        self.command = 0
        self.wCap, self.hCap = wCap, hCap
        self.video = cv.VideoCapture(0)
        self.frame = None

    def testGestureRecognition(self):

        # fps统计
        cTime = 0
        pTime = 0

        # 摄像头参数设置
        wCap, hCap = 640, 480
        # wCap, hCap = 1280, 720
        self.video.set(3, wCap)
        self.video.set(4, hCap)

        # 帧差重心
        preCenter = [wCap / 2, hCap / 2]
        curCenter = [0, 0]

        while True:

            ret, self.frame = self.video.read()
            self.frame = cv.flip(self.frame, 1)
            if ret:
                # 手部关键点检测
                landmarks = handLandmarks(self.frame)
                command = 0
                if not isinstance(landmarks, str):
                    # 手势命令识别
                    curCenter, command = gestureRecognition(
                        self.frame, landmarks, preCenter)
                    preCenter = curCenter

                # 帧率统计
                cTime = time.time()  # 现在的时间
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv.putText(self.frame, "fps"+str(int(fps)), (20, 50),
                           cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), thickness=2)
                if command != 0:
                    cv.putText(self.frame, self.commands[command], (400, 50),
                               cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), thickness=2)
                cv.imshow('frame', self.frame)

                if cv.waitKey(1) == 27:
                    break

        self.video.release()


if __name__ == '__main__':
    gestureRecognizer = GestureRecognizer()
    gestureRecognizer.testGestureRecognition()
