"""imu_preprocessor_node: clean up the IMU. YOUR CODE GOES HERE.

Input  : /imu/data_raw
Output : /imu/data (sensor_msgs/Imu) with real covariances, gyro bias removed.
Why    : the Gazebo IMU reports zero covariance, so robot_localization treats it as
         perfect. Estimate bias while the robot is still, set covariances from the noise
         you measured, then point imu0 in config/ekf.yaml at /imu/data.
"""


def main(args=None):
    pass


if __name__ == "__main__":
    main()
