from beginner_tutorials.srv import AddTwoInts
from visualization_msgs.msg import Marker
import rospy

def Marker_pub(req):
    
    goal_marker = rospy.Publisher('goal_Marker', Marker, queue_size = 10)

    pub_goal_msg = Marker()
    pub_goal_msg.ns = "goal_Marker"
    pub_goal_msg.header.frame_id = "/odom"
    pub_goal_msg.header.stamp = rospy.Time.now()
    pub_goal_msg.id = 0
    pub_goal_msg.type = 1
    pub_goal_msg.pose.position.x = req.a
    pub_goal_msg.pose.position.y = req.b
    pub_goal_msg.pose.position.z = 1
    pub_goal_msg.pose.orientation.x = 0.0
    pub_goal_msg.pose.orientation.y = 0.0
    pub_goal_msg.pose.orientation.z = 0.06
    pub_goal_msg.pose.orientation.w = 1.0
    pub_goal_msg.scale.x = 0.5
    pub_goal_msg.scale.y = 0.5
    pub_goal_msg.scale.z = 0.03
    pub_goal_msg.color.a = 0.3
    pub_goal_msg.color.r = 1.0
    pub_goal_msg.color.g = 0.0
    pub_goal_msg.color.b = 0.0
    pub_goal_msg.lifetime = rospy.Duration(0)

    goal_marker.publish(pub_goal_msg)

def goal_rviz():
    rospy.init_node('goal_rviz')
    s = rospy.Service('add_two_ints', AddTwoInts, Marker_pub)
    rospy.spin()

if __name__ == "__main__":
    goal_rviz()