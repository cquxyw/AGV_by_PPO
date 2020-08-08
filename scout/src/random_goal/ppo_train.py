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
import csv

import subprocess
import ppo_algo
import ppo_env

import threading

EP_MAX = 1000000
EP_LEN = 480
BATCH = 64
GAMMA = 0.9
test = 0

METHOD = [
    dict(name='kl_pen', kl_target=0.01, lam=0.5),   # KL penalty
    dict(name='clip', epsilon=0.2),                 # Clipped surrogate objective, find this is better
][1]

# save rewards data as npy file of every train
def save_plot(ep, ep_r, TRAIN_TIME, PLOT_EPISODE, PLOT_REWARD):
    plot_path = 'Train_Result/single/img/PPO_final_%i.npy' %(TRAIN_TIME)
    PLOT_EPISODE = np.append(PLOT_EPISODE, ep)
    PLOT_REWARD = np.append(PLOT_REWARD, ep_r)
    PLOT_RESULT = np.concatenate([[PLOT_EPISODE], [PLOT_REWARD]])
    np.save(plot_path, PLOT_RESULT)
    return PLOT_EPISODE, PLOT_REWARD

# save the parameters as csv file of every train
def save_para(ppo, env, TRAIN_TIME):
    csvfile = open('Train_Result/single/img/PPO_final_para.csv', 'a+', newline='')
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
        PLOT_REWARD = np.array([], dtype = float)

        # if BREAK = 0, means action is not 'nan'.
        # if BREAK = 1, means action is 'nan', reset ppo and env to another train.
        BREAK = 0

        # 1. fix LR: Change LR in ppo_algo.py, and uncomment restore function.
        # 2. random LR: Change LR in ppo_algo.py, and conmment restore function.
        ppo = ppo_algo.ppo(TRAIN_TIME)
        print('\n Training Start')

        # 0: basic model
        ppo.restore(0)

        env = ppo_env.env()
        env.choose_goal(1)

        # save_para(ppo, env, TRAIN_TIME+1)

        all_ep_r = []

        for ep in range(EP_MAX):

            a_init = [0, 0]
            s = env.set_init_pose()

            goal_index = random.randint(0, 3)
            env.choose_goal(goal_index)
            print('Goal:%i,%i' %(env.goal_x,env.goal_y))
            env.gazebo_srv()
            
            last_u_state = s[7]
            # last_dis_from_des_point, last_dis_from_ori = env.compute_param()

            buffer_s = []
            buffer_a = []
            buffer_r = []

            ep_r = 0
            time.sleep(0.5)

            reach_time = 10

            for t in range(EP_LEN):

                a =  ppo.choose_action(s)

                if np.isnan(a[0]) or np.isnan(a[1]):
                    BREAK = 1

                    # record the information of nan situation in order to find out which part has problem
                    ppo.write_log(TRAIN_TIME, ep, t, a, s_, r)

                    print('Warning: Action is nan. Restart Train')
                    break
                    # os._exit(0)

                ap = env.set_action(a)
                # print('v: %f ; w: %f' %(ap[0],ap[1]))

                s_= env.compute_state()
                # print(s_)

                collide = s_[-1]
                current_dis_from_des_point = s_[28]
                current_dis_from_ori = s_[30]

                u_state = s_[27]
                # print('u_state: %f' %(u_state))
                d_u = last_u_state - u_state
                # print('d_u: %f' %(d_u))

                # collide, current_dis_from_des_point to judge whether it is end of episode
                r = env.compute_reward(collide, current_dis_from_des_point, current_dis_from_ori, d_u)
                # print('R:%f'%(r))

                last_u_state = u_state

                ppo.write_log(TRAIN_TIME, ep, t, a, s_, r)

                buffer_s.append(s)
                buffer_a.append(a)
                buffer_r.append((r+8)/8)

                s = s_
                ep_r += r
                
                # Batch end normally
                if (t+1) % BATCH == 0 or t == EP_LEN-1:
                    if test == 0:
                        update(ppo, s_, buffer_r, buffer_s, buffer_a)

                # Batch end with special behaviors
                if current_dis_from_des_point < env.reach_goal_circle:
                    print('Reach goal')
                    update(ppo, s_, buffer_r, buffer_s, buffer_a)
                    break
            
                if collide == 1:
                    update(ppo, s_, buffer_r, buffer_s, buffer_a)
                    print('Collision')
                    break

                if current_dis_from_ori > 12:
                    update(ppo, s_, buffer_r, buffer_s, buffer_a)
                    print('Out range')
                    break
            
            # Set the beginning action of robot in next episode, or it would be set by last time
            ap = env.set_action(a_init)

            # Print the result of episode reward
            if ep == 0: all_ep_r.append(ep_r)
            else: all_ep_r.append(all_ep_r[-1]*0.9 + ep_r*0.1)
            print(
                'Ep: %i' % ep,
                "|Ep_r: %.3f" % ep_r,
                ("|Lam: %.4f" % METHOD['lam']) if METHOD['name'] == 'kl_pen' else '',
            )

            # if ep_r > 0:
            #     if ppo.A_LR >= 1e-8:
            #         ppo.A_LR = ppo.A_LR * 0.99
            #     else:
            #         ppo.A_LR = 1e-8

            # Save reward data for plot
            PLOT_EPISODE, PLOT_REWARD = save_plot(ep, ep_r, TRAIN_TIME, PLOT_EPISODE, PLOT_REWARD)
            
            # Save model
            if ep % 20 == 0:
                ppo.save(TRAIN_TIME+1)

            # Reset gazebo environment
            env.reset_env()
            
            if BREAK == 1:
                break
        
        ppo.resetgraph()