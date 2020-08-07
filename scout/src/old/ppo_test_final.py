import rospy
import random
from scout.msg import RL_input_msgs
from geometry_msgs.msg import Twist
from visualization_msgs.msg import Marker

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import os

import subprocess
import ppo_algo_final as ppo_algo
import ppo_env_final as ppo_env

EP_MAX = 1000000
EP_LEN = 640
BATCH = 64
GAMMA = 0.9
test = 0

METHOD = [
    dict(name='kl_pen', kl_target=0.01, lam=0.5),   # KL penalty
    dict(name='clip', epsilon=0.2),                 # Clipped surrogate objective, find this is better
][1]
    
if __name__ == '__main__':
    rospy.init_node('RL', anonymous=True)

    for TRAIN_TIME in range(50):

        BREAK = 0

        ppo = ppo_algo.ppo(TRAIN_TIME)

        # 0: basic model
        ppo.restore(10)
        env = ppo_env.env()
        env.choose_goal(0)

        for ep in range(EP_MAX):
            a_init = [0, 0]
            # env.reset_env()
        
            goal_index = 1

            goal_input = eval(input("请输您想要去的目的地："))
            env.goal_x = goal_input[0]
            env.goal_y = goal_input[1]
            env.gazebo_srv()
            print("输入目的地为：%i, %i；任务开始" %(env.goal_x, env.goal_y))

            s = env.set_init_pose()

            last_u_state = s[7]

            buffer_s = []
            buffer_a = []
            buffer_r = []

            ep_r = 0
            time.sleep(0.5)

            for t in range(EP_LEN):

                a =  ppo.choose_action(s)

                if np.isnan(a[0]) or np.isnan(a[1]):
                    BREAK = 1
                    print('Warning: Action is nan. Restart Train')
                    break

                ap = env.set_action(a)

                s_= env.compute_state()
                s = s_

                collide = s_[-1]
                current_dis_from_des_point = s_[28]
                current_dis_from_ori = s_[30]

                # ppo.write_log(TRAIN_TIME, ep, t, a, s_, r)
                if t == EP_LEN-1:
                    print('任务超时')
                    time.sleep(2)
                    break

                if current_dis_from_des_point < env.reach_goal_circle:
                    if not goal_index == 0:
                        print('到达目的地，即将开始返程')
                        time.sleep(2)
                        goal_index = 0
                        env.choose_goal(goal_index)
                        continue
                    else:
                        print('已返程，任务完成')
                        time.sleep(2)
                        break
            
                if collide == 1:
                    print('发生碰撞，任务失败')
                    break

                if current_dis_from_ori > 12:
                    time.sleep(2)
                    print('超出行驶区域，任务失败')
                    break
            
            # Set the beginning action of robot in next episode, or it would be set by last time
            ap = env.set_action(a_init)

            # print(
            #     'Ep: %i' % ep,
            #     "|Ep_r: %.3f" % ep_r,
            #     ("|Lam: %.4f" % METHOD['lam']) if METHOD['name'] == 'kl_pen' else '',
            # )

            # Reset gazebo environment
            env.reset_env()
            
            if BREAK == 1:
                break
        
        ppo.resetgraph()