import rospy
import random
from scout.msg import RL_input_msgs
from vlp_fir.msg import obs_info
from gazebo_msgs.msg import ContactsState
from geometry_msgs.msg import Twist

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# def col():
#     print('info = ')
#     data = rospy.wait_for_message('/bumper', ContactsState)
#     if len(data.states):
#         print('1:collide')
#     else:
#         print('1:save')
# def odom():
#     data = rospy.wait_for_message('obj_', obs_info)
#     print('2:')
#     print(data)

# for i in range(10000):
#     rospy.init_node('testt', anonymous=True)
#     col()
#     odom()

a = np.full([1,5], np.nan)

with tf.Session() as sess:  
    print(sess.run(tf.clip_by_value(1, 2, 5)))
