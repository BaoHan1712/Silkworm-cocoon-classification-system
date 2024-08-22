import cv2
from support.sort import Sort
from ultralytics import YOLO
from support.utils import brown_mask, yellow_mask, format_number
import math
import numpy as np
import serial
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk

# Kết nối với Arduino qua cổng serial
arduino = serial.Serial(port='COM4', baudrate=9600)
time.sleep(1)


# Hàm thực hiện xử lý video và đếm
def process_video():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    model = YOLO("model\ken60.onnx", task='detect')

    classnames = []
# Theo dõi màu
    tracked_colors = {}

    with open('class.txt', 'r') as f:
        classnames = f.read().splitlines()

    tracker = Sort(max_age=35)

    # Line
    line = [1, 300, 1080, 300]

    # Tính toán
    c_white = []
    c_brown = []
    c_yellow = []


    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        if not ret:
            break

        # Tạo mảng lưu thông tin đối tượng
        detections = np.empty((0, 5))

        result = model(frame, imgsz=640, conf = 0.6)

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

        # Theo dõi các đối tượng
        for results in track_result:
            x1, y1, x2, y2, id = results
            x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)

            w, h = x2 - x1, y2 - y1
            cx, cy = x1 + w // 2, y1 + h // 2

            cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)
            # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if y1 < y2 and x1 < x2:
                roi = frame[y1:y2, x1:x2]
                if roi.size > 0:
                    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                    mask_brown = brown_mask(hsv)   
                    mask_yellow = yellow_mask(hsv)

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
                    
                    elif color == 'yellow':
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        
                    elif color == 'white':
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    if line[0] < cx < line[2] and line[1] - 20 < cy < line[1] + 20:
                        cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 5)

                        # Bạn có thể thay đổi đối tượng tùy ý
                        if objectdetect == 'ken':
                            if c_brown.count(id) == 0 and color == 'brown':
                                c_brown.append(id)
                                arduino.write('1'.encode()) 
                                time.sleep(0.1)
                                count_brown.set(count_brown.get() + 1)
                                update_labels()

                            if c_yellow.count(id) == 0 and color == 'yellow':
                                c_yellow.append(id)
                                arduino.write('2'.encode())
                                time.sleep(0.1)
                                count_yellow.set(count_yellow.get() + 1)
                                update_labels()

                            if c_white.count(id) == 0 and color == 'white': 
                                c_white.append(id)
                                count_white.set(count_white.get() + 1)
                                update_labels()

            cv2.putText(frame, f'{id} {objectdetect}', (x1 + 8, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("bao objects", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
#___________________________________________________________GIAO DIỆN_______________________________________________________________________

def reset_counters():
    count_brown.set(0)
    count_yellow.set(0)
    count_white.set(0)
    update_labels()

# Hàm cập nhật nhãn đếm
def update_labels():
    label_brown.config(text=f"Đếm Brown: {count_brown.get()}")
    label_yellow.config(text=f"Đếm Yellow: {count_yellow.get()}")
    label_white.config(text=f"Đếm White: {count_white.get()}")

# Hàm tính thành tiền
def calculate_amount():
    try:
        # Lấy giá trị đã loại bỏ dấu phẩy để tính toán
        kg = float(entry_kg_var.get().replace(',', ''))
        price_brown = float(entry_price_brown_var.get().replace(',', ''))
        price_yellow = float(entry_price_yellow_var.get().replace(',', ''))
        price_white = float(entry_price_white_var.get().replace(',', ''))

        total = count_brown.get() + count_yellow.get() + count_white.get()

        if total > 0:
            percent_brown = count_brown.get() / total
            percent_yellow = count_yellow.get() / total
            percent_white = count_white.get() / total

            amount_brown = percent_brown * kg * price_brown
            amount_yellow = percent_yellow * kg * price_yellow
            amount_white = percent_white * kg * price_white

            # Định dạng số với dấu phẩy và thêm 'VNĐ'
            label_amount_brown.config(text=f"Thành tiền Brown: {amount_brown:,.0f} VNĐ")
            label_amount_yellow.config(text=f"Thành tiền Yellow: {amount_yellow:,.0f} VNĐ")
            label_amount_white.config(text=f"Thành tiền White: {amount_white:,.0f} VNĐ")

            # Tính tổng số tiền của ba loại
            total_amount = amount_brown + amount_yellow + amount_white
            label_total_amount.config(text=f"Tổng thành tiền: {total_amount:,.0f} VNĐ")
        else:
            label_amount_brown.config(text="Thành tiền Brown: 0 VNĐ")
            label_amount_yellow.config(text="Thành tiền Yellow: 0 VNĐ")
            label_amount_white.config(text="Thành tiền White: 0 VNĐ")
            label_total_amount.config(text="Tổng thành tiền: 0 VNĐ")
    except ValueError:
        label_amount_brown.config(text="Lỗi: Vui lòng nhập đúng định dạng số")
        label_amount_yellow.config(text="Lỗi: Vui lòng nhập đúng định dạng số")
        label_amount_white.config(text="Lỗi: Vui lòng nhập đúng định dạng số")
        label_total_amount.config(text="Lỗi: Vui lòng nhập đúng định dạng số")

# Tạo cửa sổ Tkinter
root = tk.Tk()
root.title("Bảng đếm và thành tiền")
root.configure(bg='#add8e6')

# Khởi tạo các biến đếm
count_brown = tk.IntVar()
count_yellow = tk.IntVar()
count_white = tk.IntVar()

# Tạo các nhãn hiển thị đếm
label_brown = tk.Label(root, text="Đếm Brown: 0", bg='#add8e6', font=("Helvetica", 12))
label_yellow = tk.Label(root, text="Đếm Yellow: 0", bg='#add8e6', font=("Helvetica", 12))
label_white = tk.Label(root, text="Đếm White: 0", bg='#add8e6', font=("Helvetica", 12))

label_brown.grid(row=1, column=0, padx=20, pady=5)
label_yellow.grid(row=2, column=0, padx=20, pady=5)
label_white.grid(row=3, column=0, padx=20, pady=5)

# Tạo nút đặt lại
reset_button = tk.Button(root, text="Đặt lại", command=reset_counters)
reset_button.grid(row=8, column=0, padx=20, pady=20)

# Tạo các biến StringVar cho các Entry
entry_kg_var = tk.StringVar()
entry_price_brown_var = tk.StringVar()
entry_price_yellow_var = tk.StringVar()
entry_price_white_var = tk.StringVar()

# Nhãn kg
label_kg = tk.Label(root, text="Nhập Số kg:", bg='#add8e6', font=("Helvetica", 12))
label_kg.grid(row=4, column=0, padx=20, pady=5)

# Ô nhập số kg
entry_kg = tk.Entry(root, textvariable=entry_kg_var)
entry_kg.grid(row=4, column=2, padx=20, pady=5)
entry_kg.bind('<FocusOut>', lambda e: format_number(e, entry_kg_var))

# Vị trí gia tiền nâu
label_price_brown = tk.Label(root, text="Nhập Giá Brown:", bg='#add8e6', font=("Helvetica", 12))
label_price_brown.grid(row=5, column=0, padx=20, pady=5)
entry_price_brown = tk.Entry(root, textvariable=entry_price_brown_var)
entry_price_brown.grid(row=5, column=2, padx=20, pady=5)
entry_price_brown.bind('<FocusOut>', lambda e: format_number(e, entry_price_brown_var))

# Vị trí vàng
label_price_yellow = tk.Label(root, text="Nhập Giá Yellow:", bg='#add8e6', font=("Helvetica", 12))
label_price_yellow.grid(row=6, column=0, padx=20, pady=5)
entry_price_yellow = tk.Entry(root, textvariable=entry_price_yellow_var)
entry_price_yellow.grid(row=6, column=2, padx=20, pady=5)
entry_price_yellow.bind('<FocusOut>', lambda e: format_number(e, entry_price_yellow_var))

# Vị trí trắng
label_price_white = tk.Label(root, text="Nhập Giá White:", bg='#add8e6', font=("Helvetica", 12))
label_price_white.grid(row=7, column=0, padx=20, pady=5)
entry_price_white = tk.Entry(root, textvariable=entry_price_white_var)
entry_price_white.grid(row=7, column=2, padx=20, pady=5)
entry_price_white.bind('<FocusOut>', lambda e: format_number(e, entry_price_white_var))

# Nút tính tiền
calculate_button = tk.Button(root, text="Tính tiền", command=calculate_amount)
calculate_button.grid(row=8, column=2, columnspan=2, padx=20, pady=20)

# Các nhãn hiển thị thành tiền
label_amount_brown = tk.Label(root, text="Thành tiền Brown: 0", bg='#add8e6', font=("Helvetica", 12))
label_amount_brown.grid(row=9, column=0, columnspan=3, padx=20, pady=5)

label_amount_yellow = tk.Label(root, text="Thành tiền Yellow: 0", bg='#add8e6', font=("Helvetica", 12))
label_amount_yellow.grid(row=10, column=0, columnspan=3, padx=20, pady=5)

label_amount_white = tk.Label(root, text="Thành tiền White: 0", bg='#add8e6', font=("Helvetica", 12))
label_amount_white.grid(row=11, column=0, columnspan=3, padx=20, pady=5)

# Tổng số tiền 
label_total_amount = tk.Label(root, text="Tổng thành tiền: 0 VNĐ", bg='#add8e6', font=("Helvetica", 12))
label_total_amount.grid(row=12, column=0, columnspan=3, padx=10, pady=5)

# Load và hiển thị ảnh st.png và logo lạc hồng
image = Image.open("images\st.png")
image = image.resize((100, 100), Image.Resampling.LANCZOS)  
photo = ImageTk.PhotoImage(image)

image1 = Image.open("images\lachong.png")
image1 = image1.resize((100, 100), Image.Resampling.LANCZOS)  
photo1 = ImageTk.PhotoImage(image1)

#Nơi ảnh xuất hiện
label_image = tk.Label(root, image=photo, bg='#add8e6')
label_image.grid(row=0, column=2, padx=5, pady=5)

label_image1 = tk.Label(root, image=photo1, bg='#add8e6')
label_image1.grid(row=0, column=0, padx=5, pady=5)

# Khởi động luồng xử lý video
video_thread = threading.Thread(target=process_video)
video_thread.daemon = True
video_thread.start()

# Bắt đầu vòng lặp Tkinter
root.mainloop()
