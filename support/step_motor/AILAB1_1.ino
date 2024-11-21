#include <Stepper.h>

// Number of steps per output rotation
const int stepsPerRevolution = 200;

// Create instances of Stepper library
Stepper myStepper(stepsPerRevolution, 2, 3, 4, 5);
Stepper myStepper2(stepsPerRevolution, 8, 9, 10, 11);

// Button pins
const int buttonIncreasePin = 6;
const int buttonDecreasePin = 7;

// Initial speed
int motorSpeed = 220;

void setup() {
  // Set button pins as inputs
  pinMode(buttonIncreasePin, INPUT_PULLUP);
  pinMode(buttonDecreasePin, INPUT_PULLUP);

  // Set initial speed
  myStepper.setSpeed(motorSpeed);
  myStepper2.setSpeed(180);

  // Initialize serial port
  Serial.begin(9600);
}

void loop() {
  // Read button states
  int buttonIncreaseState = digitalRead(buttonIncreasePin);
  int buttonDecreaseState = digitalRead(buttonDecreasePin);

  // Increase speed if button pressed
  if (buttonIncreaseState == LOW) {
    motorSpeed += 10;
    myStepper.setSpeed(motorSpeed);
 
    delay(200); // Debounce delay
  }

  // Decrease speed if button pressed
  if (buttonDecreaseState == LOW) {
    motorSpeed -= 10;
    if (motorSpeed < 0) {
      motorSpeed = 0;
    }
    myStepper.setSpeed(motorSpeed);

    delay(200); // Debounce delay
  }

  // Step the motors

  for (int i = 0; i < stepsPerRevolution; i++) {
    myStepper.step(-1);  
    myStepper2.step(-1); 
}
}

