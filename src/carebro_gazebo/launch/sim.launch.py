"""Start Gazebo with a CareBro world, spawn the robot, bridge /scan + /clock,
start ros2_control (diff-drive) and optionally RViz.

Sensors bridged: /scan, /imu/data_raw, /ground_truth/odom and the RealSense-style
/camera/* topics (color, depth, camera_info, points).

    ros2 launch carebro_gazebo sim.launch.py world:=obstacles|warehouse|house

Humble -> Gazebo Fortress ("ignition"), Jazzy -> Gazebo Harmonic ("gz").
"""
import os
import tempfile
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
    RegisterEventHandler,
    SetEnvironmentVariable,
)
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

# world name -> default spawn pose (x, y, yaw)
WORLDS = {
    "obstacles": (-4.0, -4.0, 0.0),
    "warehouse": (-8.5, -5.5, 0.0),
    "house": (-3.0, -1.0, 0.0),
}


def _prepend_env(name, path):
    old = os.environ.get(name, "")
    return path + (os.pathsep + old if old else "")


def launch_setup(context, *args, **kwargs):
    ros_distro = os.environ.get("ROS_DISTRO", "humble")
    is_ignition = ros_distro == "humble"      # Fortress; anything newer -> Harmonic
    gz_prefix = "ignition" if is_ignition else "gz"

    desc_share = get_package_share_directory("carebro_description")
    gz_share = get_package_share_directory("carebro_gazebo")
    ctrl_share = get_package_share_directory("carebro_controller")

    # ---- world ---------------------------------------------------------
    world_arg = LaunchConfiguration("world").perform(context)
    if world_arg in WORLDS:
        world_file = os.path.join(gz_share, "worlds", f"{world_arg}.sdf")
        default_pose = WORLDS[world_arg]
    elif os.path.isfile(world_arg):                 # custom absolute path
        world_file, default_pose = world_arg, (0.0, 0.0, 0.0)
    else:
        raise RuntimeError(
            f"Unknown world '{world_arg}'. Use one of {sorted(WORLDS)} or an absolute .sdf path."
        )

    if not is_ignition:
        # The shipped worlds use Fortress plugin names; translate for Harmonic.
        text = Path(world_file).read_text()
        text = text.replace("ignition-gazebo-", "gz-sim-").replace("ignition::gazebo::", "gz::sim::")
        world_file = os.path.join(tempfile.gettempdir(), f"carebro_{Path(world_file).stem}_gz.sdf")
        Path(world_file).write_text(text)

    def pose(name, i):
        v = LaunchConfiguration(name).perform(context)
        return v if v != "" else str(default_pose[i])

    x, y, yaw = pose("x", 0), pose("y", 1), pose("yaw", 2)

    # ---- robot description --------------------------------------------
    robot_description = ParameterValue(
        Command([
            "xacro ",
            os.path.join(desc_share, "urdf", "carebro.urdf.xacro"),
            " is_ignition:=", "true" if is_ignition else "false",
        ]),
        value_type=str,
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
    )

    # ---- Gazebo --------------------------------------------------------
    # lets Gazebo resolve package://carebro_description/meshes/...
    resource_dir = str(Path(desc_share).parent.resolve())
    env_actions = [
        SetEnvironmentVariable("IGN_GAZEBO_RESOURCE_PATH", _prepend_env("IGN_GAZEBO_RESOURCE_PATH", resource_dir)),
        SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", _prepend_env("GZ_SIM_RESOURCE_PATH", resource_dir)),
    ]

    gz_args = f"-v 3 -r {world_file}"
    if LaunchConfiguration("gui").perform(context).lower() == "false":
        gz_args += " -s"                                # server only (headless)

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": gz_args}.items(),
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-topic", "robot_description", "-name", "carebro",
                   "-x", x, "-y", y, "-z", "0.02", "-Y", yaw],
    )

    # Gazebo -> ROS bridge. Camera topics are renamed to the names the real
    # realsense2_camera driver uses, so perception code ports to hardware unchanged.
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        output="screen",
        arguments=[
            f"/clock@rosgraph_msgs/msg/Clock[{gz_prefix}.msgs.Clock",
            f"/scan@sensor_msgs/msg/LaserScan[{gz_prefix}.msgs.LaserScan",
            f"/imu/data_raw@sensor_msgs/msg/Imu[{gz_prefix}.msgs.IMU",
            f"/ground_truth/odom@nav_msgs/msg/Odometry[{gz_prefix}.msgs.Odometry",
            f"/camera/image@sensor_msgs/msg/Image[{gz_prefix}.msgs.Image",
            f"/camera/depth_image@sensor_msgs/msg/Image[{gz_prefix}.msgs.Image",
            f"/camera/camera_info@sensor_msgs/msg/CameraInfo[{gz_prefix}.msgs.CameraInfo",
            f"/camera/points@sensor_msgs/msg/PointCloud2[{gz_prefix}.msgs.PointCloudPacked",
        ],
        remappings=[
            ("/camera/image", "/camera/color/image_raw"),
            ("/camera/depth_image", "/camera/depth/image_rect_raw"),
            ("/camera/camera_info", "/camera/color/camera_info"),
            ("/camera/points", "/camera/depth/color/points"),
        ],
    )

    # ---- ros2_control (start once the robot exists in Gazebo) ------------
    joint_state_broadcaster = Node(
        package="controller_manager", executable="spawner",
        arguments=["joint_state_broadcaster",
                   "--controller-manager", "/controller_manager",
                   "--controller-manager-timeout", "60"],
    )
    diff_drive = Node(
        package="controller_manager", executable="spawner",
        arguments=["carebro_controller",
                   "--controller-manager", "/controller_manager",
                   "--controller-manager-timeout", "60"],
    )
    twist_relay = Node(
        package="carebro_controller", executable="twist_relay",
        parameters=[{"use_sim_time": True}],
    )
    start_controllers = RegisterEventHandler(
        OnProcessExit(target_action=spawn_robot,
                      on_exit=[joint_state_broadcaster, diff_drive, twist_relay])
    )

    rviz = Node(
        package="rviz2", executable="rviz2", output="screen",
        arguments=["-d", os.path.join(gz_share, "rviz", "sim.rviz")],
        parameters=[{"use_sim_time": True}],
        condition=IfCondition(LaunchConfiguration("rviz")),
    )

    return env_actions + [
        robot_state_publisher, gazebo, spawn_robot, bridge, start_controllers, rviz,
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("world", default_value="obstacles",
                              description="obstacles | warehouse | house | /abs/path/to/world.sdf"),
        DeclareLaunchArgument("x", default_value="", description="spawn x (default: per world)"),
        DeclareLaunchArgument("y", default_value="", description="spawn y (default: per world)"),
        DeclareLaunchArgument("yaw", default_value="", description="spawn yaw in rad (default: per world)"),
        DeclareLaunchArgument("rviz", default_value="true", description="open RViz"),
        DeclareLaunchArgument("gui", default_value="true", description="open the Gazebo GUI (false = headless)"),
        OpaqueFunction(function=launch_setup),
    ])
