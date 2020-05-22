import rospy
from visualization_msgs.msg import Marker
from std_msgs.msg import Int16MultiArray
from scout.srv import AddTwoInts, AddTwoIntsResponse

from gazebo_msgs.msg import *
from gazebo_msgs.srv import *

import threading

x = 0
y = 0

def thread():
    rospy.spin()

def handle(req):

    global x
    global y

    x = req.a
    y = req.b

def pub():

    # Publish goal information to gazebo
    gazebo_goal_msg = SetModelStateRequest()
    gazebo_goal_msg.model_state.model_name = 'Goal_0'
    gazebo_goal_msg.model_state.pose.position.x = x
    gazebo_goal_msg.model_state.pose.position.y = y
    gazebo_goal_msg.model_state.pose.position.z = 1
    gazebo_goal_msg.model_state.pose.orientation.x = 0
    gazebo_goal_msg.model_state.pose.orientation.y = 0
    gazebo_goal_msg.model_state.pose.orientation.z = 0
    gazebo_goal_msg.model_state.pose.orientation.w = 0
    gazebo_goal_msg.model_state.reference_frame = 'world'

    gazebo_goal_msg1 = SetLinkStateRequest()
    gazebo_goal_msg1.link_state.link_name = 'Goal_0::link'
    gazebo_goal_msg1.link_state.pose.position.x = x
    gazebo_goal_msg1.link_state.pose.position.y = y
    gazebo_goal_msg1.link_state.pose.position.z = 1
    gazebo_goal_msg1.link_state.pose.orientation.x = 0
    gazebo_goal_msg1.link_state.pose.orientation.y = 0
    gazebo_goal_msg1.link_state.pose.orientation.z = 0
    gazebo_goal_msg1.link_state.pose.orientation.w = 0
    gazebo_goal_msg1.link_state.reference_frame = 'world'
    
    rospy.wait_for_service('/gazebo/set_model_state')
    try:
        print('Send')
        gazebo_goal_proxy = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        gazebo_goal_proxy(gazebo_goal_msg)

        gazebo_goal_proxy1 = rospy.ServiceProxy('/gazebo/set_link_state', SetLinkState)
        gazebo_goal_proxy1(gazebo_goal_msg1)
    except rospy.ServiceException:
        print('fuck')

    return AddTwoIntsResponse(req.a+req.b)

def goal_sent_server():

    rospy.init_node('goal_sent')
    s = rospy.Service('add_two_ints', AddTwoInts, handle)

    gazebo_thread = threading.Thread(target=thread())
    gazebo_thread.start()



if __name__ == '__main__':
    goal_sent_server()

        # goal_marker = rospy.Publisher('goal_Marker', Marker, queue_size = 10)

        # pub_goal_msg = Marker()
        # pub_goal_msg.ns = "goal_Marker"
        # pub_goal_msg.header.frame_id = "/odom"
        # pub_goal_msg.header.stamp = rospy.Time.now()
        # pub_goal_msg.id = 0
        # pub_goal_msg.pose.position.x = goal[0]
        # pub_goal_msg.pose.position.y = goal[1]
        # pub_goal_msg.lifetime = rospy.Duration(0)
        # pub_goal_msg.pose.position.z = 1
        # pub_goal_msg.pose.orientation.x = 0.0
        # pub_goal_msg.pose.orientation.y = 0.0
        # pub_goal_msg.pose.orientation.z = 0.0
        # pub_goal_msg.pose.orientation.w = 1.0
        # pub_goal_msg.scale.x = 0.5
        # pub_goal_msg.scale.y = 0.5
        # pub_goal_msg.scale.z = 0.03
        # pub_goal_msg.color.a = 0.3
        # pub_goal_msg.color.r = 1.0
        # pub_goal_msg.color.g = 0.0
        # pub_goal_msg.color.b = 0.0

        # goal_marker.publish(pub_goal_msg)