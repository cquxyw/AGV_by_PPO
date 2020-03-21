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

PLOT_EPISODE = []
PLOT_REWARD = []
EP_MAX = 100000
EP_LEN = 400
GAMMA = 0.9

BATCH = 10
goal_x = 8
goal_y = 8
METHOD = [
    dict(name='kl_pen', kl_target=0.01, lam=0.5),   # KL penalty
    dict(name='clip', epsilon=0.2),                 # Clipped surrogate objective, find this is better
][1] 

def env(ppo, a, s, car_s):

    reward = 0
    over_v = 0
    over_w = 0

# Pubulish action
    # create publisher
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    pub_msg = Twist()

    # clip action
    print(a)
    if a[0] > 2:
        over_v = 2-a[0]
        a[0] = 2
    elif a[0] < 0:
        over_v = a[0]
        a[0] = 0

    if a[1] > 3.14:
        over_w = 3.14 - a[1]
        a[1] = 3.14
    elif a[1] < -3.14:
        over_w = a[1] - 3.14
        a[1] = -3.14
    
    overspeed = over_v + over_w

    # if action is nan, quit
    if np.isnan(a[0]):
        print('Crash: Action is NAN')
        os._exit(0)
    # if not, publish action to gazebo
    else:
        pub_msg.linear.x = a[0]
        pub_msg.angular.z = a[1]
        pub.publish(pub_msg)
#----------------------------------

    # get feedback data of car state 
    data = rospy.wait_for_message('RLin',RL_input_msgs)

    # evaluation index
    dis_t = (car_s[0]-goal_x)**2+(car_s[1]-goal_y)**2
    dis_t1 = (data.me_x-goal_x)**2+(data.me_y-goal_y)**2
    dis_diff = dis_t - dis_t1
    
    yaw_t = data.me_yaw
    yaw_goal = math.atan((goal_y - data.me_y)/(goal_x - data.me_x))
    yaw_diff = abs(yaw_goal - yaw_t)

    v_diff = abs(data.me_v - a[0])
    # ---------

    # define state
    car_s = np.array([data.me_x,data.me_y,data.me_yaw,data.me_v,data.me_w])
    s_ = np.array([dis_t1, overspeed])
    # ---------

    # define reward
    reward = - dis_t1 * 0.01 + dis_diff * 1 + overspeed * 1
    if dis_t1 < 0.1:
        reward = reward + 1000
    elif 0.1 < dis_t1 < 1:
        reward = reward + 50
    # ---------

    return s_, reward, car_s

def init():   
    data = rospy.wait_for_message('RLin',RL_input_msgs)

    # evaluation index
    dis_t1 = (data.me_x-goal_x)**2+(data.me_y-goal_y)**2
    overspeed = 0
    # ---------

    # define state
    car_s = np.array([data.me_x,data.me_y,data.me_yaw,data.me_v,data.me_w])
    s = np.array([dis_t1, overspeed])
    # ---------

    return s, car_s

if __name__ == '__main__':
    rospy.init_node('RL', anonymous=True)
    ppo = ppo_algo.ppo()
    all_ep_r = []
    ppo.restore()

    for ep in range(EP_MAX):
        s, car_s = init()
        buffer_s, buffer_a, buffer_r = [], [], []
        ep_r = 0
        time.sleep(1)

        for t in range(EP_LEN):
            a = ppo.choose_action(s)
            s_, r, car_s = env(ppo, a, s, car_s)
            buffer_s.append(s)
            buffer_a.append(a)
            buffer_r.append((r+8)/8)    # normalize reward, find to be useful
            s = s_
            ep_r += r

            # if (t+1) % BATCH == 0 or t == EP_LEN-1:
            if t % BATCH == 0 or t == EP_LEN-1:
                v_s_ = ppo.get_v(s_)
                discounted_r = []
                for r in buffer_r[::-1]:
                    v_s_ = r + GAMMA * v_s_
                    discounted_r.append(v_s_)
                discounted_r.reverse()

                bs, ba, br = np.vstack(buffer_s), np.vstack(buffer_a), np.array(discounted_r)[:, np.newaxis]
                buffer_s, buffer_a, buffer_r = [], [], []
                ppo.update(bs, ba, br)
        
            # When robot is nearby the goal, skip to next episode
            elif (car_s[0]-goal_x)**2+(car_s[1]-goal_y)**2 < 0.1:
                v_s_ = ppo.get_v(s_)
                discounted_r = []
                for r in buffer_r[::-1]:
                    v_s_ = r + GAMMA * v_s_
                    discounted_r.append(v_s_)
                discounted_r.reverse()

                bs, ba, br = np.vstack(buffer_s), np.vstack(buffer_a), np.array(discounted_r)[:, np.newaxis]
                buffer_s, buffer_a, buffer_r = [], [], []
                ppo.update(bs, ba, br)
                break

        # Set the beginning action of robot in next episode, or it would be set by last time
        ainit = [0, 0] 
        env(ppo, ainit, s_, car_s)

        # Print the result of episode reward
        if ep == 0: all_ep_r.append(ep_r)
        else: all_ep_r.append(all_ep_r[-1]*0.9 + ep_r*0.1)
        print(
            'Ep: %i' % ep,
            "|Ep_r: %i" % ep_r,
            ("|Lam: %.4f" % METHOD['lam']) if METHOD['name'] == 'kl_pen' else '',
        )
        
        # Plot results
        PLOT_EPISODE.append(ep)
        PLOT_REWARD.append(ep_r)
        plt.plot(PLOT_EPISODE, PLOT_REWARD, color="Blue")
        plt.title("TRAINNING RESULT")
        plt.xlabel("EPISODE")
        plt.ylabel("REWARD")
        
        # Save model and plot
        if ep % 100 == 0:
            plt.savefig('/home/xyw/BUAA/Graduation/src/scout/result/img/result.eps')
        if ep % 200 == 0:
            ppo.save(ep)

        # Reset gazebo environment
        subprocess.Popen(['rosservice','call','/gazebo/reset_world'])