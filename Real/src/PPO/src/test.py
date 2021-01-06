import rospy
from vlp_fir.msg import obs_info

import numpy as np

def get_obs_info():
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

if __name__ == '__main__':

    rospy.init_node('test_lidar')

    while not rospy.is_shutdown():
        state = get_obs_info()
        print(state)