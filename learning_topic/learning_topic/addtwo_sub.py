import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

class AddTwoSubscriber(Node):
    def __init__(self, name):
        super().__init__(name)
        self.subscriber = self.create_subscription(Int32MultiArray, "addtwo", self.listener_callback, 10)

    def listener_callback(self, msg):
        a, b, c = msg.data
        self.get_logger().info(f'Subscriber: received {a} + {b} = {c}')

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoSubscriber("addtwo_subscriber")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()