import rospy
from scout.msg import RL_input_msgs
from geometry_msgs.msg import Twist
from vlp_fir.msg import obs_info
from gazebo_msgs.msg import ContactsState

import tensorflow as tf
import numpy as np
import math
import os
import random

import subprocess

PI = 3.1415926

class env(object):

    def __init__(self, disturb):
        self.limit_v = 1.5
        self.limit_w = 0.785

        self.goal_x = 6
        self.goal_y = 0

        self.limit_circle = 12
        self.reach_goal_circle = 0.8
            
        self.disturb = disturb 
        self.disturb_x = 0
        self.disturb_y = 0
        self.disturb_yaw = 0
            
    def set_action(self, action):
        # set publisher
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        pub_msg = Twist()
        # print(action)
        
        # clip action
        action[0] = np.clip(action[0], -self.limit_v, self.limit_v)
        action[1] = np.clip(action[1], -self.limit_w, self.limit_w)


        # publish action
        if not np.isnan(action[0]) or np.isnan(action[1]):
            pub_msg.linear.x = action[0]
            pub_msg.angular.z = action[1]
            pub.publish(pub_msg)
        else:
            print('Warning: Action is NAN')

    def get_robot_info(self):
        data = rospy.wait_for_message('RLin', RL_input_msgs)
        current_state_info = np.array([data.me_x, data.me_y, 8, data.me_v, data.me_w])
        current_obs_info = np.array([
                -3, 0, 0, 0,
                4, 2, 0, 0,
                4, -2, 0, 0,
            ])

        state = np.concatenate([current_state_info, current_obs_info])
        return state
    
    def get_collision_info(self):
        data = rospy.wait_for_message('bumper', ContactsState)
        if len(data.states):
            collide = 1
        else:
            collide = 0
        return collide

    def compute_param(self):
        current_state_info = self.get_robot_info()

        vec_current_point = np.array([current_state_info[0], current_state_info[1]])
        vec_des_point = np.array([self.goal_x, self.goal_y])
        current_dis_from_des_point = np.linalg.norm(vec_des_point - vec_current_point)

        over_v = abs(current_state_info[3]) - self.limit_v
        over_w = abs(current_state_info[4]) - self.limit_w
        overspeed = math.hypot(over_v, over_w)

        return overspeed, current_dis_from_des_point
    
    def compute_state(self):
        current_state_info = self.get_robot_info()

        if self.disturb == 1:
            self.disturb_x = random.uniform(-3,3)
            self.disturb_y = random.uniform(-3,3)
            self.disturb_yaw = random.uniform(-PI/6,PI/6)
            current_state_info[0] += self.disturb_x
            current_state_info[1] += self.disturb_y
            current_state_info[2] += self.disturb_yaw

        state = current_state_info
        return state
    
    def compute_reward(self, collide, overspeed, current_dis_from_des_point, dis_temp, diff_a):
        reward = -0.1

        r_dis = dis_temp - current_dis_from_des_point
        dis_list = [0, 1]
        dis_list.append(abs(r_dis))

        r_dis_norm = ((r_dis - min(dis_list)) / (max(dis_list) - min(dis_list)))

        reward += r_dis_norm

        if collide == 1:
            reward += -10

        if current_dis_from_des_point < self.reach_goal_circle:
            reward += 20

        if current_dis_from_des_point > self.limit_circle:
            reward += -10
            
        return reward

    def set_init_pose(self):
        self.reset_env()
        init_state = self.compute_state()
        return init_state

    def reset_env(self):
        subprocess.Popen(['rosservice','call','/gazebo/reset_world'])