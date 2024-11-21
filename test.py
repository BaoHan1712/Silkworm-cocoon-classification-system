import cv2
import numpy as np

# Hàm để nhận diện màu nâu trong không gian màu HSV
def detect_brown_color(image):
    # Chuyển đổi hình ảnh từ BGR sang HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Định nghĩa dải màu nâu trong không gian màu HSV
    lower_brown = np.array([10, 100, 20])
    upper_brown = np.array([20, 255, 200])

    # Tạo mask cho màu nâu
    mask = cv2.inRange(hsv_image, lower_brown, upper_brown)

    return mask

# Hàm tìm contour và vẽ bbox
def draw_bounding_box(image, mask):
    # Tìm contour từ mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Tính toán bbox từ contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Vẽ hộp bao quanh (bbox) với màu đen
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 2)

    return image

# Tải hình ảnh
image = cv2.imread('1655873004496.JPG')

# Nhận diện màu nâu
mask_brown = detect_brown_color(image)

# Vẽ bounding box quanh màu nâu
image_with_bbox = draw_bounding_box(image, mask_brown)

# Hiển thị hình ảnh kết quả
cv2.imshow("Brown Color Detection", image_with_bbox)
cv2.waitKey(0)
cv2.destroyAllWindows()
