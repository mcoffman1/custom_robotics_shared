#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import random

def rand_vel_pub():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('rand_vel_pub', anonymous=False)
    rate = rospy.Rate(1) # Hz
    vel = Twist()

    while not rospy.is_shutdown():
        vel.linear.x = random.uniform(0.5, 2.0)
        vel.angular.z = random.uniform(-3.0, 3.0)
        pub.publish(vel)
        rate.sleep()

if __name__=='__main__':
    try:
        rand_vel_pub()
    except rospy.ROSInterruptException:
        pass