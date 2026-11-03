"""Start everything with switches.

    ros2 launch carebro_bringup bringup.launch.py world:=obstacles nav_mode:=slam_nav
    ros2 launch carebro_bringup bringup.launch.py nav_mode:=navigation fusion:=true

nav_mode : sim         Gazebo + robot only
           navigation  saved map + AMCL + Nav2   (carebro_navigation/maps/obstacles.yaml)
           slam_nav    live SLAM + Nav2
sensors / fusion / perception / ai : true|false, started 20 s after the base system.
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

NAV_MODES = {
    "sim": ("carebro_gazebo", "sim.launch.py"),
    "navigation": ("carebro_navigation", "navigation.launch.py"),
    "slam_nav": ("carebro_navigation", "slam_navigation.launch.py"),
}


def _include(package, launch_file, arguments=None, condition=None):
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory(package), "launch", launch_file)
        ),
        launch_arguments=(arguments or {}).items(),
        condition=condition,
    )


def _launch_setup(context, *args, **kwargs):
    mode = LaunchConfiguration("nav_mode").perform(context)
    if mode not in NAV_MODES:
        raise RuntimeError(
            f"nav_mode must be one of {sorted(NAV_MODES)}, got '{mode}'"
        )
    package, launch_file = NAV_MODES[mode]

    base = _include(
        package,
        launch_file,
        {
            "world": LaunchConfiguration("world"),
            "gui": LaunchConfiguration("gui"),
        },
    )

    layers = TimerAction(
        period=20.0,
        actions=[
            _include("carebro_sensors", "sensors.launch.py",
                     condition=IfCondition(LaunchConfiguration("sensors"))),
            _include("carebro_sensor_fusion", "fusion.launch.py",
                     {"publish_tf": LaunchConfiguration("fusion_publish_tf")},
                     condition=IfCondition(LaunchConfiguration("fusion"))),
            _include("carebro_perception", "perception.launch.py",
                     condition=IfCondition(LaunchConfiguration("perception"))),
            _include("carebro_ai", "ai.launch.py",
                     condition=IfCondition(LaunchConfiguration("ai"))),
        ],
    )
    return [base, layers]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("world", default_value="obstacles"),
        DeclareLaunchArgument("nav_mode", default_value="slam_nav"),
        DeclareLaunchArgument("gui", default_value="true"),
        DeclareLaunchArgument("sensors", default_value="true"),
        DeclareLaunchArgument("fusion", default_value="false"),
        DeclareLaunchArgument("fusion_publish_tf", default_value="false"),
        DeclareLaunchArgument("perception", default_value="false"),
        DeclareLaunchArgument("ai", default_value="false"),
        OpaqueFunction(function=_launch_setup),
    ])
