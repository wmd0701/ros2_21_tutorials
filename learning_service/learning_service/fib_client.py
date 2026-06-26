import rclpy
from rclpy.node import Node
from learning_interface.srv import Fib
import random

class FibClient(Node):
    def __init__(self, name):
        super().__init__(name)
        self.client = self.create_client(Fib, 'fibonacci')
        self.get_logger().info('Client: waiting for service to become available...')
        self.client.wait_for_service()
        self.get_logger().info('Client: service is available, sending request...')
        self.send_request()

    def send_request(self):
        a, b = random.randint(0, 10), random.randint(1, 10)
        request = Fib.Request(a = a, b = b)
        self.get_logger().info(f'Client: sending request: a={a}, b={b}')
        
        self.future = self.client.call_async(request)
        self.future.add_done_callback(self.response_callback)
        
    def response_callback(self, future):
        c = future.result().c
        self.get_logger().info(f'Client: received response: {c}')

def main(args=None):
    rclpy.init(args=args)
    node = FibClient("fib_client")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()