import rclpy
from rclpy.node import Node
from learning_interface.srv import Fib
import time

class FibServer(Node):
    def __init__(self, name):
        super().__init__(name)
        self.srv = self.create_service(Fib, 'fibonacci', self.fib_callback)
        self.get_logger().info('Server: waiting for requests...')

        self.declare_parameter('limit', 150)
        self.limit = self.get_parameter('limit').get_parameter_value().integer_value

    def fib_callback(self, request, response):
        a, b, c = request.a, request.b, 0
        self.get_logger().info(f'Server: incoming request: a={a}, b={b}, summing up until larger than limit={self.limit}')

        while c <= self.limit:
            c = a + b
            self.get_logger().info(f'Server: {a} + {b} = {c}')
            a = b
            b = c
            time.sleep(1)
        
        response.c = c
        return response
    
def main(args=None):
    rclpy.init(args=args)
    node = FibServer("fib_server")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()