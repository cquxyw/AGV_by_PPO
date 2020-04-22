import rospy
from visualization_msgs.msg import Marker
from std_msgs.msg import Int16MultiArray

if __name__ == '__main__':
    x = 0
    y = 0
    rospy.init_node('goal_Marker')
    while not rospy.is_shutdown():

        data = rospy.rospy.wait_for_message('goal_rand', Int16MultiArray)
        if len(data):
            x = data.data[0]
            y = data.data[1]

        goal_marker = rospy.Publisher('goal_Marker', Marker, queue_size = 10)

        pub_goal_msg = Marker()
        pub_goal_msg.ns = "goal_Marker"
        pub_goal_msg.header.frame_id = "/odom"
        pub_goal_msg.header.stamp = rospy.Time.now()
        pub_goal_msg.id = 0
        pub_goal_msg.pose.position.x = x
        pub_goal_msg.pose.position.y = y
        pub_goal_msg.lifetime = rospy.Duration(0)
        pub_goal_msg.pose.position.z = 1
        pub_goal_msg.pose.orientation.x = 0.0
        pub_goal_msg.pose.orientation.y = 0.0
        pub_goal_msg.pose.orientation.z = 0.0
        pub_goal_msg.pose.orientation.w = 1.0
        pub_goal_msg.scale.x = 0.5
        pub_goal_msg.scale.y = 0.5
        pub_goal_msg.scale.z = 0.03
        pub_goal_msg.color.a = 0.3
        pub_goal_msg.color.r = 1.0
        pub_goal_msg.color.g = 0.0
        pub_goal_msg.color.b = 0.0

        goal_marker.publish(pub_goal_msg)