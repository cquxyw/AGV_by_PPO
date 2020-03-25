import rospy
from scout.msg import RL_input_msgs
from geometry_msgs.msg import Twist

import tensorflow as tf
import numpy as np
import math
import os

import subprocess

class env(object):

    def __init__(self):
        self.limit_v = 2
        self.limit_w = 3.14

        self.goal_x = 8
        self.goal_y = 8
    
    def set_action(self, action):
        # set publisher
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        pub_msg = Twist()
        print(action)
        
        # clip action
        action[0] = np.clip(action[0], -2, 2)
        action[1] = np.clip(action[1], -3.14, 3.14)

        # publish action
        if not np.isnan(action[0]) or np.isnan(action[1]):
            pub_msg.linear.x = action[0]
            pub_msg.angular.z = action[1]
            pub.publish(pub_msg)
        else:
            print('Warning: Action is NAN')
            os._exit(0)

    def get_robot_info(self):
        data = rospy.wait_for_message('RLin',RL_input_msgs)
        current_state_info = np.array([data.me_x, data.me_y, data.me_yaw, data.me_v, data.me_w])
        return current_state_info
    
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
        # compute state
        state = current_state_info
        return state
    
    def compute_reward(self):
        current_state_info = self.get_robot_info()
        overspeed, current_dis_from_des_point = self.compute_param()

        reward_over_speed = - overspeed
        reward_dis = - current_dis_from_des_point

        distance_from_des_x = self.goal_x - current_state_info[0]
        distance_from_des_y = self.goal_y - current_state_info[1]
        des_yaw = math.atan2(distance_from_des_y, distance_from_des_x)
        current_yaw = current_state_info[2]
        diff_yaw = des_yaw - current_yaw
        reward_diff_yaw = math.sqrt(pow(diff_yaw, 2))

        # compute reward
        reward = reward_over_speed * 0.3 + reward_diff_yaw * 0.3 + reward_dis

        if current_dis_from_des_point < 0.1:
            reward += 200
        elif 0.1 < current_dis_from_des_point < 1:
            reward += 20
        
        if overspeed > 20:
            reward += -80
            
        return reward

    def set_init_pose(self):
        self.reset_env()
        init_state = self.compute_state()
        return init_state

    def reset_env(self):
        subprocess.Popen(['rosservice','call','/gazebo/reset_world'])