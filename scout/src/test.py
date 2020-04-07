import rospy
import random
from scout.msg import RL_input_msgs
from vlp_fir.msg import obs_info
from gazebo_msgs.msg import ContactsState
from geometry_msgs.msg import Twist

import numpy as np
import matplotlib.pyplot as plt

def col():
    print('info = ')
    data = rospy.wait_for_message('/bumper', ContactsState)
    if len(data.states):
        print('1:collide')
    else:
        print('1:save')
def odom():
    data = rospy.wait_for_message('RLin', RL_input_msgs)
    print('2:')
    print(data.obs_x[0])

for i in range(10000):
    rospy.init_node('testt', anonymous=True)
    col()
    odom()
