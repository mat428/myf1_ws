import os

# Find the installed location of a ROS2 package
from ament_index_python.packages import get_package_share_directory

# Used to create and return a launch file
from launch import LaunchDescription

# Used to launch ROS2 nodes
from launch_ros.actions import Node

# Converts a Xacro file into a URDF
import xacro


def generate_launch_description():

    # Package name
    pkg_name = 'articubot_one'

    # Path to the robot Xacro file
    xacro_file = os.path.join(
        get_package_share_directory(pkg_name),
        'description',
        'examplerobotdescription.urdf.xacro'
    )

    # Convert Xacro to URDF XML
    robot_description = {
        'robot_description': xacro.process_file(xacro_file).toxml()
    }

    # Publishes the robot TF tree from the URDF
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # Publishes joint angles using sliders
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )

    # Opens RViz for visualization
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen'
    )

    # Launch all three nodes
    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])