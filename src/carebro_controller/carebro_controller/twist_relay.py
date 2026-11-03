#!/usr/bin/env python3
"""Relay geometry_msgs/Twist -> geometry_msgs/TwistStamped.

teleop_twist_keyboard and Nav2 publish plain Twist on /cmd_vel, while the
diff_drive_controller listens for TwistStamped on /carebro_controller/cmd_vel.
"""
import rclpy
from geometry_msgs.msg import Twist, TwistStamped
from rclpy.node import Node


class TwistRelay(Node):
    def __init__(self):
        super().__init__("twist_relay")
        self.declare_parameter("input_topic", "/cmd_vel")
        self.declare_parameter("output_topic", "/carebro_controller/cmd_vel")
        self.declare_parameter("frame_id", "base_footprint")

        in_topic = self.get_parameter("input_topic").value
        out_topic = self.get_parameter("output_topic").value
        self.frame_id_ = self.get_parameter("frame_id").value

        self.pub_ = self.create_publisher(TwistStamped, out_topic, 10)
        self.sub_ = self.create_subscription(Twist, in_topic, self.callback, 10)
        self.get_logger().info(f"Relaying Twist {in_topic} -> TwistStamped {out_topic}")

    def callback(self, msg: Twist):
        out = TwistStamped()
        out.header.stamp = self.get_clock().now().to_msg()
        out.header.frame_id = self.frame_id_
        out.twist = msg
        self.pub_.publish(out)


def main():
    rclpy.init()
    node = TwistRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == "__main__":
    main()
