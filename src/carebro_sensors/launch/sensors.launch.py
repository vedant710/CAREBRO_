import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory("carebro_sensors")

    encoder_sim = Node(
        package="carebro_sensors",
        executable="encoder_sim",
        name="encoder_sim",
        parameters=[
            os.path.join(share, "config", "encoders.yaml"),
            {"use_sim_time": True},
        ],
        output="screen",
    )

    return LaunchDescription([encoder_sim])
