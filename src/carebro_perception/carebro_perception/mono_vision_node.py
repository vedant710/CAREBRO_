"""mono_vision_node: monocular (RGB-only) vision. YOUR CODE GOES HERE.

Inputs (same names as the real RealSense driver):
  /camera/color/image_raw     sensor_msgs/Image   (rgb8, 640x480 in sim)
  /camera/color/camera_info   sensor_msgs/CameraInfo
Ideas: ORB/feature tracking, visual odometry, ArUco / dock-marker detection, line or
colour segmentation. Suggested output: /perception/mono/debug_image (sensor_msgs/Image).
"""


def main(args=None):
    pass


if __name__ == "__main__":
    main()
