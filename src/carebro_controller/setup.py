import os
from glob import glob

from setuptools import find_packages, setup

package_name = "carebro_controller"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Vedant Kulkarni",
    maintainer_email="vedantkulkarni252@gmail.com",
    description="ros2_control diff-drive config and Twist relay for CareBro.",
    license="MIT",
    entry_points={
        "console_scripts": [
            "twist_relay = carebro_controller.twist_relay:main",
        ],
    },
)
