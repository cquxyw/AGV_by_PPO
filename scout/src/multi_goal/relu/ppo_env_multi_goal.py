import rospy
from scout.msg import RL_input_msgs
from geometry_msgs.msg import Twist
from vlp_fir.msg import obs_info
from gazebo_msgs.msg import ContactsState
from visualization_msgs.msg import Marker
from std_msgs.msg import Int16MultiArray

import tensorflow as tf
import numpy as np
import random
import math
import os

import subprocess

real_env = 0

class env(object):

    def __init__(self):
        self.limit_v = 1.5
        self.limit_w = 0.785

        self.reach_goal_circle = 0.5
    
    def rand_goal(self):
        self.goal_x = random.randint(6, 12)
        self.goal_y = random.randint(6, 12)
        msg = [self.goal_x, self.goal_y]
        goal_rand = rospy.Publisher('goal_Rand', Int16MultiArray, queue_size = 10)
        goal_rand_msg = Int16MultiArray()
        goal_rand_msg.data = msg
        goal_rand.publish(goal_rand_msg)

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
        current_state_info = np.array([data.me_x, data.me_y, data.me_yaw, data.me_v, data.me_w])
        return current_state_info
    
    def get_obs_info(self):
        data = rospy.wait_for_message('obj_', obs_info)

        ## simple application
        # current_obs_info = np.empty([1,4])
        # for i in range(data.num):
        #     iobs = [data.x[i], data.y[i], data.len[i], data.width[i]]
        #     current_obs_info = np.vstack([current_obs_info, iobs])
        # current_obs_info = np.delete(current_obs_info, 0, 0)
        # return current_obs_info

        ## real environment
        if real_env == 1:
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
        else:
            current_obs_info = np.array([2,3,1,1,3,4,1,1,5,6,1,1,7,8,1,1,9,10,1,1])

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

        return current_dis_from_des_point
    
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

    def compute_reward(self, collide, current_dis_from_des_point):

        reward = 0

        if collide == 1:
            reward += -1

        if current_dis_from_des_point < self.reach_goal_circle:
            reward += 1
            
        return reward

    def set_init_pose(self):
        self.reset_env()
        init_state = self.compute_state()
        return init_state

    def reset_env(self):
        subprocess.Popen(['rosservice','call','/gazebo/reset_world'])