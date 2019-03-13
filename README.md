# ros-3dpose-estimation
extract 3d joint position from one RGB camera in realtime

## dependency
* [rospy](http://wiki.ros.org/ja)
* [openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
* [3d-pose-baseline](https://github.com/una-dinosauria/3d-pose-baseline)

## node introduction
* **video publisher**: a node that can publish frames from video
* **openpose_node**: subscribe message from **video_publisher** and publish 2d joint position
* **3d-pose-estimation node**: subscribe message from **openpose_node** and publish 3d joint position
