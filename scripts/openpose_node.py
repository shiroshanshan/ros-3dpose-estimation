import rospy
import cv2
import numpy as np
from select import OpenposeData
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import sys
sys.path.append("/home/fan/openpose_ws/openpose/build/python/openpose")
try:
    from openpose import *
except:
    raise Exception('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')

params = dict()
params["logging_level"] = 3
params["output_resolution"] = "-1x-1"
params["net_resolution"] = "-1x368"
params["model_pose"] = "COCO"
params["alpha_pose"] = 0.6
params["scale_gap"] = 0.3
params["scale_number"] = 1
params["render_threshold"] = 0.05
# If GPU version is built, and multiple GPUs are available, set the ID here
params["num_gpu_start"] = 0
params["disable_blending"] = False
# Ensure you point to the correct path where models are located
params["default_model_folder"] = dir_path + "/../../../models/"
# Construct OpenPose object allocates GPU memory

DIR = '/home/fan/mmd-interaction-rosmaster/openpose/'
bridge = CvBridge()

def camera_callback(data):
    # try:
    openpose = OpenPose(params)
    cv_image = bridge.imgmsg_to_cv2(data,"bgr8")
    size = cv_image.shape
    print('---------------------------------image processing---------------------------------')
    keypoints = openpose.forward(cv_image, False)
    print('output data shape:{0}'.format(keypoints.shape))
    openposedata = OpenposeData(keypoints)
    selected_data = openposedata.openpose_select()
    if type(selected_data) == str: #error
        pub = rospy.Publisher('/openpose/output', String, queue_size=10)
        pub.publish(selected_data)
        print(selected_data)
    else:
        pub = rospy.Publisher('/openpose/output', String, queue_size=10)
        pub.publish(np.array2string(selected_data[:,:2],separator=','))
        print('---------------------------------data publishing---------------------------------')

    # cv2.imshow("output", output_image)
    # cv2.waitKey(15)
    # except:
    #     print('processing failed')

def listener():
    rospy.init_node('camera_listener',anonymous=True)
    rospy.Subscriber('/webcam/image_raw',Image,camera_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
