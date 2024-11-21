import cv2
import numpy as np


def create_color_mask(hsv, lower_color, upper_color):
    return cv2.inRange(hsv, lower_color, upper_color)

<<<<<<< HEAD
# Hàm tính trung bình độ sáng của vùng ROI
def calculate_brightness(hsv_roi):
    return np.mean(hsv_roi[:, :, 2])

# Hàm tự động điều chỉnh ngưỡng màu nâu dựa trên độ sáng
def adjust_brown_threshold(brightness):
    if brightness < 50:  # Ánh sáng yếu
        lower_brown = np.array([0, 100, 30], dtype=np.uint8)
        upper_brown = np.array([60, 255, 140], dtype=np.uint8)
    elif brightness > 200:  # Ánh sáng mạnh
        lower_brown = np.array([0, 130, 80], dtype=np.uint8)
        upper_brown = np.array([60, 255, 200], dtype=np.uint8)
    else:  # Ánh sáng trung bình
        lower_brown = np.array([0, 120, 50], dtype=np.uint8)
        upper_brown = np.array([60, 255, 160], dtype=np.uint8)
    
    return lower_brown, upper_brown


def auto_brown_mask(hsv_roi):
    brightness = calculate_brightness(hsv_roi)
    lower_brown, upper_brown = adjust_brown_threshold(brightness)
    return cv2.inRange(hsv_roi, lower_brown, upper_brown)
=======
>>>>>>> a4f7f890a220c2bf2ed4fdffcf31685bfd3930d2

def brown_mask(hsv):
    lower_brown = np.array([0, 120, 50], dtype=np.uint8)
    upper_brown = np.array([60, 255, 160], dtype=np.uint8)
    return create_color_mask(hsv, lower_brown, upper_brown)


def yellow_mask(hsv):
    lower_yellow = np.array([7, 7, 128], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)
    return create_color_mask(hsv, lower_yellow, upper_yellow)

# Hàm dấu phẩy
def format_number(event, entry_var):
    try:
        value = entry_var.get().replace(',', '')
        formatted_value = f"{float(value):,.0f}"
        # Cập nhật lại Entry với giá trị đã định dạng
        entry_var.set(formatted_value)
    except ValueError:
        entry_var.set('')

<<<<<<< HEAD
#Tính toán độ sáng của frame        
def calculate_frame_brightness(frame):
    # Chuyển frame sang không gian màu LAB
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    # Tách kênh L (độ sáng)
    l_channel = lab[:,:,0]
    # Tính trung bình độ sáng
    brightness = np.mean(l_channel)
    return brightness

=======
>>>>>>> a4f7f890a220c2bf2ed4fdffcf31685bfd3930d2


