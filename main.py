import cv2
from support.sort import Sort
from ultralytics import YOLO
from support.utils import  auto_yellow_mask, auto_brown_mask
import math
import numpy as np
import time  # Thêm thư viện time để đo thời gian


cap = cv2.VideoCapture("images\den.MOV")

model = YOLO("model\ken_final.engine", task='detect')

classnames = ['ken']

tracker = Sort(max_age=50)

# Line
line = [1, 300, 1080, 300]
    
#calculator
c_white = []
c_brown = []
c_yellow = []

tracked_colors = {}

# Đo thời gian bắt đầu
prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame =cv2.resize(frame,(1080,720))
    
    # Tính toán FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Tạo mảng lưu trữ thông tin phát hiện
    detections = np.empty((0, 5))
    
    result = model(frame, imgsz=640, conf=0.6)
    
    for info in result:
        boxes = info.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            conf = box.conf[0]
            classindex = box.cls[0]
            conf = math.ceil(conf * 100)
            classindex = int(classindex)
            objectdetect = classnames[classindex]

            if conf > 60:
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                new_detections = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, new_detections))

    track_result = tracker.update(detections)
    
    cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (0, 255, 0), 5)
    
    # Object tracking 
    for results in track_result:
        x1, y1, x2, y2, id = results
        x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)

        w, h = x2 - x1, y2 - y1
        cx, cy = x1 + w // 2, y1 + h // 2
        
        cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)
        
        if y1 < y2 and x1 < x2:
            roi = frame[y1:y2, x1:x2]
            if roi.size > 0:
                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                
                mask_brown = auto_brown_mask(hsv)   
                mask_yellow = auto_yellow_mask(hsv)

                if id not in tracked_colors:
                    if cv2.countNonZero(mask_brown) > 0:
                        tracked_colors[id] = 'brown'
                    elif cv2.countNonZero(mask_yellow) > 0:
                        tracked_colors[id] = 'yellow'
                    elif cv2.countNonZero(mask_yellow) == 0 and cv2.countNonZero(mask_brown) == 0:
                        tracked_colors[id] = 'white'

                color = tracked_colors[id]

                if color == 'brown':
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, f'{id} ken chet', (x1 + 8, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2, cv2.LINE_AA)
                
                elif color == 'yellow':
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(frame, f'{id} ken vang', (x1 + 8, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2, cv2.LINE_AA)

                elif color == 'white':
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'{id} ken trang', (x1 + 8, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2, cv2.LINE_AA)
                    
                if line[0] < cx < line[2] and line[1] - 20 < cy < line[1] + 20:
                    cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 5)

                # you can change car to everything you want  
                if objectdetect == 'ken':
                    # counting brown
                    if c_brown.count(id) == 0 and color == 'brown':
                        c_brown.append(id)

                    # counting yellow
                    if c_yellow.count(id) == 0 and color == 'yellow':
                        c_yellow.append(id)

                    # counting white
                    if c_white.count(id) == 0 and color == 'white': 
                        c_white.append(id)
    
    cv2.putText(frame, f'anh sang', (x1 + 3, y1 - 3), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2, cv2.LINE_AA)
                    
    cv2.putText(frame, f'brown = {len(c_brown)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, f'yellow= {len(c_yellow)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, f'white = {len(c_white)}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)

    # Hiển thị FPS trên video
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.imshow("bao objects", frame)
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
