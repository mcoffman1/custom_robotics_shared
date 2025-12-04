#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16

# Define the MyPublisher class
class MyPublisher:
    def __init__(self):
        # Initialize a ROS node named 'Int_Publisher'. The `anonymous=True` ensures the node has a unique name
        # by appending random numbers to the end, allowing multiple instances without name collisions.
        rospy.init_node('Int_Publisher', anonymous=False)
        self.int_pub = rospy.Publisher('/my_int', Int16, queue_size=10, latch=True)

    def publish_int(self, num):
        my_int = Int16(num)
        self.int_pub.publish(my_int)

# This block ensures that the following code is executed only when the script is run directly, not when imported as a module.
if __name__ == '__main__':
    mp = MyPublisher()
    rate = rospy.Rate()

    # Enter a loop that runs until ROS is shutdown (e.g., CTRL+C is pressed in the terminal)
    while not rospy.is_shutdown():
        try:
            mp.publish_int(7)
            rate.sleep()
        except KeyboardInterrupt:
            break
    rospy.loginfo("int pub shutdown")