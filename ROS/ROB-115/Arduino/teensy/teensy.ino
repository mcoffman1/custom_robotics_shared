#include <Servo.h>

Servo head;
Servo right_shoulder;
Servo left_shoulder;
Servo right_ankle;
Servo left_ankle;

void setup() 
{
  head.attach(3);
  right_shoulder.attach(4);
  left_shoulder.attach(5);
  right_ankle.attach(6);
  left_ankle.attach(7);

  head.write(90);
  
  //========================
  //==160-forward 130 middle to 90-back
  //========================
  right_shoulder.write(110);
  
  //========================
  //==80-forward 113 middle to 150-back
  //========================
  left_shoulder.write(130);
  
  //========================
  //60-forward 55-center
  //========================
  right_ankle.write(60);
  
  //========================
  //65-forward 55-center
  //========================
  left_ankle.write(60);
 
}
int pos = 0;
void loop() 
{ 
//  for(pos = 0; pos <= 180; pos += 1) // goes from 0 degrees to 180 degrees 
//  {                                  // in steps of 1 degree 
//    head.write(pos);              // tell servo to go to position in variable 'pos' 
//    delay(50);                       // waits 15ms for the servo to reach the position 
//  } 
//  for(pos = 180; pos>=0; pos-=1)     // goes from 180 degrees to 0 degrees 
//  {                                
//    head.write(pos);              // tell servo to go to position in variable 'pos' 
//    delay(50);                       // waits 15ms for the servo to reach the position 
//  } 
}