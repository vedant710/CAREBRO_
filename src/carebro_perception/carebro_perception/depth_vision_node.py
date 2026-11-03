"""depth_vision_node: depth vision. YOUR CODE GOES HERE.

Inputs:
  /camera/depth/image_rect_raw  sensor_msgs/Image
        simulation: 32FC1 in metres.  real RealSense: 16UC1 in millimetres -> handle both.
  /camera/color/camera_info     intrinsics (depth is pixel-aligned with colour)
Ideas: nearest-obstacle distance, cliff / step detection, floor-plane segmentation,
free-space estimation. Suggested output: /perception/depth/min_distance (std_msgs/Float32).
"""


def main(args=None):
    pass


if __name__ == "__main__":
    main()
