import rospy
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
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

    rospy.init_node('marker', anonymous=True)
    x = -6
    y = -7

    while not rospy.is_shutdown():

        makerarray = MarkerArray()

        goal_marker = rospy.Publisher('goal_Marker', Marker, queue_size = 100)
        goal_marker1 = rospy.Publisher('goal_Marker', Marker, queue_size = 100)
        goal_marker2 = rospy.Publisher('goal_Marker', Marker, queue_size = 100)

        pub_goal_msg = Marker()
        pub_goal_msg.ns = "goal_Marker"
        pub_goal_msg.header.frame_id = "/odom"
        pub_goal_msg.header.stamp = rospy.Time.now()
        pub_goal_msg.id = 0
        pub_goal_msg.type = 2
        pub_goal_msg.pose.position.x = x
        pub_goal_msg.pose.position.y = y
        pub_goal_msg.lifetime = rospy.Duration(0)
        pub_goal_msg.pose.position.z = 0
        pub_goal_msg.pose.orientation.x = 0.0
        pub_goal_msg.pose.orientation.y = 0.0
        pub_goal_msg.pose.orientation.z = 0.0
        pub_goal_msg.pose.orientation.w = 1.0
        pub_goal_msg.scale.x = 1.6
        pub_goal_msg.scale.y = 1.6
        pub_goal_msg.scale.z = 0.05
        pub_goal_msg.color.a = 0.8
        pub_goal_msg.color.r = 0.0
        pub_goal_msg.color.g = 1.0
        pub_goal_msg.color.b = 0.0

        pub_ori_msg = Marker()
        pub_ori_msg.ns = "goal_Marker1"
        pub_ori_msg.header.frame_id = "/odom"
        pub_ori_msg.header.stamp = rospy.Time.now()
        pub_ori_msg.id = 0
        pub_ori_msg.type = 2
        pub_ori_msg.pose.position.x = 0
        pub_ori_msg.pose.position.y = 0
        pub_ori_msg.lifetime = rospy.Duration(0)
        pub_ori_msg.pose.position.z = 0
        pub_ori_msg.pose.orientation.x = 0.0
        pub_ori_msg.pose.orientation.y = 0.0
        pub_ori_msg.pose.orientation.z = 0.0
        pub_ori_msg.pose.orientation.w = 1.0
        pub_ori_msg.scale.x = 1.6
        pub_ori_msg.scale.y = 1.6
        pub_ori_msg.scale.z = 0.05
        pub_ori_msg.color.a = 0.8
        pub_ori_msg.color.r = 0.0
        pub_ori_msg.color.g = 0.0
        pub_ori_msg.color.b = 0.8

        pub_range_msg = Marker()
        pub_range_msg.ns = "goal_Marker2"
        pub_range_msg.header.frame_id = "/odom"
        pub_range_msg.header.stamp = rospy.Time.now()
        pub_range_msg.id = 0
        pub_range_msg.type = 2
        pub_range_msg.pose.position.x = 0
        pub_range_msg.pose.position.y = 0
        pub_range_msg.lifetime = rospy.Duration(0)
        pub_range_msg.pose.position.z = 0
        pub_range_msg.pose.orientation.x = 0.0
        pub_range_msg.pose.orientation.y = 0.0
        pub_range_msg.pose.orientation.z = 0.0
        pub_range_msg.pose.orientation.w = 1.0
        pub_range_msg.scale.x = 24
        pub_range_msg.scale.y = 24
        pub_range_msg.scale.z = 0.05
        pub_range_msg.color.a = 0.3
        pub_range_msg.color.r = 0.3
        pub_range_msg.color.g = 0.0
        pub_range_msg.color.b = 0.0
        
        goal_marker.publish(pub_goal_msg)
        goal_marker1.publish(pub_ori_msg)
        goal_marker2.publish(pub_range_msg)
