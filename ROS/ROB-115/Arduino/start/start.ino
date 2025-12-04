#include <Servo.h>

Servo leg;
Servo M1;
Servo M2;
Servo M4;
Servo M5;


void setup() 
{
  leg.attach(9,1000,2000);
  // MIN 40 max 140
  M1.attach(5,1000,2000);
  M2.attach(6,1000,2000);
  M4.attach(10,1000,2000);
  M5.attach(11,1000,2000);
  delay(2000);

  leg.write(160);
}

void loop() 
{
}