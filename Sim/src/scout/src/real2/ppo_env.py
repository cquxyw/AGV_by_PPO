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
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelConfiguration
from gazebo_msgs.srv import SetModelConfigurationRequest
import threading
import random

class env(object):

    def __init__(self):
        self.limit_v = 1.5
        self.limit_w = 0.785

        self.goal_x = 6
        self.goal_y = 0

        self.limit_circle = 6
        self.reach_goal_circle = 0.8

        self.obs1x = 0
        self.obs1y = 0

        self.obs2x = 0
        self.obs2y = 0

        self.obs2x = 0
        self.obs2y = 0


    def set_obs(self):
        self.obs1x = random.uniform(-3,3)
        self.obs1y = random.uniform(-3,3)

        self.obs2x = random.uniform(-3,3)
        self.obs2y = random.uniform(-3,3)

        self.obs3x = random.uniform(-3,3)
        self.obs3y = random.uniform(-3,3)

        goal_set = random.randint(0,1)
        if(goal_set == 0):
            self.goal_x = random.uniform(-3,-5)
        else:
            self.goal_x = random.uniform(3,5)
            
        self.goal_y = random.uniform(-4,4)

        subprocess.Popen(['rosservice','call','/gazebo/set_model_state', '{model_state: { model_name: obs1, pose: { position: { x: %.2f, y: %.2f ,z: 0 }, orientation: {x: 0, y: 0, z: 0, w: 0 } }, twist: { linear: {x: 0.0 , y: 0 ,z: 0 } , angular: { x: 0.0 , y: 0 , z: 0.0 } } , reference_frame: world } }' %(self.obs1x, self.obs1y)])

        subprocess.Popen(['rosservice','call','/gazebo/set_model_state', '{model_state: { model_name: obs2, pose: { position: { x: %.2f, y: %.2f ,z: 0 }, orientation: {x: 0, y: 0, z: 0, w: 0 } }, twist: { linear: {x: 0.0 , y: 0 ,z: 0 } , angular: { x: 0.0 , y: 0 , z: 0.0 } } , reference_frame: world } }' %(self.obs2x, self.obs2y)])

        subprocess.Popen(['rosservice','call','/gazebo/set_model_state', '{model_state: { model_name: obs3, pose: { position: { x: %.2f, y: %.2f ,z: 0 }, orientation: {x: 0, y: 0, z: 0, w: 0 } }, twist: { linear: {x: 0.0 , y: 0 ,z: 0 } , angular: { x: 0.0 , y: 0 , z: 0.0 } } , reference_frame: world } }' %(self.obs3x, self.obs3y)])

        subprocess.Popen(['rosservice','call','/gazebo/set_model_state', '{model_state: { model_name: goal, pose: { position: { x: %.2f, y: %.2f ,z: 0 }, orientation: {x: 0, y: 0, z: 0, w: 0 } }, twist: { linear: {x: 0.0 , y: 0 ,z: 0 } , angular: { x: 0.0 , y: 0 , z: 0.0 } } , reference_frame: world } }' %(self.goal_x, self.goal_y)])

    def set_action(self, action):
        # set publisher
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        pub_msg = Twist()
        # print(action)
        
        # clip action
        action[0] = np.clip(self.limit_v*action[0], 0, self.limit_v)
        action[1] = np.clip(self.limit_w*action[1], -self.limit_w, self.limit_w)

        # publish action
        if not np.isnan(action[0]) or np.isnan(action[1]):
            pub_msg.linear.x = action[0]
            pub_msg.angular.z = action[1]
            pub.publish(pub_msg)
        else:
            print('Warning: Action is NAN')

    def get_robot_info(self):
        data = rospy.wait_for_message('RLin', RL_input_msgs)
        current_state_info = np.array([data.me_x, data.me_y, data.me_yaw, data.me_v, data.me_w, self.goal_x, self.goal_y])
        return current_state_info
    
    def get_obs_info(self):
        data = rospy.wait_for_message('obj_', obs_info)
        if data.num >= 3:
            current_obs_info = np.array([
                data.x[0], data.y[0], data.len[0], data.width[0],
                data.x[1], data.y[1], data.len[1], data.width[1],
                data.x[2], data.y[2], data.len[2], data.width[2],
            ])
        elif data.num == 2:
            current_obs_info = np.array([
                data.x[0], data.y[0], data.len[0], data.width[0],
                data.x[1], data.y[1], data.len[1], data.width[1],
                0, 0, 0, 0,
            ])
        elif data.num == 1:
            current_obs_info = np.array([
                data.x[0], data.y[0], data.len[0], data.width[0],
                0, 0, 0, 0,
                0, 0, 0, 0,
            ])
        elif data.num == 0:
            current_obs_info = np.array([
                0, 0, 0, 0,
                0, 0, 0, 0,
                0, 0, 0, 0,
            ])
        
        return current_obs_info
    
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

        dis_ori = math.hypot(current_state_info[0], current_state_info[1])

        return dis_ori, current_dis_from_des_point
    
    def compute_state(self):
        current_state_info = self.get_robot_info()
        current_obs_info = self.get_obs_info()

        # compute state
        state = np.concatenate([current_state_info, current_obs_info])
        return state
    
    def compute_reward(self, collide, current_dis_from_des_point, dis_ori, dis_temp):

        r_dis = dis_temp - current_dis_from_des_point
        dis_list = [0, 1]
        dis_list.append(abs(r_dis))

        r_dis_norm = ((r_dis - min(dis_list)) / (max(dis_list) - min(dis_list)))

        reward = r_dis_norm

        if collide == 1:
            reward += -10

        if current_dis_from_des_point < self.reach_goal_circle:
            reward += 20

        if dis_ori > self.limit_circle:
            reward += -10
            
        return reward

    def set_init_pose(self):
        self.reset_env()
        init_state = self.compute_state()
        return init_state

    def reset_env(self):
        subprocess.Popen(['rosservice','call','/gazebo/reset_world'])