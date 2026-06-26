import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse
from learning_interface.action import Fib
import time

class FibActionServer(Node):
    def __init__(self, name):
        super().__init__(name)
        self.action_server = ActionServer(self, Fib, 'fibonacci', 
                                          goal_callback = self.goal_callback, 
                                          execute_callback = self.execute_callback)

        self.declare_parameter('max_fib', 500)
        self.max_fib = self.get_parameter('max_fib').get_parameter_value().integer_value

        self.get_logger().info(f"Action Server: server started. Max Fibonacci value set to: {self.max_fib}")

    def goal_callback(self, goal_request):
        self.limit = goal_request.limit
        if self.limit > self.max_fib:
            self.get_logger().info(f"Action Server: Goal rejected. Limit {self.limit} exceeds max_fib {self.max_fib}.")
            return GoalResponse.REJECT
        else:
            self.get_logger().info(f"Action Server: Goal accepted. Limit: {self.limit}.")
            return GoalResponse.ACCEPT
        
    def execute_callback(self, goal_handle):
        feedback_msg = Fib.Feedback()
        a, b, c = 0, 1, 0
        while c <= self.limit:
            c = a + b
            self.get_logger().info(f"Action Server: {a} + {b} = {c}")
            feedback_msg.current = c
            goal_handle.publish_feedback(feedback_msg)
            a = b
            b = c
            time.sleep(1.5)
        
        goal_handle.succeed()
        result = Fib.Result()
        result.final = c
        self.get_logger().info(f"Action Server: Fibonacci sequence completed. Final value: {c}.")
        return result
    
def main(args=None):
    rclpy.init(args=args)
    node = FibActionServer("fib_server")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()