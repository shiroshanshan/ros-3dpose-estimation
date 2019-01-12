import os
import rospy
from std_msgs.msg import String

def take_last(element):
    return int(element.split('_')[1])

def talker():
    TEST_PATH = '/home/fan/generate-motion-from-roadmap/openpose/1533631208/00/'
    rospy.init_node('openpose_publisher', anonymous=True)
    str_pub = rospy.Publisher('/openpose/test', String, queue_size=10)
    rate = rospy.Rate(3)
    fs = os.listdir(TEST_PATH)
    fs.sort(key=take_last)
    idx = 0
    while idx < len(fs) and not rospy.is_shutdown():
        try:
            with open(TEST_PATH + fs[idx], 'r') as f:
                data = f.read()
                data = eval(data)['people'][0]['pose_keypoints_2d']
                data = [data[i] for i in range(len(data)) if (i-2) % 3 != 0]
            str_pub.publish(str(data))
            print('openpose message publishing...')
            rate.sleep()
            idx += 1
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
