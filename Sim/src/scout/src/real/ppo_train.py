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

EP_MAX = 1000000
EP_LEN = 160
BATCH = 32
GAMMA = 0.9

METHOD = [
    dict(name='kl_pen', kl_target=0.01, lam=0.5),   # KL penalty
    dict(name='clip', epsilon=0.2),                 # Clipped surrogate objective, find this is better
][1]

# save rewards data as npy file of every train
def save_plot(ep, ep_r, TRAIN_TIME, PLOT_EPISODE, PLOT_REWARD):
    plot_path = '/home/xyw/Train_Result/real/PPO_%i.npy' %(TRAIN_TIME)
    PLOT_EPISODE = np.append(PLOT_EPISODE, ep)
    PLOT_REWARD = np.append(PLOT_REWARD, ep_r)
    PLOT_RESULT = np.concatenate([[PLOT_EPISODE], [PLOT_REWARD]])
    np.save(plot_path, PLOT_RESULT)
    return PLOT_EPISODE, PLOT_REWARD

def update(ppo, s_, buffer_r, buffer_s, buffer_a):

    v_s_ = ppo.get_v(s_)
    discounted_r = []
    for r in buffer_r[::-1]:
        v_s_ = r + GAMMA * v_s_
        discounted_r.append(v_s_)
    discounted_r.reverse()

    bs, ba, br = np.vstack(buffer_s), np.vstack(buffer_a), np.array(discounted_r)[:, np.newaxis]
    buffer_s = []
    buffer_a = []
    buffer_r = []
    
    ppo.update(bs, ba, br)
    
if __name__ == '__main__':
    rospy.init_node('RL', anonymous=True)

    for TRAIN_TIME in range(50):

        PLOT_EPISODE = np.array([],dtype = int)
        PLOT_REWARD = np.array([], dtype = int)

        # if BREAK = 0, means action is not 'nan'.
        # if BREAK = 1, means action is 'nan', reset ppo and env to another train.
        BREAK = 0

        # 1. fix LR: Change LR in ppo_algo.py, and uncomment restore function.
        # 2. random LR: Change LR in ppo_algo.py, and conmment restore function.
        ppo = ppo_algo.ppo()
        print('\n Training Start')

        ppo.restore(TRAIN_TIME)

        env = ppo_env.env()

        all_ep_r = []

        for ep in range(EP_MAX):
            a_init = [0, 0]
            s = env.set_init_pose()

            buffer_s = []
            buffer_a = []
            buffer_r = []

            ep_r = 0
            time.sleep(0.1)
             
            dis_temp = math.hypot(env.goal_x, env.goal_y)
            a_temp = [0,0]

            for t in range(EP_LEN):

                a =  ppo.choose_action(s)
                # print(ppo.get_v(s))
                if np.isnan(a[0]) or np.isnan(a[1]):
                    BREAK = 1
                    print('Warning: Action is nan. Restart Train')
                    break
                    # os._exit(0)
                env.set_action(a)

                s_= env.compute_state()

                collide = env.get_collision_info()
                overspeed, current_dis_from_des_point = env.compute_param()

                diff_a = np.linalg.norm(np.array(a)-np.array(a_temp))

                r = env.compute_reward(collide, overspeed, current_dis_from_des_point, dis_temp, diff_a)

                dis_temp = current_dis_from_des_point
                a_temp = a

                buffer_s.append(s)
                buffer_a.append(a)
                buffer_r.append((r+8)/8)    # normalize reward, find to be useful
                s = s_
                ep_r += r

                if (t+1) % BATCH == 0 or t == EP_LEN-1:
                    update(ppo, s_, buffer_r, buffer_s, buffer_a)
                    # print(ppo.alossr, ppo.clossr)
            
                # When robot is nearby the goal, skip to next episode
                if collide == 1:
                    update(ppo, s_, buffer_r, buffer_s, buffer_a)
                    # print(ppo.alossr, ppo.clossr)
                    print('Collision')
                    break
                
                if current_dis_from_des_point < env.reach_goal_circle:
                    update(ppo, s_, buffer_r, buffer_s, buffer_a)
                    # print(ppo.alossr, ppo.clossr)
                    print('Sucess')
                    break
                elif current_dis_from_des_point > env.limit_circle:
                    update(ppo, s_, buffer_r, buffer_s, buffer_a)
                    # print(ppo.alossr, ppo.clossr)
                    print('Over-area')
                    break

                # if speed is too high, skip to next episode
                # if overspeed > env.limit_overspeed:
                #     update(ppo, s_, buffer_r, buffer_s, buffer_a)
                #     print(ppo.alossr, ppo.clossr)
                #     print('Over-speed')
                #     break                   
            
            # Set the beginning action of robot in next episode, or it would be set by last time
            env.set_action(a_init)

            # Print the result of episode reward
            if ep == 0: all_ep_r.append(ep_r)
            else: all_ep_r.append(all_ep_r[-1]*0.9 + ep_r*0.1)
            print(
                'Ep: %i' % ep,
                "|Ep_r: %f" % ep_r,
                ("|Lam: %.4f" % METHOD['lam']) if METHOD['name'] == 'kl_pen' else '',
            )
            
            # Save model and plot
            PLOT_EPISODE, PLOT_REWARD = save_plot(ep, ep_r, TRAIN_TIME+1, PLOT_EPISODE, PLOT_REWARD)
            
            if ep % 50 == 0:
                 ppo.save(TRAIN_TIME+1)

            # Reset gazebo environment
            env.reset_env()
            
            if BREAK == 1:
                print(ppo.alossr, ppo.clossr)
                break
        
        ppo.resetgraph()
