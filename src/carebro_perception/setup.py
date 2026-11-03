import os
from glob import glob

from setuptools import find_packages, setup

package_name = "carebro_perception"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Vedant Kulkarni",
    maintainer_email="vedantkulkarni252@gmail.com",
    description="Perception algorithms for CareBro (mono + depth vision).",
    license="MIT",
    entry_points={
        "console_scripts": [
            "mono_vision_node = carebro_perception.mono_vision_node:main",
            "depth_vision_node = carebro_perception.depth_vision_node:main",
            "obstacle_cloud_node = carebro_perception.obstacle_cloud_node:main",
        ],
    },
)
