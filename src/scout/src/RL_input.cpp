#include "ros/ros.h"
#include "nav_msgs/Odometry.h" 
#include "vlp_fir/send_msgs.h"
#include "scout/RL_input_msgs.h"
#include <sstream>
#include <iostream>

using namespace std;

scout::RL_input_msgs pub_msg;

void callback(const nav_msgs::Odometry::ConstPtr& msg)
{
    pub_msg.me_x = msg->pose.pose.position.x;
    pub_msg.me_y = msg->pose.pose.position.y;
    pub_msg.me_yaw = msg->pose.pose.orientation.z;
    pub_msg.me_v = msg->twist.twist.linear.x;
    pub_msg.me_w = msg->twist.twist.angular.z;
}
void callback2(const vlp_fir::send_msgs::ConstPtr& msg2)
{
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