#include "ros/ros.h"
#include "nav_msgs/Odometry.h" 
#include "tf/transform_datatypes.h"
// #include "vlp_fir/send_msgs.h"
#include "vlp_fir/obs_info.h"
#include "scout/RL_input_msgs.h"
#include "visualization_msgs/Marker.h"
#include <sstream>
#include <iostream>

using namespace std;

scout::RL_input_msgs pub_msg;
visualization_msgs::Marker marker;

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
void callback2(const visualization_msgs::Marker::ConstPtr& msg2)
{
    marker.header.frame_id = "/odom";
    marker.header.stamp = ros::Time();
    marker.ns = 'RL_marker';
    marker.id = 1;
    marker.type = visualization_msgs::Marker::CUBE;
    marker.action = visualization_msgs::Marker::ADD;

    marker.pose.position.x = msg2->pose.position.x;
    marker.pose.position.y = msg2->pose.position.y;
    marker.pose.position.z = 0;
    marker.pose.orientation.x = 0.0;
    marker.pose.orientation.y = 0.0;
    marker.pose.orientation.z = 0.0;
    marker.pose.orientation.w = 1.0;
    marker.scale.x = 0.5;
    marker.scale.y = 0.5;
    marker.scale.z = 0.05;

    marker.color.a = 1; // Don't forget to set the alpha!
    marker.color.r = 1.0;
    marker.color.g = 0.0;
    marker.color.b = 0.0;
    marker.lifetime = ros::Duration(0);
}


int main(int argc, char **argv)
{
    ros::init(argc, argv, "RL_input");
    ros::NodeHandle n;
    ros::Subscriber sub = n.subscribe("odom", 1000, callback);
    ros::Subscriber sub2 = n.subscribe("goal_Marker", 1000, callback2);
    ros::Publisher pub = n.advertise<scout::RL_input_msgs>("RLin",1000);
    ros::Publisher pubm = n.advertise<visualization_msgs::Marker>("Goal",1000);
    while(ros::ok())
    {
        ros::AsyncSpinner spinner(2);
        spinner.start();
        pub.publish(pub_msg);
        pubm.publish(marker);
        spinner.stop();
    }
    return 0;
}