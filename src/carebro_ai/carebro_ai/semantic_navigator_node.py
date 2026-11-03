"""semantic_navigator_node: connect AI output to Nav2. YOUR CODE GOES HERE.

Inputs : /ai/detections, /camera/depth/image_rect_raw, TF (map -> camera_link)
Output : goals sent to Nav2 (nav2_msgs NavigateToPose action, or nav2_simple_commander)
Ideas  : "go to the chair": detection pixel + depth -> 3D point -> map frame -> goal a
         safe distance short of it. Cancel / replan when the detection changes.
"""


def main(args=None):
    pass


if __name__ == "__main__":
    main()
