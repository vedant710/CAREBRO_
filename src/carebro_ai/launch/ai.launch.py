import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    params = os.path.join(
        get_package_share_directory("carebro_ai"), "config", "ai.yaml"
    )

    def ai_node(executable):
        return Node(
            package="carebro_ai",
            executable=executable,
            name=executable,
            parameters=[params, {"use_sim_time": True}],
            output="screen",
        )

    # Your main() functions are empty for now, so these exit immediately
    # until you write them.
    return LaunchDescription([
        ai_node("object_detector_node"),
        ai_node("nl_command_node"),
        ai_node("semantic_navigator_node"),
    ])
