"""obstacle_cloud_node: obstacles for Nav2 from the point cloud. YOUR CODE GOES HERE.

Input : /camera/depth/color/points  sensor_msgs/PointCloud2  (frame: camera_link)
Goal  : find obstacles the 2D LiDAR plane (z ~ 0.13 m) cannot see (low or overhanging),
        then publish /perception/obstacle_points (PointCloud2) or
        /perception/obstacle_scan (LaserScan) and add it as an observation source in the
        Nav2 costmap (config/nav2_params.yaml) when you are ready.
"""


def main(args=None):
    pass


if __name__ == "__main__":
    main()
