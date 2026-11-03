"""Spawn joint_state_broadcaster + the diff-drive controller and the Twist relay.

sim.launch.py already includes this; run it on its own only if Gazebo is
already up with the robot spawned.
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager", "/controller_manager",
            "--controller-manager-timeout", "60",
        ],
    )

    wheel_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "carebro_controller",
            "--controller-manager", "/controller_manager",
            "--controller-manager-timeout", "60",
        ],
    )

    twist_relay = Node(
        package="carebro_controller",
        executable="twist_relay",
        parameters=[{"use_sim_time": True}],
    )

    return LaunchDescription(
        [joint_state_broadcaster_spawner, wheel_controller_spawner, twist_relay]
    )
