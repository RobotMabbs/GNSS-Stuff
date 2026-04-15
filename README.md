To setup the GNSS ublox unit, plug in the USB port into the jon, and attach, or tape, the black antenna to the outside of the rover (ideally a flat and metal surface). 
The red GNSS board should also be firmly affixed to the rover, but it can be inside of the housing.  
First check that the device/port in ublox_config.yaml is correct, likely the port is correct, but change this:  
``device: "/dev/ttyACM0"``  
if needed. To see what ports are in use, use:  
``ls /dev/ttyACM*``  
To get all of the nodes and information publishing (make sure you are in the correct directory):     
``ros2 launch rover_bringup.launch.py``  
Sometimes this is a little finicky, and I think it might be a WSL problem. If this doesn't work, everything can be run individually.  
In seperate terminals run:  
``ros2 run ublox_gps ublox_gps_node --ros-args --params-file ublox_config.yaml``  
which sets up the GNSS, and publishes the /fix and /navpvt. Next:  
``python3 heading_to_imu.py``  
which translates to /imu/data. Then:  
``ros2 run tf2_ros static_transform_publisher --x 0 --y 0 --z 0 --qx 0 --qy 0 --qz 0 --qw 1 --frame-id base_link --child-frame-id gps``  
which combines everything and publishes /odom. Finally:  
``ros2 run robot_localization navsat_transform_node --ros-args --params-file localization.yaml --remap imu:=/imu/data --remap gps/fix:=/fix``
which will transform into X/Y coordinates.  
To see if everything is publishing right, check the ROS2 graph:  
``rqt_graph``  
Ideally if stuff is setup right everything should publish and be usable by the cost mapping stuff Logan set up, but be so fr that's prolly not gonna happen.
