import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    yaml_path = os.path.expanduser('~/localization.yaml')
    ublox_config_path = os.path.expanduser('~/ublox_config.yaml')
    python_script_path = os.path.expanduser('~/heading_to_imu.py')

    return LaunchDescription([
        # 1. GPS Node (Now loading your specific hardware configuration!)
        Node(
            package='ublox_gps',
            executable='ublox_gps_node',
            name='ublox_gps_node',
            parameters=[ublox_config_path],
            output='screen'
        ),

        # 2. Heading to IMU Python Script
        ExecuteProcess(
            cmd=['python3', python_script_path],
            output='screen'
        ),

        # 3. Static Transform (base_link -> gps)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['--x', '0', '--y', '0', '--z', '0', 
                       '--qx', '0', '--qy', '0', '--qz', '0', '--qw', '1', 
                       '--frame-id', 'base_link', '--child-frame-id', 'gps'],
            output='screen'
        ),

        # 4. EKF Filter Node
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            parameters=[yaml_path],
            output='screen'
        ),

        # 5. NavSat Transform Node
        Node(
            package='robot_localization',
            executable='navsat_transform_node',
            name='navsat_transform_node',
            parameters=[yaml_path],
            remappings=[
                ('imu', '/imu/data'),
                ('gps/fix', '/fix')
            ],
            output='screen'
        )
    ])
