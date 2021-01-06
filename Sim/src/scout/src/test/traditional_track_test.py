import rospy
import random
from geometry_msgs.msg import Twist
from scout.msg import RL_input_msgs
from gazebo_msgs.msg import ContactsState

import numpy as np
import matplotlib.pyplot as plt
import time
import math

import subprocess

thresh = 0.8
goal_x = 6
goal_y = 0
reach_goal_circle = 0.8
limit_circle = 12
PI = 3.1415926

def cal_yaw(me, track_point):
    if track_point[1] > me[1] and track_point[0] > me[0]:
        yaw = math.atan((track_point[1] - me[1]) / (track_point[0] - me[0]))
    elif track_point[1] > me[1] and track_point[0] < me[0]:
        yaw = PI - abs(math.atan((track_point[1] - me[1]) / (track_point[0] - me[0])))
    elif track_point[1] < me[1] and track_point[0] > me[0]:
        yaw = math.atan((track_point[1] - me[1]) / (track_point[0] - me[0]))
    else:
        yaw = math.atan((track_point[1] - me[1]) / (track_point[0] - me[0])) - PI

    error = yaw - me[2]

    if abs(error) < PI/2:
        w = error
        v = 0.6
    else:
        w = PI - abs(error)
        v = - 0.6

    return w, v

def set_action(w,v):

    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    pub_msg = Twist()

    pub_msg.linear.x = v
    pub_msg.angular.z = w

    pub.publish(pub_msg)

if __name__ == '__main__':
    rospy.init_node('Traditional', anonymous=True)

    path = [[1,0.2],[2,0.5],[3,1],[4,1.5],[4.5,1.5],[5,1],[6,0]]

    all_time = 0
    success_time = 0
    collision_time = 0
    over_area_time = 0

    for ep in range(2000):

        subprocess.Popen(['rosservice','call','/gazebo/reset_world'])
        time.sleep(0.3)
        all_time += 1
        track_point_index = 0
        
        for i in range(680):

            data = rospy.wait_for_message('RLin', RL_input_msgs)        
            data_co = rospy.wait_for_message('bumper', ContactsState)
            if len(data_co.states):
                collide = 1
            else:
                collide = 0

            # me_x = data.me_x + random.uniform(-3,3)
            # me_y = data.me_y + random.uniform(-3,3)
            # me_yaw = data.me_yaw + random.uniform(-PI/4, PI/4)

            me_x = data.me_x
            me_y = data.me_y
            me_yaw = data.me_yaw
            me = [me_x, me_y, me_yaw]

            # --------------------------------------------------------------- 
            # track_list = {}

            # for i in range(len(path)):
            #     error = cal_yaw(me, path[i])

            #     if abs(error) > PI/2:
            #         continue
    
            #     dis_x = abs(me_x - path[i][0])
            #     dis_y = abs(me_y - path[i][0])
            #     dis = math.hypot(dis_x, dis_y)
            #     if dis > thresh:
            #         track_list[i] = dis
    
            # if not track_list:
            #     print('No points')
            #     break
            # else:
            #     track_point_index = min(track_list, key=track_list.get)
            #     track_point = path[track_point_index]

            # --------------------------------------------------------------- 

            if track_point_index == len(path)-1:
                pass
            else:
                dis_x = abs(me_x - path[track_point_index][0])
                dis_y = abs(me_y - path[track_point_index][0])
                dis = math.hypot(dis_x, dis_y)
                if dis < thresh:
                    track_point_index += 1

                track_point = path[track_point_index]

            w,v = cal_yaw(me, track_point)

            set_action(w,v)

            dis_goal = math.hypot(abs(data.me_x - goal_x), abs(data.me_y - goal_y))
            if dis_goal < reach_goal_circle:
                success_time += 1
                print('Sucess')
                break
            
            if collide == 1:
                collision_time += 1
                print('Collision')
                break

            if dis_goal > limit_circle:
                over_area_time += 1
                print('Over-area')
                break

        print("all_time: %d \n over_arer_time %d \n collision_time %d \n success_time %d"
        %(all_time, over_area_time, collision_time, success_time))

