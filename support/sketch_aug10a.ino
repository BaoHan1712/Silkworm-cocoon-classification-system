#include <Servo.h>

const int servoPin = 5;          // Pin điều khiển servo 1
const int servoPin2 = 4;         // Pin điều khiển servo 2
const int trigPin = 12;          // Pin phát xung siêu âm
const int echoPin = 11;          // Pin nhận xung siêu âm
const int distanceThreshold = 20; // Khoảng cách ngưỡng để phát hiện vật

Servo myServo;                   // Đối tượng servo 1
Servo myServo2;                  // Đối tượng servo 2

int signalList[20];              // Danh sách lưu tín hiệu
int listSize = 0;                // Kích thước danh sách
bool isProcessing = false;       // Trạng thái xử lý tín hiệu
int currentSignal = -1;          // Tín hiệu hiện tại để xử lý

unsigned long previousMillis = 0; // Thời gian trước đó
const long interval = 3000;       // Khoảng thời gian 3 giây
bool servoAt180 = false;          // Trạng thái servo 1 đã quay đến 180 độ
bool servo2At180 = false;         // Trạng thái servo 2 đã quay đến 180 độ

void setup() {
  Serial.begin(9600); 
  myServo.attach(servoPin);
  myServo2.attach(servoPin2);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  myServo.write(0);  // Đặt servo 1 về vị trí 0 độ
  myServo2.write(0); // Đặt servo 2 về vị trí 0 độ
  delay(1000);       // Chờ các servo ổn định
}

void loop() {
  // Kiểm tra khoảng cách từ cảm biến siêu âm
  long duration, distance;
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) / 29.1; // Tính khoảng cách
  
  // Thời gian hiện tại
  unsigned long currentMillis = millis();

  if (distance < distanceThreshold) {
    // Có vật gần, kiểm tra danh sách tín hiệu
    if (listSize > 0 && !isProcessing) {
      // Lấy tín hiệu đầu tiên trong danh sách và bắt đầu xử lý
      currentSignal = signalList[0];
      for (int i = 0; i < listSize - 1; i++) {
        signalList[i] = signalList[i + 1];
      }
      listSize--;

      // Bắt đầu xử lý tín hiệu
      isProcessing = true;
      servoAt180 = false;
      servo2At180 = false;
      previousMillis = currentMillis; // Khởi tạo thời gian trước
    }
  }

  // Điều khiển servo dựa trên tín hiệu hiện tại
  if (isProcessing) {
    if (currentSignal == 2) {
      // Điều khiển servo 1 khi nhận tín hiệu 3
      if (!servoAt180) {
        myServo.write(90);  
        servoAt180 = true;
        previousMillis = currentMillis; // Khởi tạo lại thời gian trước
      } 
      else if (servoAt180 && currentMillis - previousMillis >= interval) {
        myServo.write(0);    // Quay servo 1 về 0 độ
        isProcessing = false;  // Kết thúc xử lý tín hiệu
      }
    } 
    else if (currentSignal == 3) {
      // Điều khiển servo 2 khi nhận tín hiệu 1
      if (!servo2At180) {
        myServo2.write(90);  // Quay servo 2 đến 90 độ
        servo2At180 = true;
        previousMillis = currentMillis; // Khởi tạo lại thời gian trước
      } 
      else if (servo2At180 && currentMillis - previousMillis >= interval) {
        myServo2.write(0);    // Quay servo 2 về 0 độ
        isProcessing = false;  // Kết thúc xử lý tín hiệu
      }
    } 
    else {
      isProcessing = false;  // Kết thúc xử lý tín hiệu nếu không phù hợp
    }
  }
  
  // Kiểm tra xem có tín hiệu mới từ Python không
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();
    int signal = -1;
    
    // Xác định tín hiệu
    if (incomingByte == '1') {
      signal = 1;
    } else if (incomingByte == '2') {
      signal = 2;
    } else if (incomingByte == '3') {
      signal = 3;
    }
    
    // Thêm tín hiệu vào danh sách nếu hợp lệ và danh sách chưa đầy
    if (signal != -1 && listSize < sizeof(signalList) / sizeof(signalList[0])) {
      signalList[listSize] = signal;
      listSize++;
    }
  }
}
