#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16

class ButtonHandler:
    def __init__(self):
        rospy.init_node('button_node', anonymous=False)
        button_sub = rospy.Subscriber('button', Int16, self.button_callback, queue_size=10)
        self.leg_pos_pub = rospy.Publisher('leg_pos', Int16, queue_size=10, latch=True)
    
    # runs when subscriber gets a message
    def button_callback(self, msg):
        num = msg.data
        if num == 1:
            #extend
            #print('extend')
            self.publish_pos(100)
        elif num == 2:
            #retract
            #print('retract')
            self.publish_pos(0)
            
    def publish_pos(self, pos):
        my_int16 = Int16(pos)
        print(my_int16)
        self.leg_pos_pub.publish(my_int16)
        
if __name__=='__main__':
    bh = ButtonHandler()
    rate = rospy.Rate(30)
    
    # create a loop that runs until ros shutdown
    while not rospy.is_shutdown():
        try:
            #bh.publish_pos(0)
            rate.sleep()
        except KeyboardInterrupt:
            rospy.loginfo('button node shutdown')
            break
        