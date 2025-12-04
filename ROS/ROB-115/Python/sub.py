#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16

class MySubscriber:
    def __init__(self) -> None:
        rospy.init_node('Int_Subscriber', anonymous=False)
        int_sub = rospy.Subscriber('/my_int', Int16, self.intsub_callback, queue_size=10)

    def intsub_callback(self, msg): 
        num = msg.data
        if num == 10:
            print('Success')
        else:
            print(msg)

if __name__=='__main__':
    ms = MySubscriber()
    rospy.spin()
