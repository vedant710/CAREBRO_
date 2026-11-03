"""custom_ekf_node: your own Extended Kalman Filter. YOUR CODE GOES HERE.

Inputs : /carebro_controller/odom (nav_msgs/Odometry), /imu/data_raw (sensor_msgs/Imu)
Output : /fusion/custom_ekf/odom (nav_msgs/Odometry)
State  : e.g. [x, y, yaw, v, w]. Predict with the motion model, update with IMU yaw rate
         and wheel velocities. Compare against robot_localization's /odometry/filtered.
"""


def main(args=None):
    pass


if __name__ == "__main__":
    main()
