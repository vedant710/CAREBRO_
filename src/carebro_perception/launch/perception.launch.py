import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    params = os.path.join(
        get_package_share_directory("carebro_perception"), "config", "perception.yaml"
    )

    def perception_node(executable):
        return Node(
            package="carebro_perception",
            executable=executable,
            name=executable,
            parameters=[params, {"use_sim_time": True}],
            output="screen",
        )

    # Your main() functions are empty for now, so these exit immediately
    # ("process has finished cleanly") until you write them.
    return LaunchDescription([
        perception_node("mono_vision_node"),
        perception_node("depth_vision_node"),
        perception_node("obstacle_cloud_node"),
    ])
