import rospy
import random
from scout.msg import RL_input_msgs
from geometry_msgs.msg import Twist

import numpy as np
import matplotlib.pyplot as plt

def env(ppo, a, s, car_s):
    data = rospy.wait_for_message('RLin', RL_input_msgs)
    print('obs_x = ')
    print(data.obs_x)

if __name__ == '__main__':
    env()