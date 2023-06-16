# 基于手势识别的图像浏览器
- Your report should be written in English and contain the following contents:

- 1. A brief description about your program (including the structures and modules of the program);

- 

- 2. The implemented requirements;

- 

- 3. Advantages and disadvantages of your program;

- 

- 4. How to improve your program;

- 

| Program:Each feature(function) 7'; Origninality 4' | Report:1. (10'); 2. (5'); 3.(10'); 4. (5'); in English (2'); Clarity (3') |
| -------------------------------------------------- | ------------------------------------------------------------ |
|                                                    |                                                              |

## 1. Background

### 1.1Environment
compiler: Python3.7+

package needed: opencv-python, MediaPipe, PyQt5

### 1.2How to run

on the terminal, input `python picture_viewer.py` and enter

 ## 2. Description

### 2.1 Overview

This project realizes the album interaction based on Gesture recognition.

User can perform different operations on the album based on different gestures.

### 2.2 Structures

The following is the core structure of the code—–

F:.
│  fingersVector.py
│  GestureRecognition.py
│  HandLandmarks.py
│  picture_viewer.py
│  picture_viewer.ui
│  picture_viewer_ui.py
│  
├─picture
│  
└─resource        

The picture folder contains some default images.

The resource folder contains some interactive images.

### 2.3 Code Logic

1. We first achieved the ==localization of 21 bone points== in our fingers in `fingersVector.py`

2. We ==imaged the identified joint points== and generated a mark images in `HandLandmarks.py`
3. Then we ==set the different gestures== based on the recognized joint point images in `GestureRecognition.py`

Our gestures include: 

| Gestures | code                                                         |
| -------- | ------------------------------------------------------------ |
| OK       | fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 |
| 大拇指   | fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 |
| 食指     | fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 |
| 中指     | fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0 |
| 无名指   | fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 1 and fingers[4] == 0 |
| 小拇指   | fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1 |
| 拳头     | fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 |
| 手掌     | fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 |
| 比心     | fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0            and vectorSize(landmark[3], landmark[6]) < 20 and vectorAngle(landmark[4], landmark[6], landmark[8]) < 90 |
| spider   | fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1 |

4. Finally, we designed the interface window and called relevant functions in the window to realize our album interaction function in `picture_viewer.py`

Our interactive functions include the following points:

| gesture | interactive function |
| ------- | -------------------- |
|         |                      |



