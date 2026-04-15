import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from ublox_msgs.msg import NavPVT
import math

class HeadingToImuNode(Node):
    def __init__(self):
        super().__init__('heading_to_imu_node')
        self.subscription = self.create_subscription(NavPVT, '/navpvt', self.navpvt_callback, 10)
        self.publisher = self.create_publisher(Imu, '/imu/data', 10)
        self.get_logger().info("Heading translator node actively running (with fixed covariance)...")

    def navpvt_callback(self, msg):
        imu_msg = Imu()
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = 'gps' 
        
        heading_deg = msg.heading / 100000.0
        yaw_rad = math.radians(heading_deg)
        
        imu_msg.orientation.x = 0.0
        imu_msg.orientation.y = 0.0
        imu_msg.orientation.z = math.sin(yaw_rad / 2.0)
        imu_msg.orientation.w = math.cos(yaw_rad / 2.0)
        
        # THE FIX: Replace -1.0 with 9999.9 (high uncertainty) for Roll/Pitch. 
        # Keep Yaw (index 8) at 0.01 (high certainty).
        imu_msg.orientation_covariance = [
            9999.9, 0.0,    0.0,
            0.0,    9999.9, 0.0,
            0.0,    0.0,    0.01
        ]
        
        # Do the same for angular velocity and linear acceleration
        imu_msg.angular_velocity_covariance = [
            9999.9, 0.0, 0.0, 
            0.0, 9999.9, 0.0, 
            0.0, 0.0, 9999.9
        ]
        imu_msg.linear_acceleration_covariance = [
            9999.9, 0.0, 0.0, 
            0.0, 9999.9, 0.0, 
            0.0, 0.0, 9999.9
        ]
        
        self.publisher.publish(imu_msg)

def main(args=None):
    rclpy.init(args=args)
    node = HeadingToImuNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
