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
    print('\n Navigation Start')

    ppo.restore(0)

    env = ppo_env.env(1)

    all_ep_r = []

    all_time = 0
    success_time = 0
    collision_time = 0
    over_area_time = 0

    for ep in range(EP_MAX):
        a_init = [0, 0]
        s = env.set_init_pose()

        ep_r = 0
        time.sleep(0.1)

        all_time += 1

        for t in range(EP_LEN):

            a =  ppo.choose_action(s)

            if np.isnan(a[0]) or np.isnan(a[1]):
                print('Warning: Action is nan. Restart Train')
                break

            env.set_action(a)

            s_= env.compute_state()

            collide = env.get_collision_info()
            overspeed, current_dis_from_des_point = env.compute_param()

            s = s_

            print('X误差:%f ; Y误差:%f; 航向角误差：%f' %(env.disturb_x, env.disturb_y, env.disturb_yaw))
            
            if t == EP_LEN-1:
                print('Nothing happen')
        
            if collide == 1:
                collision_time += 1
                print('Collision')
                break
            
            if current_dis_from_des_point < env.reach_goal_circle:
                success_time += 1
                print('Sucess')
                break
            elif current_dis_from_des_point > env.limit_circle:
                over_area_time += 1
                print('Over-area')
                break

        print("all_time: %d \n over_arer_time %d \n collision_time %d \n success_time %d"
        %(all_time, over_area_time, collision_time, success_time))

        env.set_action(a_init)

        # Reset gazebo environment
        env.reset_env()

        time.sleep(0.5)