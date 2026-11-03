"""encoder_odometry_node: odometry from raw encoder ticks. YOUR CODE GOES HERE.

Inputs : /encoders/left_ticks, /encoders/right_ticks (std_msgs/Int32, cumulative)
Output : /fusion/encoder_odom (nav_msgs/Odometry)
Needs  : ticks_per_rev (1320 in sim), wheel radius 0.033 m, wheel separation (see
         carebro_controller/config/carebro_controller.yaml). Diff-drive kinematics.
"""


def main(args=None):
    pass


if __name__ == "__main__":
    main()
