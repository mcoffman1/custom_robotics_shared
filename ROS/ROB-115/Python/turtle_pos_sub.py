#!/usr/bin/env python3

import rospy
from turtlesim.msg import Pose
from std_srvs.srv import Empty

class TurtleMonitor:
    def __init__(self):
        rospy.init_node('pos_sub', anonymous = True)

        # parameters
        self.x_val = 5.6
        self.y_val = 5.6
        self.count = 0
        self.last_color = None # (r, g, b)

        self.divisor = 30

        rospy.Subscriber('/turtle1/pose', Pose, self.pose_callback)

    # set up the callback for the ros subscriber
    def pose_callback(self,msg):
        self.count += 1

        # log pose updates based on divisor
        if self.count % self.divisor == 0:
            rospy.loginfo('Turtle pos: x=%.2f, y=%.2f, theta=%.2f', msg.x, msg.y, msg.theta)

        # change our color
        if msg.x > self.x_val and msg.y > self.y_val:
            new_color = (255, 0 ,0) # (r,g,b)
        else:
            new_color = (0, 0, 255)

        # change the background
        if new_color != self.last_color:
            self.set_background(*new_color)
            self.last_color = new_color

    # set up the set background method
    def set_background(self, r, g, b):
        rospy.set_param('/turtlesim/background_r', r)
        rospy.set_param('/turtlesim/background_g', g)
        rospy.set_param('/turtlesim/background_b', b)

        try:
            rospy.wait_for_service('/clear', timeout=1.0)
            clear_bg = rospy.ServiceProxy('/clear', Empty)
            clear_bg()
        except rospy.ServiceException as e:
            rospy.logwarn("Failed to call /clear service: %s", e)

    def run(self):
        rospy.spin()


if __name__=='__main__':
    tm = TurtleMonitor()
    tm.run()