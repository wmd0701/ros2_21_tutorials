import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
import random

class AddTwoPublisher(Node):
    def __init__(self, name):
        super().__init__(name)
        self.publisher = self.create_publisher(Int32MultiArray, "addtwo", 10)
        self.timer = self.create_timer(2.0, self.timer_callback)

    def timer_callback(self):
        msg = Int32MultiArray()
        a, b = random.randint(0, 100), random.randint(0, 100)
        c = a + b
        msg.data = [a, b, c]
        self.publisher.publish(msg)
        self.get_logger().info(f'Publisher: publishing {a} + {b} = {c}')

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoPublisher("addtwo_publisher")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()