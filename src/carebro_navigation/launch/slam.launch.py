import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    gz_share = get_package_share_directory("carebro_gazebo")
    nav_share = get_package_share_directory("carebro_navigation")
    slam_share = get_package_share_directory("slam_toolbox")

    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gz_share, "launch", "sim.launch.py")
        ),
        launch_arguments={
            "world": LaunchConfiguration("world"),
            "rviz": LaunchConfiguration("rviz"),
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

    return LaunchDescription([
        DeclareLaunchArgument("world", default_value="obstacles"),
        DeclareLaunchArgument("rviz", default_value="true"),
        DeclareLaunchArgument("gui", default_value="true"),
        sim,
        TimerAction(period=10.0, actions=[slam]),
    ])