import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    gz_share = get_package_share_directory("carebro_gazebo")
    nav_share = get_package_share_directory("carebro_navigation")
    nav2_share = get_package_share_directory("nav2_bringup")

    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gz_share, "launch", "sim.launch.py")
        ),
        launch_arguments={
            "world": LaunchConfiguration("world"),
            "rviz": "false",
            "gui": LaunchConfiguration("gui"),
        }.items(),
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_share, "launch", "bringup_launch.py")
        ),
        launch_arguments={
            "map": LaunchConfiguration("map"),
            "params_file": os.path.join(nav_share, "config", "nav2_params.yaml"),
            "use_sim_time": "true",
            "autostart": "true",
        }.items(),
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=[
            "-d",
            os.path.join(nav2_share, "rviz", "nav2_default_view.rviz"),
        ],
        parameters=[{"use_sim_time": True}],
        output="screen",
    )

    return LaunchDescription([
        DeclareLaunchArgument("world", default_value="obstacles"),
        DeclareLaunchArgument("gui", default_value="true"),
        DeclareLaunchArgument(
            "map",
            default_value=os.path.join(nav_share, "maps", "obstacles.yaml"),
        ),
        sim,
        TimerAction(period=10.0, actions=[nav2, rviz]),
    ])