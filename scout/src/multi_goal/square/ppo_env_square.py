import rospy
from scout.msg import RL_input_msgs
from geometry_msgs.msg import Twist
from vlp_fir.msg import obs_info
from gazebo_msgs.msg import ContactsState
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from visualization_msgs.msg import Marker
from std_msgs.msg import Int16MultiArray
from beginner_tutorials.srv import *

import tensorflow as tf
import numpy as np
import random
import math
import os

import subprocess

real_env = 1
goal = [(3,0),(2,-6),(3,-8),(6,0),(-1,5),(-6,1),(-6,3),(-6,-7),(-4,-6)]

class env(object):

    def __init__(self):
        self.limit_v = 1.5
        self.limit_w = 0.785

        self.reach_goal_circle = 0.5

        self.square_range = 30
    
    def rand_goal(self):
        goal_index = random.randint(0, 8)
        self.goal_x = goal[goal_index][0]
        self.goal_y = goal[goal_index][1]

        # Publish goal information to gazebo
        gazebo_goal_msg = ModelState()
        gazebo_goal_msg.model_name = 'Goal'
        gazebo_goal_msg.pose.position.x = self.goal_x
        gazebo_goal_msg.pose.position.y = self.goal_y
        gazebo_goal_msg.pose.position.z = 0.05
        gazebo_goal_msg.pose.orientation.x = 0
        gazebo_goal_msg.pose.orientation.y = 0
        gazebo_goal_msg.pose.orientation.z = 0
        gazebo_goal_msg.pose.orientation.w = 0

        rospy.wait_for_service('/gazebo/set_model_state')

        gazebo_goal_proxy = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        resp1 = gazebo_goal_proxy(gazebo_goal_msg)

        # Publish goal information to rviz
        rospy.wait_for_service('add_two_ints')

        rvi_goal_proxy = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        resp2 = add_two_ints(self.goal_x, self.goal_y)


    def set_action(self, action):
        # set publisher
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        pub_msg = Twist()
        # print(action)
        
        # clip action
        action[0] = np.clip(action[0], -self.limit_v, self.limit_v)

        action[1] = action[1] * (0.785/1.5)
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
        current_state_info = np.array([data.me_x, data.me_y, data.me_yaw, data.me_v, data.me_w])
        return current_state_info
    
    def get_obs_info(self):

        ## simple application
        # current_obs_info = np.zeros([1,4])
        # if data.num < 3:
        #     if data.num == 0:
        #         current_obs_info = np.zeros([3,4])
        #     else:
        #         for i in range(data.num):
        #             iobs = [data.x[i], data.y[i], data.len[i], data.width[i]]
        #             current_obs_info = np.vstack([current_obs_info, iobs])
        #         current_obs_info = np.delete(current_obs_info, 0, 0)
        #         zero_obs = np.zeros([3-data.num, 4])
        #         current_obs_info = np.vstack([current_obs_info, zero_obs])
        # else:
        #     for i in range(data.num):
        #         iobs = [data.x[i], data.y[i], data.len[i], data.width[i]]
        #         current_obs_info = np.vstack([current_obs_info, iobs])
        #     current_obs_info = np.delete(current_obs_info, 0, 0)
        # current_obs_info = np.reshape(-1)

        ## real environment
        if real_env == 1:
            data = rospy.wait_for_message('obj_', obs_info)
            if data.num >= 5:
                current_obs_info = np.array([
                    [data.x[0], data.y[0], data.len[0], data.width[0]],
                    [data.x[1], data.y[1], data.len[1], data.width[1]],
                    [data.x[2], data.y[2], data.len[2], data.width[2]],
                    [data.x[3], data.y[3], data.len[3], data.width[3]],
                    [data.x[4], data.y[4], data.len[4], data.width[4]]
                ])
            elif data.num == 4:
                current_obs_info = np.array([
                    [data.x[0], data.y[0], data.len[0], data.width[0]],
                    [data.x[1], data.y[1], data.len[1], data.width[1]],
                    [data.x[2], data.y[2], data.len[2], data.width[2]],
                    [data.x[3], data.y[3], data.len[3], data.width[3]],
                    [0, 0, 0, 0]
                ])
            elif data.num == 3:
                current_obs_info = np.array([
                    [data.x[0], data.y[0], data.len[0], data.width[0]],
                    [data.x[1], data.y[1], data.len[1], data.width[1]],
                    [data.x[2], data.y[2], data.len[2], data.width[2]],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ])
            elif data.num == 2:
                current_obs_info = np.array([
                    [data.x[0], data.y[0], data.len[0], data.width[0]],
                    [data.x[1], data.y[1], data.len[1], data.width[1]],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ])
            elif data.num == 1:
                current_obs_info = np.array([
                    [data.x[0], data.y[0], data.len[0], data.width[0]],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ])
            elif data.num == 0:
                current_obs_info = np.zeros([5,4])
                current_obs_info = np.reshape(-1)
        else:
            current_obs_info = np.array([5,3,0.5,0.5,-2,4,0.5,0.5,-4,5,0.5,0.5,3,-3,0.5,0.5,-7,-1,0.5,0.5,-2,3,0.5,0.5])

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

        current_dis_from_center = np.linalg.norm(vec_current_point)

        return current_dis_from_des_point, current_dis_from_center
    
    def choose_obs(self, car_info, obs_info):
        dis_obs_list = dict()

        # calculate distance between obstacle and car
        for i in range (np.shape(obs_info)[0]):
            obs_x = obs_info[i][0]
            obs_y = obs_info[i][1]
            dis_x = car_info[0] - obs_x
            dis_y = car_info[1] - obs_y
            dis_obs = math.hypot(dis_x, dis_y)
            dis_obs_list[i] = dis_obs

        # sort distance obstacle index
        dis_obs_order = sorted(dis_obs_list.items(), key=lambda x:x[1])
        dis_obs_order_list = list(dis_obs_order)
        dis_index = [dis_obs_order_list[0][0], dis_obs_order_list[1][0], dis_obs_order_list[2][0], dis_obs_order_list[3][0], dis_obs_order_list[4][0]]
        
        return dis_index
    
    def compute_state(self):
        # get car state and obstacles state
        current_state_info = self.get_robot_info()
        current_obs_info = self.get_obs_info()

        # car state
        car_state = current_state_info
        # goal state
        goal_state = np.array([self.goal_x, self.goal_y])

        ## real_env: obstacle state(choose the latest obstacle)
        if real_env == 1:
            obs_index = self.choose_obs(current_state_info, current_obs_info)
            obs0_state = current_obs_info[obs_index[0]]
            obs1_state = current_obs_info[obs_index[1]]
            obs2_state = current_obs_info[obs_index[2]]
            obs3_state = current_obs_info[obs_index[3]]
            obs4_state = current_obs_info[obs_index[4]]
            state = np.concatenate([goal_state, car_state, obs0_state, obs1_state, obs2_state, obs3_state, obs4_state])
        else:
            state = np.concatenate([goal_state, car_state, current_obs_info])

        return state

    def compute_reward(self, collide, current_dis_from_center, current_dis_from_des_point, last_dis_from_des_point):

        # reward = 0
        reward = (last_dis_from_des_point - current_dis_from_des_point) / 100

        if collide == 1:
            reward += -1

        if current_dis_from_des_point < self.reach_goal_circle:
            reward += 1
        
        if current_dis_from_center < self.square_range:
            reward += -1
            
        return reward

    def set_init_pose(self):
        self.reset_env()
        init_state = self.compute_state()
        return init_state

    def reset_env(self):
        subprocess.Popen(['rosservice','call','/gazebo/reset_world'])