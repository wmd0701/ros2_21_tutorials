from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    client = Node(package='learning_action', executable='fib_client', output='screen', arguments=['277'])
    server = Node(package='learning_action', executable='fib_server', output='screen', parameters=[{'max_fib': 666}])
    return LaunchDescription([client, server])