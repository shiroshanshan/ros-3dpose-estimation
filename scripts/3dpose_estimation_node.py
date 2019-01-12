import sys
PATH = "/home/fan/3d-pose-baseline-master/"
sys.path.append(PATH + 'src')
from predict_3dpose import create_model
from std_msgs.msg import String
import data_utils
import cameras
import numpy as np
import tensorflow as tf
import rospy
import os

os.chdir('/home/fan/3d-pose-baseline-master/')
print('reading data, please wait...')
FLAGS = tf.app.flags.FLAGS

enc_in = np.zeros((1, 64))
enc_in[0] = [0 for i in range(64)]

actions = data_utils.define_actions(FLAGS.action)

order = [15, 12, 25, 26, 27, 17, 18, 19, 1, 2, 3, 6, 7, 8]

SUBJECT_IDS = [1, 5, 6, 7, 8, 9, 11]
rcams = cameras.load_cameras(FLAGS.cameras_path, SUBJECT_IDS)
train_set_2d, test_set_2d, data_mean_2d, data_std_2d, dim_to_ignore_2d, dim_to_use_2d = data_utils.read_2d_predictions(
    actions, FLAGS.data_dir)
train_set_3d, test_set_3d, data_mean_3d, data_std_3d, dim_to_ignore_3d, dim_to_use_3d, train_root_positions, test_root_positions = data_utils.read_3d_data(
    actions, FLAGS.data_dir, FLAGS.camera_frame, rcams, FLAGS.predict_14)
print('######reading data finished!######')

device_count = {"GPU": 1}

def callback(data):
    if data.data == 'hello':
        print(data.data)
    else:
        global FLAGS
        global enc_in
        global actions
        global order
        global SUBJECT_IDS
        global rcams
        global train_set_2d, test_set_2d, data_mean_2d, data_std_2d, dim_to_ignore_2d, dim_to_use_2d
        global train_set_3d, test_set_3d, data_mean_3d, data_std_3d, dim_to_ignore_3d, dim_to_use_3d, train_root_positions, test_root_positions
        global device_count

        input_data = np.array(eval(data.data))
        print('input data shape:{0}'.format(input_data.shape))
        tf.reset_default_graph()
        with tf.Session(config=tf.ConfigProto(
                device_count=device_count,
                allow_soft_placement=True)) as sess:
            batch_size = 128
            model = create_model(sess, actions, batch_size)
            # map list into np array
            joints_array = np.zeros((1, 36))
            joints_array[0] = [0 for i in range(36)]
            for o in range(len(joints_array[0])):
                #feed array with xy array
                joints_array[0] = input_data.flatten()
            _data = joints_array[0]
            # mapping all body parts or 3d-pose-baseline format
            for i in range(len(order)):
                for j in range(2):
                    # create encoder input
                    enc_in[0][order[i] * 2 + j] = _data[i * 2 + j]
            for j in range(2):
                # Hip
                enc_in[0][0 * 2 + j] = (enc_in[0][1 * 2 + j] + enc_in[0][6 * 2 + j]) / 2
                # Neck/Nose
                enc_in[0][14 * 2 + j] = (enc_in[0][15 * 2 + j] + enc_in[0][12 * 2 + j]) / 2
                # Thorax
                enc_in[0][13 * 2 + j] = 2 * enc_in[0][12 * 2 + j] - enc_in[0][14 * 2 + j]

                # set spine
            spine_x = enc_in[0][24]
            spine_y = enc_in[0][25]

            enc_in = enc_in[:, dim_to_use_2d]
            mu = data_mean_2d[dim_to_use_2d]
            stddev = data_std_2d[dim_to_use_2d]
            enc_in = np.divide((enc_in - mu), stddev)

            dp = 1.0
            dec_out = np.zeros((1, 48))
            dec_out[0] = [0 for i in range(48)]
            _, _, poses3d = model.step(sess, enc_in, dec_out, dp, isTraining=False)
            enc_in = data_utils.unNormalizeData(enc_in, data_mean_2d, data_std_2d, dim_to_ignore_2d)
            poses3d = data_utils.unNormalizeData(poses3d, data_mean_3d, data_std_3d, dim_to_ignore_3d)

        print('output data shape:{0}'.format(poses3d.shape))

def listener():

    rospy.init_node('preprocess_listener',anonymous=True)
    rospy.Subscriber('/openpose/test',String,callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        os.environ["TF_CPP_MIN_LOG_LEVEL"]='3'
        listener()
    except rospy.ROSInterruptException:
        pass
