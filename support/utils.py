import cv2
import numpy as np


def create_color_mask(hsv, lower_color, upper_color):
    return cv2.inRange(hsv, lower_color, upper_color)


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



