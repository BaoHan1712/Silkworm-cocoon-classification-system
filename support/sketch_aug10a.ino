#include <Servo.h>

const int servoPin = 5;          // Pin điều khiển servo 1
const int servoPin2 = 3;         // Pin điều khiển servo 2
int irSensorPin = A0;            // Pin kết nối cảm biến hồng ngoại

Servo myServo;                   // Đối tượng servo 1
Servo myServo2;                  // Đối tượng servo 2

int signalList[30];              // Danh sách lưu tín hiệu
int listSize = 0;                // Kích thước danh sách
bool isProcessing = false;       // Trạng thái xử lý tín hiệu
int currentSignal = -1;          // Tín hiệu hiện tại để xử lý

unsigned long previousMillis = 0; // Thời gian trước đó
const long interval = 2000;       // Khoảng thời gian 2 giây
bool servoAt180 = false;          // Trạng thái servo 1 đã quay đến 180 độ
bool servo2At180 = false;         // Trạng thái servo 2 đã quay đến 180 độ
bool objectDetected = false;      // Trạng thái phát hiện vật

void setup() {
  Serial.begin(9600); 
  myServo.attach(servoPin);
  myServo2.attach(servoPin2);
  pinMode(irSensorPin, INPUT);
  
  myServo.write(15);  // Đặt servo 1 về vị trí 0 độ
  myServo2.write(80); // Đặt servo 2 về vị trí 0 độ
  delay(1000);       // Chờ các servo ổn định
}

void loop() {
  // Kiểm tra tín hiệu từ cảm biến hồng ngoại
  int irSignal = digitalRead(irSensorPin);

  // Thời gian hiện tại
  unsigned long currentMillis = millis();

  if (irSignal == LOW && !objectDetected) {  // Khi cảm biến phát hiện vật
    objectDetected = true; // Đánh dấu rằng vật đã được phát hiện
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
  else if (irSignal == HIGH) {  // Khi vật rời khỏi cảm biến
    objectDetected = false; // Đặt lại trạng thái phát hiện vật
  }

  // Điều khiển servo dựa trên tín hiệu hiện tại
  if (isProcessing) {
    if (currentSignal == 2) {
    // Điều khiển servo 1 khi nhận tín hiệu 2
    if (!servoAt180) {
      if (currentMillis - previousMillis >= 1000) {  // Đợi 1 giây trước khi quay servo
        myServo.write(90);  
        servoAt180 = true;
        previousMillis = currentMillis; // Khởi tạo lại thời gian trước
      }
    } 
    else if (servoAt180 && currentMillis - previousMillis >= interval) {
      myServo.write(15);    // Quay servo 1 về 15 độ
      isProcessing = false;  // Kết thúc xử lý tín hiệu
    }
  }

    else if (currentSignal == 1) {
      // Điều khiển servo 2 khi nhận tín hiệu 2
      if (!servo2At180) {
        myServo2.write(160);  // Quay servo 2 đến 160 độ
        servo2At180 = true;
        previousMillis = currentMillis; // Khởi tạo lại thời gian trước
      } 
      else if (servo2At180 && currentMillis - previousMillis >= interval) {
        myServo2.write(80);    // Quay servo 2 về 80 độ
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
    } 
    // Thêm tín hiệu vào danh sách nếu hợp lệ và danh sách chưa đầy
    if (signal != -1 && listSize < sizeof(signalList) / sizeof(signalList[0])) {
      signalList[listSize] = signal;
      listSize++;
    }
  }
}
