import rospy
import random

import tensorflow.compat.v1 as tf
import numpy as np
import time
import math
import os

# from gpstoenu.msg import enu
# from can_listener.msg import vel_can
from PPO.msg import RL_input_msgs
from geometry_msgs.msg import Twist

import ppo_algo
import ppo_env
    
if __name__ == '__main__':

    rospy.init_node('RL')

    ppo = ppo_algo.ppo()
    env = ppo_env.env()

    print('Tensorflow启动成功')

    ppo.restore(0)

    a_init = [0, 0]
 
    s = np.array([0,0,8,0,0,
        -3, 0, 0, 0,
        4, 2, 0, 0,
        4, -2, 0, 0,
        ])
                     
    print('3秒后导航开始，请远离')
    time.sleep(3)

    while not rospy.is_shutdown():
        
        start = time.clock()

        a =  ppo.choose_action(s)
        env.set_action(a)

        s_= env.compute_state()
        s = s_
        print("当前位置：北向-%.1f;东向-%.1f" %(s[0],s[1]))
        print("采取动作：线速度-%.1f;角速度-%.1f" %(a[0],a[1]))

        end = time.clock()
        print("耗时：%.3f" %(end-start))

        dis_x = abs(s[0]-6)
        dis_y = abs(s[1])
        dis = math.hypot(dis_x,dis_y)
        if dis < 0.8:
            break
    
    print('已到达目的地，导航成功')