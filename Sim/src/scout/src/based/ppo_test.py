import rospy
import random
from scout.msg import RL_input_msgs
from geometry_msgs.msg import Twist

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import os
import csv

import subprocess
import ppo_algo
import ppo_env


EP_MAX = 2000
EP_LEN = 160
BATCH = 32
GAMMA = 0.9

METHOD = [
    dict(name='kl_pen', kl_target=0.01, lam=0.5),   # KL penalty
    dict(name='clip', epsilon=0.2),                 # Clipped surrogate objective, find this is better
][1]
    
if __name__ == '__main__':
    rospy.init_node('RL', anonymous=True)

    ppo = ppo_algo.ppo()
    print('\n Training Start')

    ppo.restore(0)

    env = ppo_env.env()

    for ep in range(EP_MAX):
        a_init = [0, 0]
        s = env.set_init_pose()

        ep_r = 0
        time.sleep(0.1)

        for t in range(EP_LEN):

            start = time.clock()

            a =  ppo.choose_action(s)

            if np.isnan(a[0]) or np.isnan(a[1]):
                BREAK = 1
                print('Warning: Action is nan. Restart Train')
                break
                # os._exit(0)
            env.set_action(a)

            s_= env.compute_state()

            collide = env.get_collision_info()
            overspeed, current_dis_from_des_point = env.compute_param()

            s = s_

            end = time.clock()
            print("耗时：%.3f" %(end-start))

            if t == EP_LEN-1:
                print('Nothing happen')
                break
        
            # When robot is nearby the goal, skip to next episode
            if collide == 1:
                print('Collision')
                break
            
            if current_dis_from_des_point < env.reach_goal_circle:
                print('Sucess')
                break
            elif current_dis_from_des_point > env.limit_circle:
                print('Over-area')
                break               
        
        # Set the beginning action of robot in next episode, or it would be set by last time
        env.set_action(a_init)

        # Reset gazebo environment
        env.reset_env()
    
    ppo.resetgraph()
