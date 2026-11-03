import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    ekf_yaml = os.path.join(
        get_package_share_directory("carebro_sensor_fusion"), "config", "ekf.yaml"
    )

    ekf = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        output="screen",
        parameters=[
            ekf_yaml,
            {
                "use_sim_time": True,
                "publish_tf": ParameterValue(
                    LaunchConfiguration("publish_tf"), value_type=bool
                ),
            },
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument("publish_tf", default_value="false"),
        ekf,
    ])
