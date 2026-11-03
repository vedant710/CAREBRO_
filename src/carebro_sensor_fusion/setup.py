import os
from glob import glob

from setuptools import find_packages, setup

package_name = "carebro_sensor_fusion"

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
    description="Sensor fusion for CareBro (EKF config + your algorithms).",
    license="MIT",
    entry_points={
        "console_scripts": [
            "custom_ekf_node = carebro_sensor_fusion.custom_ekf_node:main",
            "complementary_filter_node = carebro_sensor_fusion.complementary_filter_node:main",
            "encoder_odometry_node = carebro_sensor_fusion.encoder_odometry_node:main",
            "imu_preprocessor_node = carebro_sensor_fusion.imu_preprocessor_node:main",
            "drift_evaluator_node = carebro_sensor_fusion.drift_evaluator_node:main",
        ],
    },
)
