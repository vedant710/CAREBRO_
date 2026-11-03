"""object_detector_node: AI object detection. YOUR CODE GOES HERE.

Input  : /camera/color/image_raw (sensor_msgs/Image)
Output : /ai/detections (vision_msgs/Detection2DArray), /ai/debug_image (annotated)
Ideas  : YOLO (ultralytics / ONNX Runtime), put weights in the models/ folder.
CPU-only? use a small model and process every Nth frame.
"""


def main(args=None):
    pass


if __name__ == "__main__":
    main()
