from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import LifecycleNode, Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import os

def generate_launch_description():
    # กำหนด path ของ package `med_bot`
    share_dir = get_package_share_directory('med_bot')

    # กำหนด path ของไฟล์พารามิเตอร์ X4-Pro.yaml
    parameter_file = LaunchConfiguration('params_file')

    # สร้าง argument สำหรับไฟล์พารามิเตอร์
    params_declare = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(share_dir, 'config', 'X4-Pro.yaml'),
        description='Path to the ROS2 parameters file to use.'
    )

    # Node สำหรับ YDLidar ROS2 driver (Lifecycle Node)
    driver_node = LifecycleNode(
        package='ydlidar_ros2_driver',
        executable='ydlidar_ros2_driver_node',
        name='ydlidar_ros2_driver_node',
        output='screen',
        emulate_tty=True,
        parameters=[parameter_file],
        namespace='/'
    )

    # Static Transform Publisher สำหรับ laser_frame
    tf2_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_pub_laser',
        arguments=['0', '0', '0.02', '0', '0', '0', '1', 'base_link', 'laser_frame'],
    )

    return LaunchDescription([
        params_declare,
        driver_node,
        tf2_node,
    ])
