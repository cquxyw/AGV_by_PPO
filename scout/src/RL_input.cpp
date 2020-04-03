#include "ros/ros.h"
#include "nav_msgs/Odometry.h" 
#include "tf/transform_datatypes.h"
// #include "vlp_fir/send_msgs.h"
#include "vlp_fir/obs_info.h"
#include "scout/RL_input_msgs.h"
#include <sstream>
#include <iostream>

using namespace std;

scout::RL_input_msgs pub_msg;

void callback(const nav_msgs::Odometry::ConstPtr& msg)
{
    tf::Quaternion quat;
    tf::quaternionMsgToTF(msg->pose.pose.orientation, quat);
    double roll, pitch, yaw;
    tf::Matrix3x3(quat).getRPY(roll, pitch, yaw);
    
    pub_msg.me_x = msg->pose.pose.position.x;
    pub_msg.me_y = msg->pose.pose.position.y;
    pub_msg.me_yaw = yaw;
    pub_msg.me_v = msg->twist.twist.linear.x;
    pub_msg.me_w = msg->twist.twist.angular.z;
}
void callback2(const vlp_fir::obs_info::ConstPtr& msg2)
{
    pub_msg.obs_num = msg2->num;
    pub_msg.obs_x = msg2->x;
    pub_msg.obs_y = msg2->y;
    pub_msg.obs_len = msg2->len;
    pub_msg.obs_width = msg2->width;
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "RL_input");
    ros::NodeHandle n;
    ros::Subscriber sub = n.subscribe("odom", 1000, callback);
    ros::Subscriber sub2 = n.subscribe("obj_", 1000, callback2);
    ros::Publisher pub = n.advertise<scout::RL_input_msgs>("RLin",1000);
    while(ros::ok())
    {
        ros::AsyncSpinner spinner(2);
        spinner.start();
        pub.publish(pub_msg);
        spinner.stop();
    }
    return 0;
}