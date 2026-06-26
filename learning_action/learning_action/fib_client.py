import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from learning_interface.action import Fib
import sys

class FibActionClient(Node):
    def __init__(self, name):
        super().__init__(name)
        self.action_client = ActionClient(self, Fib, 'fibonacci')
        self.limit = int(sys.argv[1]) if len(sys.argv) > 1 else 150

        self.send_goal()

    def send_goal(self):
        self.get_logger().info(f"Action Client: waiting for action server to be available...")
        self.action_client.wait_for_server()
        self.get_logger().info(f"Action Client: action server available. Sending goal with limit: {self.limit}.")

        goal_request = Fib.Goal()
        goal_request.limit = self.limit
        self.send_goal_future = self.action_client.send_goal_async(goal_request, 
                                                                   feedback_callback=self.feedback_callback)
        
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if goal_handle.accepted:
            self.get_logger().info("Action Client: Goal accepted. Waiting for result...")
            self.get_result_future = goal_handle.get_result_async()
            self.get_result_future.add_done_callback(self.get_result_callback)
        else:
            self.get_logger().info("Action Client: Goal rejected.")
            return
        
    def get_result_callback(self, future):
        final = future.result().result.final
        self.get_logger().info(f"Action Client: Result received. Final Fibonacci value: {final}.")

    def feedback_callback(self, feedback_msg):
        current = feedback_msg.feedback.current
        self.get_logger().info(f"Action Client: intermediate feedback received. Current Fibonacci value: {current}")

def main(args=None):
    rclpy.init(args=args)
    node = FibActionClient("fib_client")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()