"""Simulated motor encoders.

Real encoders give integer tick counts, not radians. This node turns the simulated
wheel joint angles (/joint_states, i.e. what Gazebo / ros2_control know) into
quantised tick counts, optionally with Gaussian noise, so your sensor-fusion code
sees the same kind of data a real robot would produce.

  subscribes: /joint_states                (sensor_msgs/JointState)
  publishes : /encoders/left_ticks         (std_msgs/Int32)  cumulative count
              /encoders/right_ticks        (std_msgs/Int32)  cumulative count

Parameters: left_joint, right_joint, ticks_per_rev, noise_std_ticks
(see config/encoders.yaml).
"""
import math
import random

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Int32


class EncoderSim(Node):
    def __init__(self):
        super().__init__("encoder_sim")
        self.declare_parameter("left_joint", "wheel_left_joint")
        self.declare_parameter("right_joint", "wheel_right_joint")
        self.declare_parameter("ticks_per_rev", 1320)
        self.declare_parameter("noise_std_ticks", 0.0)

        self._left = self.get_parameter("left_joint").value
        self._right = self.get_parameter("right_joint").value
        self._ticks_per_rev = float(self.get_parameter("ticks_per_rev").value)
        self._noise = float(self.get_parameter("noise_std_ticks").value)

        self._pub_left = self.create_publisher(Int32, "encoders/left_ticks", 10)
        self._pub_right = self.create_publisher(Int32, "encoders/right_ticks", 10)
        self.create_subscription(JointState, "joint_states", self._on_joint_state, 10)
        self.get_logger().info(
            f"encoder_sim: {self._ticks_per_rev:.0f} ticks/rev, noise {self._noise} ticks"
        )

    def _to_ticks(self, angle_rad):
        ticks = angle_rad / (2.0 * math.pi) * self._ticks_per_rev
        if self._noise > 0.0:
            ticks += random.gauss(0.0, self._noise)
        return int(round(ticks))

    def _on_joint_state(self, msg):
        angles = dict(zip(msg.name, msg.position))
        if self._left in angles:
            self._pub_left.publish(Int32(data=self._to_ticks(angles[self._left])))
        if self._right in angles:
            self._pub_right.publish(Int32(data=self._to_ticks(angles[self._right])))


def main(args=None):
    rclpy.init(args=args)
    node = EncoderSim()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
