import cv2

# Mở camera (sử dụng chỉ số 0 cho camera mặc định)
cap = cv2.VideoCapture(0)

# Kiểm tra nếu camera không mở được
if not cap.isOpened():
    print("Không thể mở camera")
    exit()

while True:
    # Đọc khung hình từ camera
    ret, frame = cap.read()

    # Kiểm tra xem có đọc được khung hình không
    if not ret:
        print("Không thể nhận diện khung hình (đã hết)")
        break

    # Hiển thị khung hình
    cv2.imshow('Camera', frame)

    # Nhấn 'q' để thoát khỏi vòng lặp
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
