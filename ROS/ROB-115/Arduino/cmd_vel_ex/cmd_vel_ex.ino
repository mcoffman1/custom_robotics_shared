
//======================================================================
#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int16.h>
//======================================================================
#include <Servo.h>

//=============Setup Drive motors=======================================
Servo left_wheel;
Servo right_wheel; 

//======================================================================
//================Setup node handler and global vars====================
//======================================================================

// Handles startup and shutdown of ROS
ros::NodeHandle nh;

const double whbase = .622;
const double m = 64.286;
const double b = 90;

//======================================================================
//============Setup callback function===================================
//======================================================================

// Take the velocity command as input and calculate the PWM values.
void getvel(const geometry_msgs::Twist& cmdVel) 
{
   
  // Calculate the PWM value given the desired velocity 
  double linear = cmdVel.linear.x;
  double angular = cmdVel.angular.z;

  double vleft = linear - ((angular * whbase) / 2);
  double vright = linear + ((angular * whbase) / 2);

  double left_speed = m*vleft+b;
  
  // set pwm limits
  if (left_speed > 180)
  {
    left_speed = 180;
  }else if (left_speed < 0)
  {
    left_speed = 0;
  }
  
  
  double right_speed = m*vright+b;
  
  // set pwm limits
  if (right_speed > 180)
  {
    right_speed = 180;
  }else if (right_speed < 0)
  {
    right_speed = 0;
  }

  drive(left_speed,right_speed);

}

//============Setup Subscriber function=================================

ros::Subscriber<geometry_msgs::Twist> subCmdVel("cmd_vel", &getvel );

//======================================================================


//===================ROS Publishers=====================================
std_msgs::Int16 left_pwm_msg;
ros::Publisher lpwm_pub("left_pwm", &left_pwm_msg);

std_msgs::Int16 right_pwm_msg;
ros::Publisher rpwm_pub("right_pwm", &right_pwm_msg);
//======================================================================


void setup() 
{
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  
  // ROS Setup
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.subscribe(subCmdVel); 
  nh.advertise(lpwm_pub); 
  nh.advertise(rpwm_pub);
   
  left_wheel.attach(11, 1000, 2000);
  right_wheel.attach(10, 1000, 2000);
}


void loop() 
{
  nh.spinOnce();
  delay(10);
}