import rospy
from std_srvs.srv import Empty

if __name__ == '__main__':
    
    rospy.init_node('reset_world')

    while not rospy.is_shutdown():
        rospy.wait_for_service('/gazebo/reset_world')
        reset_world = rospy.ServiceProxy('/gazebo/reset_world',Empty)
        reset_world()