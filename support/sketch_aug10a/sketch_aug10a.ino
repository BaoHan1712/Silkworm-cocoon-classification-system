#include <Arduino.h>
#define START_BYTE 0x02

#define DEFAULT_SIZE 5
#define MAX_DATA_SIZE 10
struct PackageUART {
    uint8_t form;         
    uint8_t to;           
    uint8_t title;        
    uint16_t data[MAX_DATA_SIZE];  // Thông tin
    uint8_t dataSize;     
    uint16_t checkSum; 
};

void setup() {
  
}

void loop() {
  if (Serial.available() > 0) {
        if (Serial.read() != START_BYTE) return;  
        PackageUART package;
        uint8_t sizePacketUart = Serial.read();
        Serial.println(sizePacketUart);
        uint8_t dataSize = (sizePacketUart - DEFAULT_SIZE) / 2;  // Tính toán số phần tử trong data
        
        if (dataSize > MAX_DATA_SIZE) {
            Serial.println("Kích thước data vượt quá giới hạn!");
            Serial.print(dataSize);
            return;
        }
        uint8_t buffer[sizePacketUart];
        size_t bytesRead = Serial.readBytes(buffer, sizePacketUart);
        package.form = buffer[0];
        package.to = buffer[1];
        package.title = buffer[2];
        package.dataSize = dataSize;

        for (int i = 0; i < dataSize; i++) { // Lấy thông tin
            package.data[i] = (buffer[3 + i * 2] << 8) | buffer[4 + i * 2];
        }

        package.checkSum = (buffer[dataSize * 2 + 3] << 8) | buffer[dataSize * 2 + 4];

        if (package.checkSum != calculateCheckSum(package.form, package.to, package.title, package.data, package.dataSize)) {
            Serial.println("Checksum không đúng");
            return;
        }
        // Serial.println(package.form);
        // Serial.println(package.to);
        // Serial.println(package.title,HEX);
        // for (int i = 0; i < dataSize; i++) {
        //     Serial.println(package.data[i]);
        // }
        
        switch (package.title)
        {
        case 0x54:
            {
                 uint16_t data[2] = {512, 100};
                sendPacket(package.to, package.form, package.title, data, 2);

                break;
            }
        case 0x6F:{
            
            break;
        }
        case 0x66:{
            
            break;
        }
        default:
            Serial.println("Sai tieu de!");
            break;
        }
    }
}


uint16_t calculateCheckSum(uint8_t form, uint8_t to, uint8_t title, const uint16_t* data, uint8_t dataSize) {
    uint16_t sum = form + to + title;
    for (int i = 0; i < dataSize; i++) {
        sum += (data[i] >> 8) & 0xFF;
        sum += data[i] & 0xFF;
    }
    return sum;
}


void sendPacket(uint8_t form, uint8_t to, uint8_t title, const uint16_t* data, uint8_t dataSize) {
    Serial.write(START_BYTE);       
    uint8_t packetSize = 5 + dataSize * 2; 
    Serial.write(packetSize);
    Serial.write(form);
    Serial.write(to);
    Serial.write(title);
    
    for (int i = 0; i < dataSize; i++) {
        Serial.write((data[i] >> 8) & 0xFF);
        Serial.write(data[i] & 0xFF);
    }
uint16_t sum = calculateCheckSum(form, to, title, data, dataSize);
    Serial.write((sum >> 8) & 0xFF);
    Serial.write(sum & 0xFF);
}