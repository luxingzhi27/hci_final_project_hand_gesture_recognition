import typing
from PyQt5 import QtCore, QtGui
from picture_viewer_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QMessageBox, QWidget, QLabel, QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import QPixmap, QImage, QIcon,QColor
from PyQt5.QtCore import QItemSelection
import os
import threading
import cv2 as cv
from HandLandmarks import handLandmarks
from GestureRecognition import gestureRecognition, staticGestureRec
from GestureRecognition import gestureRecognition, staticGestureRec
import time
import shutil

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


class pictureViewer(Ui_MainWindow, QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.currentPictureList = []
        self.currentIndex = 0
        self.sideBarAction.setChecked(False)
        self.sideBarCheckBox.setChecked(False)
        self.cameraViewAction.setChecked(False)
        self.cameraViewCheckBox.setChecked(False)
        self.sideBarAction.triggered.connect(self.onSideBarAction)
        self.sideBarCheckBox.stateChanged.connect(self.onSideBarCheckBox)
        self.cameraViewAction.triggered.connect(self.onCameraViewAction)
        self.cameraViewCheckBox.stateChanged.connect(self.onCameraViewCheckBox)
        self.openDirButton.clicked.connect(self.openDir)
        self.importFileButton.clicked.connect(self.importPicture)
        self.dislikeButton.clicked.connect(self.dislike)
        self.likeButton.clicked.connect(self.like)
        self.openDirAction.triggered.connect(self.openDir)
        self.importFileAction.triggered.connect(self.importPicture)
        self.nextButton.clicked.connect(self.next)
        self.lastButton.clicked.connect(self.pre)
        self.pictureListWidget.itemClicked.connect(
            self.onPictureListWidgetItemClicked)
        self.mainPictureView.resizeEvent = self.onMainPictureViewResizeEvent
        self.dirPath = None
        self.done = False
        self.cameraViewIsHide = False
        self.initLoadPicture()
        threading.Thread(target=self.showCameraView).start()

    def addItem(self, name):
        item = QListWidgetItem()
        # widget = QWidget()
        # layout = QHBoxLayout()
        # widget.setLayout(layout)
        # fileName = QLabel(name)
        # layout.addWidget(fileName)
        # item.setSizeHint(widget.sizeHint())
        item.setText(name)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setIcon(QIcon(os.path.join(self.dirPath,name)))
        self.pictureListWidget.addItem(item)
        # self.pictureListWidget.setItemWidget(item, widget)

    def next(self):
        if self.currentIndex < self.pictureListWidget.count()-1:
            self.currentIndex += 1
            self.pictureListWidget.setCurrentRow(self.currentIndex)
            picturePath = os.path.join(
                self.dirPath, self.currentPictureList[self.currentIndex])
            pixmap = QPixmap(picturePath)
            size = self.mainPictureView.size()
            pixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
            self.mainPictureView.setPixmap(pixmap)

    def pre(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.pictureListWidget.setCurrentRow(self.currentIndex)
            picturePath = os.path.join(
                self.dirPath, self.currentPictureList[self.currentIndex])
            pixmap = QPixmap(picturePath)
            size = self.mainPictureView.size()
            pixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
            self.mainPictureView.setPixmap(pixmap)

    def initLoadPicture(self):
        self.pictureListWidget.clear()
        self.currentPictureList = []
        self.dirPath = os.path.join(os.getcwd(), 'picture')
        for path in os.listdir(self.dirPath):
            if path.endswith('jpg') or path.endswith('png'):
                self.addItem(path)
                self.currentPictureList.append(path)
        self.currentIndex = 0
        self.pictureListWidget.setCurrentRow(self.currentIndex)
        picturePath = os.path.join(
            self.dirPath, self.currentPictureList[self.currentIndex])
        pixmap = QPixmap(picturePath)
        size = self.mainPictureView.size()
        pixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
        self.mainPictureView.setPixmap(pixmap)

    def showCameraView(self):
        # fps统计
        video = cv.VideoCapture(0)
        cTime = 0
        pTime = 0

        flipCTime = 3
        flipPTime = 0

        command = 0
        precommand = 0
        # 摄像头参数设置
        wCap, hCap = 480, 360
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
                    cv.putText(frame, commands[command], (170, 50),
                               cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), thickness=2)
                if command != 0 and self.pictureListWidget.count() > 0 and precommand != command:

                    precommand = command

                    if command in [8, 9]:
                        flipCTime = time.time()
                        if flipCTime-flipPTime > 1.5:
                            if command == 8:
                                if self.currentIndex > 0:
                                    self.currentIndex -= 1
                            elif command == 9:
                                if self.currentIndex < self.pictureListWidget.count()-1:
                                    self.currentIndex += 1
                            print("switch")
                            self.pictureListWidget.setCurrentRow(
                                self.currentIndex)
                            picturePath = os.path.join(
                                self.dirPath, self.currentPictureList[self.currentIndex])
                            pixmap = QPixmap(picturePath)
                            size = self.mainPictureView.size()
                            pixmap = pixmap.scaled(
                                size, QtCore.Qt.KeepAspectRatio)
                            self.mainPictureView.setPixmap(pixmap)
                        flipPTime = flipCTime

                    elif command == 6:
                        print("like")
                        self.like()

                    elif command == 5 or command == 12:
                        print("dislike")
                        self.dislike()

                if not self.cameraViewIsHide:
                    QtImgBuf = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
                    QtImg = QImage(
                        QtImgBuf.data, QtImgBuf.shape[1], QtImgBuf.shape[0], QImage.Format_RGB32)
                    self.cameraView.setPixmap(QPixmap.fromImage(QtImg))
                    size = QtImg.size()
                    self.cameraView.resize(size)
                if self.done:
                    break

        video.release()

    def dislike(self):
        self.pictureListWidget.setFocus()
        self.pictureListWidget.currentItem().setForeground(QColor(0, 0, 0))
        self.pictureListWidget.clearFocus()
        self.mainPictureView.setFocus()

    def like(self):
        self.pictureListWidget.setFocus()
        self.pictureListWidget.currentItem().setForeground(QColor(255, 0, 0))
        self.pictureListWidget.clearFocus()
        self.mainPictureView.setFocus()

    def openDir(self):
        self.dirPath = QFileDialog.getExistingDirectory(self, '选择文件夹', './')
        if self.dirPath:
            self.pictureListWidget.clear()
            self.currentPictureList = []
            print(self.dirPath)
            for path in os.listdir(self.dirPath):
                if path.endswith('jpg') or path.endswith('png'):
                    self.addItem(path)
                    self.currentPictureList.append(path)
            self.pictureListWidget.repaint()

    def importPicture(self):
        if self.dirPath:
            picturePath = QFileDialog.getOpenFileName(
                self, '选择图片', self.dirPath, 'Image files(*.jpg *.png)')
        else:
            picturePath = QFileDialog.getOpenFileName(
                self, '选择图片', './', 'Image files(*.jpg *.png)')
        if not picturePath[0]:
            return

        fileName = picturePath[0]
        newFileName = os.path.basename(fileName)
        newFilePath = os.path.join(
            self.dirPath, newFileName)

        if not os.path.exists(newFilePath):
            shutil.copy2(fileName, newFilePath)
            self.addItem(newFileName)
            self.currentPictureList.append(newFileName)
            self.pictureListWidget.repaint()
        else:
            QMessageBox.information(self, '提示', '文件已存在')

    def onPictureListWidgetItemClicked(self, item):
        self.currentIndex = self.pictureListWidget.currentRow()
        pixmap = QPixmap(os.path.join(
            self.dirPath, self.currentPictureList[self.currentIndex]))
        size = self.mainPictureView.size()
        pixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
        self.mainPictureView.setPixmap(pixmap)

    def onMainPictureViewResizeEvent(self, event):
        pixmap = self.mainPictureView.pixmap()
        if pixmap:
            size = self.mainPictureView.size()
            pixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
            self.mainPictureView.setPixmap(pixmap)

    def onSideBarCheckBox(self):
        if self.sideBarCheckBox.isChecked():
            self.sideBarAction.setChecked(True)
            self.pictureListWidget.hide()
        else:
            self.sideBarAction.setChecked(False)
            self.pictureListWidget.show()

    def onCameraViewCheckBox(self):
        if self.cameraViewCheckBox.isChecked():
            self.cameraViewAction.setChecked(True)
            self.cameraView.hide()
            self.cameraViewIsHide = True
            self.cameraView.resize(0, 0)
            self.adjustSize()
        else:
            self.cameraViewAction.setChecked(False)
            self.cameraView.show()
            self.cameraViewIsHide = False

    def onSideBarAction(self):
        if self.sideBarAction.isChecked():
            self.sideBarCheckBox.setChecked(True)
            self.pictureListWidget.hide()
        else:
            self.sideBarCheckBox.setChecked(False)
            self.pictureListWidget.show()

    def onCameraViewAction(self):
        if self.cameraViewAction.isChecked():
            self.cameraViewCheckBox.setChecked(True)
            self.cameraView.hide()
            self.cameraViewIsHide = True
            self.cameraView.resize(0, 0)
            self.adjustSize()
        else:
            self.cameraViewCheckBox.setChecked(False)
            self.cameraView.show()
            self.cameraViewIsHide = False

    def closeEvent(self, event) -> None:
        super().closeEvent(event)
        self.done = True


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = pictureViewer()
    mainWindow.show()
    sys.exit(app.exec_())
