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

import subprocess
import ppo_algo
import ppo_env

PLOT_EPISODE = []
PLOT_REWARD = []
EP_MAX = 100000
EP_LEN = 400
GAMMA = 0.9

BATCH = 20
goal_x = 8
goal_y = 8
METHOD = [
    dict(name='kl_pen', kl_target=0.01, lam=0.5),   # KL penalty
    dict(name='clip', epsilon=0.2),                 # Clipped surrogate objective, find this is better
][1]

def plot_result(ep, ep_r):
    PLOT_EPISODE.append(ep)
    PLOT_REWARD.append(ep_r)
    plt.plot(PLOT_EPISODE, PLOT_REWARD, color="Blue")
    plt.title("TRAINNING RESULT")
    plt.xlabel("EPISODE")
    plt.ylabel("REWARD")
    plt.savefig('/home/xyw/BUAA/Graduation/src/scout/result/img/result.eps')

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

    ppo = ppo_algo.ppo()
    ppo.restore()

    env = ppo_env.env()

    all_ep_r = []

    for ep in range(EP_MAX):
        a_init = [0, 0]
        s = env.set_init_pose

        buffer_s = []
        buffer_a = []
        buffer_r = []

        ep_r = 0
        time.sleep(1)

        for t in range(EP_LEN):

            a = ppo.choose_action(s)
            env.set_action(a)

            s_= env.compute_state()
            r = env.compute_reward()

            overspeed, current_dis_from_des_point = env.compute_param()

            buffer_s.append(s)
            buffer_a.append(a)
            buffer_r.append((r+8)/8)    # normalize reward, find to be useful
            s = s_
            ep_r += r

            # if (t+1) % BATCH == 0 or t == EP_LEN-1:
            if t % BATCH == 0 or t == EP_LEN - 1:
                update(ppo, s_, buffer_r, buffer_s, buffer_a)
        
            # When robot is nearby the goal, skip to next episode
            if current_dis_from_des_point < 0.1:
                update(ppo, s_, buffer_r, buffer_s, buffer_a)
                break

            # if speed is too high, skip to next episode
            if overspeed > 20:
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
        if ep % 20 == 0:
            plot_result(ep, ep_r)
        if ep % 200 == 0:
            ppo.save(ep)

        # Reset gazebo environment
        env.reset_env()