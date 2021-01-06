import rospy
from gazebo_msgs.msg import ModelState
import threading

def do(event):

    while(not rospy.is_shutdown()):
        pub_msg.model_name = 'real_obs'
        pub_msg.pose.position.x = 8
        pub_msg.pose.position.y = 0
        pub_msg.pose.position.z = 0
        pub.publish(pub_msg)

rospy.init_node('test222')
pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=1)
pub_msg = ModelState()

event = threading.Event()
t = threading.Thread(target=do, args=(event,))
t.start()
t.join()

for i in range(1000000000000000):
    print(1)

event.clear()