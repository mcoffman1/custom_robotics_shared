#include <ros.h>
#include <std_msgs/Int16.h>
//======================================================================
#include <Servo.h>

Servo leg;
Servo M1;
Servo M2;
Servo M4;
Servo M5;

//======================================================================
//================Setup node handler and global vars====================
//======================================================================

// Handles startup and shutdown of ROS
ros::NodeHandle nh;

//======================================================================
//============Setup callback function===================================
//======================================================================

// Take the velocity command as input and calculate the PWM values.
void getlegpos(const std_msgs::Int16& legpos) 
{
  int num = legpos.data;
  // Set software limits 
  if (num < 0)
  {
    num = 0;
  }else if (num > 100)
  {
    num = 100;
  }
  int angle = map(num,0,100,0,160);
  leg.write(angle);
}

//============Setup Subscriber function=================================

ros::Subscriber<std_msgs::Int16> subLegPos("leg_pos", &getlegpos );

//======================================================================

void setup() 
{
//======================================================================
  // ROS Setup
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.subscribe(subLegPos); 
//======================================================================  
  leg.attach(9,1000,2000);
  // MIN 40 max 140
  M1.attach(5,1000,2000);
  M2.attach(6,1000,2000);
  M4.attach(10,1000,2000);
  M5.attach(11,1000,2000);
  delay(2000);

  leg.write(0);
}

void loop() 
{
  nh.spinOnce();
  delay(10);
}