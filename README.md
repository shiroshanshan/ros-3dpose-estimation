# ros-3dpose-estimation
# the system can extract 3d position from video per frame
## dependency
* 3d-pose-baseline
* ros
* openpose
## node introduction
* video publisher: a node used to publish frames from video
* openpose_node: receive frame message and extract 2d position then publish
* 3d-pose-estimation node: receive 2d pose message and estimate 3d position from 2d position then publish it 
