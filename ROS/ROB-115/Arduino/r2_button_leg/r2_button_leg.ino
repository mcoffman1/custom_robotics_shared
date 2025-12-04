#include <ros.h>
#include <std_msgs/Int16.h>
//======================================================================
#include <Servo.h>

Servo leg;
Servo M1;
Servo M2;
Servo M4;
Servo M5;

const int green_button = 2;
const int red_button = 3;
int green_state = 0;
int red_state = 0;
bool button_held = 0;

//======================================================================
//================Setup node handler and global vars====================
//======================================================================

// Handles startup and shutdown of ROS
ros::NodeHandle nh;

//==================ROS Publishers======================================
std_msgs::Int16 button_msg;
ros::Publisher button_pub("button", &button_msg);
//======================================================================

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
  nh.getHardware()
  nh.initNode();
  nh.subscribe(subLegPos); 
//====================================================================== 
  nh.advertise(button_pub);
//======================================================================
  pinMode(green_button, INPUT_PULLUP);
  pinMode(red_button, INPUT_PULLUP);

  pinMode(13, OUTPUT);
//======================================================================  
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

  green_state = digitalRead(green_button);
  red_state = digitalRead(red_button);
  if (green_state == LOW)
  {
    while (green_state == LOW)
    {
      green_state = digitalRead(green_button);
      if (button_held)
      {
        ;
      }else
      {
        button_held = true;
        button_msg.data = 1;
        button_pub.publish( &button_msg );
      }
    }button_held = false;
  }else if (!red_state)
  {
    while (!red_state)
    {
      red_state = digitalRead(red_button);
      if (button_held)
      {
        ;
      }else
      {
        button_held = true;
        button_msg.data = 2;
        button_pub.publish( &button_msg );
      }
    }button_held = false;
  }
  nh.spinOnce();
  delay(10);
  
}