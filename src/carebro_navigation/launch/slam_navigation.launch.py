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
    slam_share = get_package_share_directory("slam_toolbox")

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

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_share, "launch", "online_async_launch.py")
        ),
        launch_arguments={
            "slam_params_file": os.path.join(
                nav_share, "config", "slam_toolbox_mapping.yaml"
            ),
            "use_sim_time": "true",
        }.items(),
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_share, "launch", "navigation_launch.py")
        ),
        launch_arguments={
            "params_file": os.path.join(nav_share, "config", "nav2_params.yaml"),
            "use_sim_time": "true",
            "autostart": "true",
            "use_composition": "True",
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
        sim,
        TimerAction(period=10.0, actions=[slam]),
        TimerAction(period=15.0, actions=[nav2, rviz]),
    ])