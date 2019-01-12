import rospy
import cv2
import argparse
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge, CvBridgeError

def talker():
    rospy.init_node('camera_publisher', anonymous=True)
    img_pub = rospy.Publisher('webcam/image_raw',Image,queue_size=2)
    rate = rospy.Rate(1)
#     cap = cv2.VideoCapture('video/mp4/$TIMESTAMP.mp4')
    cap = cv2.VideoCapture(VIDEO_PATH)
    bridge = CvBridge()
    if not cap.isOpened():
        print("-------------------Webcam file is not existed-----------------------")
        return -1
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if ret:
            msg = bridge.cv2_to_imgmsg(frame,encoding="bgr8")
            img_pub.publish(msg)
            print('--------------------------------- publishing ---------------------------------')
        else:
            print('--------------------------------- read file failed ---------------------------------')
        rate.sleep()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='node that can publish photos from video sequence')
    parser.add_argument('-p', '--path', dest='path', type=str,
                        default='/home/fan/Documents/video/20180718131734.webm',
                        help='just input the path of your video')
    args = parser.parse_args()
    VIDEO_PATH = args.path
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
