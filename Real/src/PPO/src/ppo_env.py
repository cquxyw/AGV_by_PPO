import rospy
from PPO.msg import RL_input_msgs
from gpstoenu.msg import enu
from can_listener.msg import vel_can
from geometry_msgs.msg import Twist
from vlp_fir.msg import obs_info

import tensorflow.compat.v1 as tf
import numpy as np
import math
import os

import subprocess

class env(object):

    def __init__(self):
        self.limit_v = 1.5
        self.limit_w = 0.785

        self.goal_x = 6
        self.goal_y = 0

        self.limit_circle = 12
        self.reach_goal_circle = 0.8
        self.limit_overspeed = 12
            
    def set_action(self, action):

        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        pub_msg = Twist()

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
        # data_loc = rospy.wait_for_message('enu', enu)
        # data_speed = rospy.wait_for_message('vel_can', vel_can)
        # current_state_info = np.array([data_loc.x, data_loc.y, 0, data_speed.v, data.w])

        data = rospy.wait_for_message('RLin', RL_input_msgs)
        current_state_info = np.array([data.x, data.y, 8, data.v, data.w])

        return current_state_info
    
    def get_obs_info(self):
        # data = rospy.wait_for_message('obj_', obs_info)
        # if data.num >= 3:
        #     current_obs_info = np.array([
        #         data.x[0], data.y[0], data.len[0], data.width[0],
        #         data.x[1], data.y[1], data.len[1], data.width[1],
        #         data.x[2], data.y[2], data.len[2], data.width[2],
        #     ])
        # elif data.num == 2:
        #     current_obs_info = np.array([
        #         data.x[0], data.y[0], data.len[0], data.width[0],
        #         data.x[1], data.y[1], data.len[1], data.width[1],
        #         0, 0, 0, 0,
        #     ])
        # elif data.num == 1:
        #     current_obs_info = np.array([
        #         data.x[0], data.y[0], data.len[0], data.width[0],
        #         0, 0, 0, 0,
        #         0, 0, 0, 0,
        #     ])
        # elif data.num == 0:
        #     current_obs_info = np.array([
        #         0, 0, 0, 0,
        #         0, 0, 0, 0,
        #         0, 0, 0, 0,
        #     ])

        current_obs_info = np.array([
            -3, 0, 0, 0,
            4, 2, 0, 0,
            4, -2, 0, 0,
            ])
        
        return current_obs_info
    
    def compute_state(self):
        current_state_info = self.get_robot_info()
        current_obs_info = self.get_obs_info()
        state = np.concatenate([current_state_info, current_obs_info])
        return state