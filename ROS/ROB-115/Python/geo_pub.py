#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

class RobotDriver:
    def __init__(self) -> None:
        rospy.init_node('Robot_Driver')
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10, latch=True)
        self.twist = Twist()

# linear and angular values must be floats
    def publish(self, linear, angular):
        self.twist.linear.x = linear
        self.twist.angular.z = angular
        self.cmd_vel_pub.publish(self.twist)

if __name__=='__main__':
    rd = RobotDriver()
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        try:
            rd.publish(1,1)
            rate.sleep()
        except KeyboardInterrupt:
            break
    rospy.loginfo('Shutting down Robot Driver')