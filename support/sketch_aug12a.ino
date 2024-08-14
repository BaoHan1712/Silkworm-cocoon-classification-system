#include <Servo.h>

const int servoPin = 6;  // Chân điều khiển của servo
Servo myServo;

void setup() {
  Serial.begin(9600);  // Khởi động giao tiếp serial với tốc độ baudrate 9600
  myServo.attach(servoPin);  // Kết nối servo với chân điều khiển
  myServo.write(0);  // Đặt servo ở góc 0 độ khi khởi động
}

void loop() {
  if (Serial.available() > 0) {
    char signal = Serial.read();  // Đọc ký tự từ cổng serial

    // Điều khiển servo dựa trên ký tự nhận được
    if (signal == '1') {
      myServo.write(180);  // Quay servo đến 180 độ
      delay(1000);  // Đợi 1 giây
      myServo.write(0);  // Quay servo về 0 độ
    } else if (signal == '2') {
      myServo.write(45);  // Quay servo đến 45 độ cho màu nâu
      delay(1000);  // Đợi 1 giây
      myServo.write(0);  // Quay servo về 0 độ
    } else if (signal == '3') {
      myServo.write(90);  // Quay servo đến 90 độ cho màu vàng
      delay(500);  // Đợi 1 giây
      myServo.write(0);  // Quay servo về 0 độ
    } else if (signal == 'W') {
      myServo.write(135);  // Quay servo đến 135 độ cho màu trắng
      delay(1000);  // Đợi 1 giây
      myServo.write(0);  // Quay servo về 0 độ
    }
  }
}
