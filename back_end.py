from flask import Flask, render_template, Response, jsonify, request
import cv2
from support.sort import *
import math
import numpy as np
from ultralytics import YOLO



app = Flask(__name__)

# Use camera
cap = cv2.VideoCapture(1)  
model = YOLO('model/silk.onnx')
classnames = []
with open('class.txt', 'r') as f:
    classnames = f.read().splitlines()

# Line
tracker = Sort(max_age=30)
line = [1, 300, 1080, 300]
    
#calculator
c_white = []
c_brown = []
c_yellow = []

def generate_frames():
    global c_white, c_brown, c_yellow
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame,(640,480))
        if not ret:
            break
        
        detections = np.empty((0, 5))
        
        result = model(frame,imgsz = 320)
        
        for info in result:
            boxes = info.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]
                classindex = box.cls[0]
                conf = math.ceil(conf * 100)
                classindex = int(classindex)
                objectdetect = classnames[classindex]

                if conf > 50:
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    new_detections = np.array([x1, y1, x2, y2, conf])
                    detections = np.vstack((detections, new_detections))

        track_result = tracker.update(detections)
        
        cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (0, 255, 0), 5)

        for results in track_result:
            x1, y1, x2, y2, id = results
            x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)

            w, h = x2 - x1, y2 - y1
            cx, cy = x1 + w // 2, y1 + h // 2

            cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if y1 < y2 and x1 < x2:
                roi = frame[y1:y2, x1:x2]
                if roi.size > 0:
                    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                    lower_brown = np.array([5, 75, 75], dtype=np.uint8)
                    upper_brown = np.array([20, 160, 160], dtype=np.uint8)
                    
                    lower_yellow = np.array([15, 120, 140], dtype=np.uint8)
                    upper_yellow = np.array([40, 255, 255], dtype=np.uint8)

                    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
                    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

                    if line[0] < cx < line[2] and line[1] - 20 < cy < line[1] + 20:
                        cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 5)

                    # you can change car to everthing you want
                        if objectdetect == 'normal':
                            # counting brown
                            if c_brown.count(id) == 0 and cv2.countNonZero(mask_brown) > 0:
                                c_brown.append(id)

                            # counting yellow
                            if c_yellow.count(id) == 0 and cv2.countNonZero(mask_yellow) > 0:
                                c_yellow.append(id)

                            # counting white
                            if c_white.count(id) == 0 and cv2.countNonZero(mask_yellow) == 0 and cv2.countNonZero(mask_brown) == 0: 
                                c_white.append(id)

        cv2.putText(frame, f'{id} {objectdetect}', (x1 + 8, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 2, cv2.LINE_AA)
                    

        # cv2.putText(frame, f'brown = {len(c_brown)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
        # cv2.putText(frame, f'yellow= {len(c_yellow)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
        # cv2.putText(frame, f'white = {len(c_white)}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)

        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('display.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_counts')
def get_counts():
    return jsonify({
        'brown': len(c_brown),
        'yellow': len(c_yellow),
        'white': len(c_white)
    })

@app.route('/reset_counts', methods=['POST'])
def reset_counts():
    global c_white, c_brown, c_yellow
    c_white = []
    c_brown = []
    c_yellow = []
    return jsonify({'success': True})

@app.route('/calculate_percentage', methods=['POST'])
def calculate_percentage():
    global c_white, c_brown, c_yellow
    data = request.json
    total_weight = data.get('weight', 0)

    # Ensure we don't divide by zero
    if total_weight <= 0:
        return jsonify({'error': 'Invalid weight'}), 400

    total_count = len(c_white) + len(c_brown) + len(c_yellow)
    
    if total_count == 0:
        return jsonify({
            'brown_percentage': 0,
            'yellow_percentage': 0,
            'white_percentage': 0,
            'brown_weight': 0,
            'yellow_weight': 0,
            'white_weight': 0
        })

    # Calculate percentages
    brown_percentage = (len(c_brown) / total_count) * 100
    yellow_percentage = (len(c_yellow) / total_count) * 100
    white_percentage = (len(c_white) / total_count) * 100

    # Calculate weight distribution based on percentages
    brown_weight = (brown_percentage / 100) * total_weight
    yellow_weight = (yellow_percentage / 100) * total_weight
    white_weight = (white_percentage / 100) * total_weight

    return jsonify({
        'brown_percentage': brown_percentage,
        'yellow_percentage': yellow_percentage,
        'white_percentage': white_percentage,
        'brown_weight': brown_weight,
        'yellow_weight': yellow_weight,
        'white_weight': white_weight
    })
    
@app.route('/calculate_price', methods=['POST'])
def calculate_price():
    global c_white, c_brown, c_yellow
    data = request.json
    total_weight = data.get('weight', 0)
    price_brown = data.get('price_brown', 0)
    price_yellow = data.get('price_yellow', 0)
    price_white = data.get('price_white', 0)

    # Ensure we don't divide by zero
    if total_weight <= 0:
        return jsonify({'error': 'Invalid weight'}), 400

    total_count = len(c_white) + len(c_brown) + len(c_yellow)
    
    if total_count == 0:
        return jsonify({
            'brown_price': 0,
            'yellow_price': 0,
            'white_price': 0,
            'total_price': 0
        })

    # Calculate percentages
    brown_percentage = (len(c_brown) / total_count) * 100
    yellow_percentage = (len(c_yellow) / total_count) * 100
    white_percentage = (len(c_white) / total_count) * 100

    # Calculate weight distribution based on percentages
    brown_weight = (brown_percentage / 100) * total_weight
    yellow_weight = (yellow_percentage / 100) * total_weight
    white_weight = (white_percentage / 100) * total_weight

    # Calculate price 
    brown_price = int(brown_weight * price_brown)
    yellow_price = int(yellow_weight * price_yellow)
    white_price = int(white_weight * price_white)

    total_price = brown_price + yellow_price + white_price

    return jsonify({
        'brown_price': brown_price,
        'yellow_price': yellow_price,
        'white_price': white_price,
        'total_price': total_price
    })
    
if __name__ == '__main__':
    app.run(debug=True) 