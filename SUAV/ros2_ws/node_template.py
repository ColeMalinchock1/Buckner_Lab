#!/usr.bin/env python

# Import the required ros2 libraries
import rclpy
from rclpy.node import Node

# Import the type of messages you want to send in ROS2
from std_msgs.msg import Int64

# Import threading library
import threading 

# Callback method called everytime a new message is sent over ROS2 node
def callback(data):

    # Calling the global message
    global message

    # Setting the data received 
    message = data.data

# Main method called at the start
def main(args = None):

    # Calling the global message
    global message

    # Initializing the ros2 node
    rclpy.init(args=args)

    # Creating the node
    node = Node("sample_node")

    # Create a subscription to another node
    # Parameters of create_subscription(message data type, topic name, method callback, priority)
    node.create_subscription(Int64, 'sample_sub_topic_name', callback, 1)

    # Create a publisher to another node
    # Parameters of create_publisher(message data type, topic name, method callback, priority)
    pub_sample_message = node.create_publisher(Int64, 'sample_pub_topic_name', 1)

    # Threading loop that automatically spins the ros2 node
    thread = threading.Thread(target=rclpy.spin, args=(node, ), daemon=True)
    thread.start()

    # While ros2 node is ok
    while rclpy.ok():

        # Make an integer message
        m = Int64()

        # Attaching the global message to the m.data
        m.data = message

        # Publishing the message
        pub_sample_message.publish(m)

    # Need to attach at the end to make sure the node is spinning and shutsdown properly.
    rclpy.spin(node)
    rclpy.shutdown()

# Automatically runs the main method
if __name__ == '__main__':
    main()
