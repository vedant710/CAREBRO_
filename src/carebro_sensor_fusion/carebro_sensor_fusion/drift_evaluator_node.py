"""drift_evaluator_node: measure drift against ground truth. YOUR CODE GOES HERE.

Inputs : /ground_truth/odom (Gazebo, WORLD frame), /carebro_controller/odom,
         /odometry/filtered, optionally /fusion/*  (all start at the robot spawn pose)
Output : position error [m], heading error [deg], RMSE; write a CSV for plots.
Note   : ground truth is in the world frame, the others start at (0,0,0). Subtract the
         pose at start (the spawn pose, e.g. -4,-4 in the obstacles world) before comparing.
"""


def main(args=None):
    pass


if __name__ == "__main__":
    main()
