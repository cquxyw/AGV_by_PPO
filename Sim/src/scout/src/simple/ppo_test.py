import rospy
import random

import tensorflow.compat.v1 as tf
import numpy as np
import time
import math
import os

# from gpstoenu.msg import enu
# from can_listener.msg import vel_can
from scout.msg import RL_input_msgs
from geometry_msgs.msg import Twist

import ppo_algo
import ppo_env
    
if __name__ == '__main__':

    rospy.init_node('RL')

    ppo = ppo_algo.ppo()
    env = ppo_env.env()
    
    print('\n Navigation Start')
    for i in range(1000):
        a_init = [0, 0]
        s = env.compute_state()

        s = env.set_init_pose()

        for i in range(320):
            
            start = time.clock()

            a =  ppo.choose_action(s)
            env.set_action(a)

            s_= env.compute_state()
            s = s_
            print("当前状态：")
            print(s)
            print("采取动作：线速度-%.1f;角速度-%.1f" %(a[0],a[1]))

            end = time.clock()
            print("耗时：%.3f" %(end-start))
        
        env.reset_env()