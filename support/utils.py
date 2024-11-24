import cv2
import numpy as np


def create_color_mask(hsv, lower_color, upper_color):
    return cv2.inRange(hsv, lower_color, upper_color)

# Hàm tính trung bình độ sáng của vùng ROI
def calculate_brightness(hsv_roi):
    bright = np.mean(hsv_roi[:, :, 2])
    # print("anh sang", bright)
    return bright

# Hàm tự động điều chỉnh ngưỡng màu nâu dựa trên độ sáng
def adjust_brown_threshold(brightness):
    if brightness <= 50:  # Ánh sáng yếu
        lower_brown = np.array([0, 100, 30], dtype=np.uint8)
        upper_brown = np.array([60, 255, 140], dtype=np.uint8)
    elif brightness >= 200:  # Ánh sáng mạnh
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

# Hàm tự động điều chỉnh ngưỡng màu vàng dựa trên độ sáng
def adjust_yellow_threshold(brightness):
    if brightness <= 50:  # Ánh sáng yếu
        lower_yellow = np.array([20, 100, 30], dtype=np.uint8)  # Hue cho vàng, Saturation và Value thấp
        upper_yellow = np.array([40, 255, 140], dtype=np.uint8)  # Hue cho vàng, bão hòa và sáng hơn
    elif brightness >= 200:  # Ánh sáng mạnh
        lower_yellow = np.array([20, 130, 80], dtype=np.uint8)  # Tăng độ bão hòa và sáng khi ánh sáng mạnh
        upper_yellow = np.array([40, 255, 255], dtype=np.uint8)  # Tăng giá trị tối đa của sáng
    else:  # Ánh sáng trung bình
        lower_yellow = np.array([7, 7, 128], dtype=np.uint8)
        upper_yellow = np.array([30, 255, 255], dtype=np.uint8)
    return lower_yellow, upper_yellow

def auto_yellow_mask(hsv_roi):
    brightness = calculate_brightness(hsv_roi)
    lower_brown, upper_brown = adjust_yellow_threshold(brightness)
    return cv2.inRange(hsv_roi, lower_brown, upper_brown)

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



