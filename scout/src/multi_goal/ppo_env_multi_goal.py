import rospy
from scout.msg import RL_input_msgs
from geometry_msgs.msg import Twist
from vlp_fir.msg import obs_info
from gazebo_msgs.msg import ContactsState
from visualization_msgs.msg import Marker

import tensorflow as tf
import numpy as np
import random
import math
import os

import subprocess

class env(object):

    def __init__(self):
        self.limit_v = 1.5
        self.limit_w = 0.785

        self.limit_circle = 20
        self.reach_goal_circle = 0.5
        self.limit_overspeed = 6
        # self.used0_obs_info = np.zeros([5, 4])
        # self.used1_obs_info = np.zeros([5, 4])
    
    def rand_goal(self):
        self.goal_x = random.randint(6, 12)
        self.goal_y = random.randint(6, 12)
        pub_goal = rospy.Publisher('goal_Marker', Marker, queue_size = 10)
        pub_goal_msg = Marker()

        pub_goal_msg.ns = "goal_Marker"
        pub_goal_msg.header.frame_id = "/odom"
        pub_goal_msg.header.stamp = rospy.Time.now()
        pub_goal_msg.id = 0
        pub_goal_msg.pose.position.x = self.goal_x
        pub_goal_msg.pose.position.y = self.goal_y
        pub_goal_msg.lifetime = rospy.Duration(0)
        pub_goal_msg.pose.position.z = 1
        pub_goal_msg.pose.orientation.x = 0.0
        pub_goal_msg.pose.orientation.y = 0.0
        pub_goal_msg.pose.orientation.z = 0.0
        pub_goal_msg.pose.orientation.w = 1.0
        pub_goal_msg.scale.x = 0.5
        pub_goal_msg.scale.y = 0.5
        pub_goal_msg.scale.z = 0.1
        pub_goal_msg.color.a = 0.2
        pub_goal_msg.color.r = 1.0
        pub_goal_msg.color.g = 0.0
        pub_goal_msg.color.b = 0.0

        pub_goal.publish(pub_goal_msg)

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
        speed = math.hypot(data.me_v, data.me_w)
        current_state_info = np.array([data.me_x, data.me_y, data.me_yaw, speed])
        return current_state_info
    
    def get_obs_info(self):
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

        # mean_obs_info = (self.used0_obs_info + self.used1_obs_info + current_obs_info) / 3
        # self.used0_obs_info = self.used1_obs_info
        # self.used1_obs_info = current_obs_info
        
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

        overspeed = abs(current_state_info[3] - math.hypot(self.limit_v, self.limit_w))

        return overspeed, current_dis_from_des_point
    
    def choose_obs(self, car_info, obs_info):
        dis_obs_list = []
        for i in range (np.shape(obs_info)[0]):
            obs_x = obs_info[i][0]
            obs_y = obs_info[i][1]
            dis_x = car_info[0] - obs_x
            dis_y = car_info[1] - obs_y
            dis_obs = math.hypot(dis_x, dis_y)
            dis_obs_list.append(dis_obs)
        dis_index = dis_obs_list.index(min(dis_obs_list))
        return dis_index
    
    def compute_state(self):
        # get car state and obstacles state
        current_state_info = self.get_robot_info()
        current_obs_info = self.get_obs_info()

        # car state
        car_state = current_state_info

        # obstacle state(choose the latest obstacle)
        min_obs_index = self.choose_obs(current_state_info, current_obs_info)
        obs_state = current_obs_info[min_obs_index]

        # goal state
        goal_state = np.array([self.goal_x, self.goal_y, 0, 0])

        # compute state
        state = np.concatenate([[car_state], [obs_state], [goal_state]])

        return state
    
    def compute_u(self, state):
        # param
        n_goal = 1
        n_obs = 1
        safe_dis = 0.5
        car_circle = 1.1/2

        # get state
        car_info = state[0]
        obs_state = state[1]
        goal_state = state[2]

        obs_len = obs_state[2]
        obs_wid = obs_state[3]

        # calculate safe range
        q = max(obs_len, obs_wid) + car_circle + safe_dis

        # calculate distance between car and obstacle
        dis_obs_x = car_info[0] - obs_state[0]
        dis_obs_y = car_info[1] - obs_state[1]
        dis_obs = math.hypot(dis_obs_x, dis_obs_y)

        # calculate distance between car and goal
        dis_goal_x = car_info[0] - goal_state[0]
        dis_goal_y = car_info[1] - goal_state[1]
        dis_goal = math.hypot(dis_goal_x, dis_goal_y)

        # calculate repulsion potential energe
        if dis_obs > q:
            ur = 0
        else:
            dis_obs = np.clip(dis_obs, 1e-3, 1e+3)
            ur = n_obs * pow(1/dis_obs - 1/q, 2)
        
        # calculate attraction potential energe
        ua = n_goal * (dis_goal - (car_circle * 3))

        u_current = ur + ua
        return u_current

    def compute_reward(self, state, collide, overspeed, current_dis_from_des_point):
        # computer yaw reward
        distance_from_des_x = state[2][0] - state[0][0]
        distance_from_des_y = state[2][1] - state[0][1]
        des_yaw = math.atan2(distance_from_des_y, distance_from_des_x)
        current_yaw = state[0][2]
        diff_yaw = des_yaw - current_yaw
        reward_diff_yaw = 1 - abs(diff_yaw)

        # get other rewards
        reward_u = - self.compute_u(state)
        reward_overspeed = - overspeed

        # calculate reward_norm
        reward_norm = []
        reward_all = np.array([reward_u, reward_overspeed, reward_diff_yaw])
        reward_mean = np.mean(reward_all)
        reward_var = np.var(reward_all)
        reward_var_s = np.sqrt(reward_var)
        for i in range(np.shape(reward_all)[0]):
            reward_norm.append((reward_all[i] - reward_mean)/reward_var_s)

        # compute reward in process
        reward = (reward_norm[0] * 0.6 + reward_norm[1] * 0.15 + reward_norm[2] * 0.1) * 0.05

        # add reward in end
        if collide == 1:
            reward += -10

        if current_dis_from_des_point < self.reach_goal_circle:
            reward += 15
        
        if current_dis_from_des_point > self.limit_circle:
            reward += -5
            
        return reward

    def set_init_pose(self):
        self.reset_env()
        init_state = self.compute_state()
        return init_state

    def reset_env(self):
        subprocess.Popen(['rosservice','call','/gazebo/reset_world'])