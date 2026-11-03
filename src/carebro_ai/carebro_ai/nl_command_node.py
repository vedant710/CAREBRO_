"""nl_command_node: natural-language commands. YOUR CODE GOES HERE.

Input  : /ai/command (std_msgs/String), e.g. "go to the kitchen then the dock"
Output : goals for semantic_navigator_node (e.g. /ai/goal_name), or Nav2 directly.
Ideas  : an LLM API or local model turns the text into a list of location names that
         exist in carebro_waypoints/config/locations.yaml. Validate the names!
"""


def main(args=None):
    pass


if __name__ == "__main__":
    main()
