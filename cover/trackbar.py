import cv2
import numpy as np

# Hàm callback cho trackbar
def nothing(x):
    pass

# Khởi tạo cửa sổ và các trackbar
cv2.namedWindow('Trackbars')
cv2.createTrackbar('L-H', 'Trackbars', 20, 180, nothing)
cv2.createTrackbar('L-S', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('L-V', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('U-H', 'Trackbars', 30, 180, nothing)
cv2.createTrackbar('U-S', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('U-V', 'Trackbars', 255, 255, nothing)

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Lấy giá trị từ các trackbar
    l_h = cv2.getTrackbarPos('L-H', 'Trackbars')
    l_s = cv2.getTrackbarPos('L-S', 'Trackbars')
    l_v = cv2.getTrackbarPos('L-V', 'Trackbars')
    u_h = cv2.getTrackbarPos('U-H', 'Trackbars')
    u_s = cv2.getTrackbarPos('U-S', 'Trackbars')
    u_v = cv2.getTrackbarPos('U-V', 'Trackbars')

    # Xác định phạm vi màu sắc
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])

    # Tạo mặt nạ dựa trên phạm vi màu sắc
    mask = cv2.inRange(hsv, lower, upper)

    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
