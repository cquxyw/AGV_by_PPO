import rospy
from scout.msg import RL_input_msgs
from geometry_msgs.msg import Twist
from vlp_fir.msg import obs_info
from gazebo_msgs.msg import ContactsState

import tensorflow as tf
import numpy as np
import math
import os

import subprocess

class env(object):

    def __init__(self):
        self.limit_v = 1.5
        self.limit_w = 0.785

        self.goal_x = 5
        self.goal_y = 0

        self.limit_circle = 6
        self.reach_goal_circle = 0.8
            
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
        current_state_info = np.array([data.me_x, data.me_y, -1])
        return current_state_info
    
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

        return current_dis_from_des_point
    
    def compute_state(self):
        state = self.get_robot_info()

        return state
    
    def compute_reward(self, collide, current_dis_from_des_point, dis_temp):
        reward = 0

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