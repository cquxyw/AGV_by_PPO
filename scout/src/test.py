import rospy
import random
from scout.msg import RL_input_msgs
from vlp_fir.msg import obs_info
from gazebo_msgs.msg import ContactsState
from geometry_msgs.msg import Twist

import numpy as np
import matplotlib.pyplot as plt

for i in range(10000):
    rospy.init_node('testt', anonymous=True)
    print('info = ')
    data = rospy.wait_for_message('/bumper', ContactsState)
    if len(data.states):
        print('collide')
    else:
        print('save')