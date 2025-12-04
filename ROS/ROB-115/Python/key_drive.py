#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import curses

class RobotDriver:
    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr
        rospy.init_node('Robot_Driver', anonymous=True)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.twist = Twist()
        self.linear = 0.0
        self.angular = 0.0

    def publish(self, linear, angular):
        self.twist.linear.x = linear
        self.twist.angular.z = angular
        self.cmd_vel_pub.publish(self.twist)

    def run(self):
        self.stdscr.nodelay(True)  # Do not wait for input when calling getch
        self.stdscr.clear()
        self.stdscr.addstr("Press arrow keys to control the robot. 's' to stop. 'q' to quit.\n")
        last_key = None
        while True:
            try:
                key = self.stdscr.getch()
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    self.linear = 0.0
                    self.angular = 0.0
                    self.publish(self.linear, self.angular)
                elif key == curses.KEY_UP:
                    self.linear = self.linear + 0.5
                    self.publish(self.linear, self.angular)
                elif key == curses.KEY_DOWN:
                    self.linear = self.linear - 0.5
                    self.publish(self.linear, self.angular)
                elif key == curses.KEY_LEFT:
                    self.angular = self.angular + 1
                    self.publish(self.linear, self.angular)
                elif key == curses.KEY_RIGHT:
                    self.angular = self.angular - 1
                    self.publish(self.linear, self.angular)

            except Exception as e:
                rospy.logerr(e)
                break

# Wrapper function to setup curses and clean up properly
def main(stdscr):
    curses.curs_set(0)  # Invisible cursor
    driver = RobotDriver(stdscr)
    driver.run()

if __name__=='__main__':
    curses.wrapper(main)
