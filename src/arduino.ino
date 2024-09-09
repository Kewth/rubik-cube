#include <AccelStepper.h>
 
// 电机步进方式定义
const int FULLSTEP = 4;    //全步进参数
const int HALFSTEP = 8;    //半步进参数
const int TOT = 2048;
AccelStepper stepperL(HALFSTEP, 4, 5, 6, 7);
AccelStepper stepperR(HALFSTEP, 8, 9, 10, 11);
char lock_val = 0;
int target;

void setup() {
  const float maxSpeed = 500;
  const float acceleration = 50;
  stepperL.setMaxSpeed(maxSpeed);
  stepperL.setAcceleration(acceleration);
  stepperR.setMaxSpeed(maxSpeed);
  stepperR.setAcceleration(acceleration);
  Serial.begin(115200);
}

void loop() {
  if (stepperL.currentPosition() == 0)
    stepperL.moveTo(2048);
  if (stepperL.currentPosition() == 2048)
    stepperL.moveTo(0);
  if (lock_val == 0 && Serial.available() > 0) {
      char val = Serial.read();
      if (val == 'L') {
          int now = stepperL.currentPosition();
          target = now + 2048;
          stepperL.moveTo(target);
          Serial.println(now);
          Serial.println(target);
          lock_val = val;
      }
      if (val == 'R') {
          int now = stepperR.currentPosition();
          target = now + 1024;
          stepperR.moveTo(target);
          lock_val = val;
      }
  }
    stepperL.run();
    stepperR.run();
  if (lock_val == 'L') {
    if (stepperL.currentPosition() == target)
      lock_val = 0;
  }
  if (lock_val == 'R') {
    if (stepperR.currentPosition() == target)
      lock_val = 0;
  }
}