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


EP_MAX = 3000
EP_LEN = 320
BATCH = 32
GAMMA = 0.9

METHOD = [
    dict(name='kl_pen', kl_target=0.01, lam=0.5),   # KL penalty
    dict(name='clip', epsilon=0.2),                 # Clipped surrogate objective, find this is better
][1]

# save rewards data as npy file of every train
def save_plot(ep, ep_r, TRAIN_TIME, PLOT_EPISODE, PLOT_REWARD):
    plot_path = '/home/xyw/BUAA/Graduation/src/scout/result/img/PPO_%i.npy' %(TRAIN_TIME)
    PLOT_EPISODE = np.append(PLOT_EPISODE, ep)
    PLOT_REWARD = np.append(PLOT_REWARD, ep_r)
    PLOT_RESULT = np.concatenate([PLOT_EPISODE, PLOT_REWARD])
    np.save(plot_path, PLOT_RESULT)
    return PLOT_EPISODE, PLOT_REWARD

# save the parameters as csv file of every train
def save_para(ppo, env, TRAIN_TIME):
    csvfile = open('/home/xyw/BUAA/Graduation/src/scout/result/img/PPO_para.csv', 'a+', newline='')
    writer = csv.writer(csvfile)
    data = ['%i' %(TRAIN_TIME), '%i' %(BATCH), '%.1e' %(ppo.A_LR), '%.1e' %(ppo.C_LR)]
    writer.writerow(data)
    csvfile.close()

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

        # 1. try to solve the problem of action non: fix LR in ppo_algo.py, and uncomment restore function.
        # 2. try to find suitable LR: random LR in ppo_algo.py, and conmment restore function.
        ppo = ppo_algo.ppo()
        # ppo.restore(TRAIN_TIME)
        env = ppo_env.env()

        save_para(ppo, env, TRAIN_TIME)

        all_ep_r = []

        for ep in range(EP_MAX):
            a_init = [0, 0]
            s = env.set_init_pose()

            buffer_s = []
            buffer_a = []
            buffer_r = []

            ep_r = 0
            time.sleep(0.1)

            for t in range(EP_LEN):

                a = ppo.choose_action(s)
                if np.isnan(a[0]) or np.isnan(a[1]):
                    BREAK = 1
                    break
                    # os._exit(0)
                env.set_action(a)

                s_= env.compute_state()
                r = env.compute_reward()

                overspeed, current_dis_from_des_point = env.compute_param()

                buffer_s.append(s)
                buffer_a.append(a)
                buffer_r.append((r+8)/8)    # normalize reward, find to be useful
                s = s_
                ep_r += r

                if (t+1) % BATCH == 0 or t == EP_LEN-1:
                    update(ppo, s_, buffer_r, buffer_s, buffer_a)
            
                # When robot is nearby the goal, skip to next episode
                if current_dis_from_des_point < env.reach_goal_circle or current_dis_from_des_point > env.limit_circle:
                    update(ppo, s_, buffer_r, buffer_s, buffer_a)
                    break

                # if speed is too high, skip to next episode
                if overspeed > env.limit_overspeed:
                    update(ppo, s_, buffer_r, buffer_s, buffer_a)
                    break
            
            # Set the beginning action of robot in next episode, or it would be set by last time
            env.set_action(a_init)

            # Print the result of episode reward
            if ep == 0: all_ep_r.append(ep_r)
            else: all_ep_r.append(all_ep_r[-1]*0.9 + ep_r*0.1)
            print(
                'Ep: %i' % ep,
                "|Ep_r: %i" % ep_r,
                ("|Lam: %.4f" % METHOD['lam']) if METHOD['name'] == 'kl_pen' else '',
            )
            
            # Save model and plot
            PLOT_EPISODE, PLOT_REWARD = save_plot(ep, ep_r, TRAIN_TIME, PLOT_EPISODE, PLOT_REWARD)
            if ep % 200 == 0:
                ppo.save(TRAIN_TIME)

            # Reset gazebo environment
            env.reset_env()
            if BREAK == 1:
                break

        if BREAK == 1:
            continue
