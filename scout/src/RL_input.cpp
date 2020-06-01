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
visualization_msgs::Marker range;
visualization_msgs::Marker goal;
scout::goal_srv goal;

uint32_t shape = visualization_msgs::Marker::CYLINDER;

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

void mark_goal()
{
    goal.header.frame_id = "/odom";
    goal.header.stamp = ros::Time::now();

    // Set the namespace and id for this marker.  This serves to create a unique ID
    // Any marker sent with the same namespace and id will overwrite the old one
    goal.ns = "basic_shapes";
    goal.id = 0;

    // Set the marker type.  Initially this is CUBE, and cycles between that and SPHERE, ARROW, and CYLINDER
    goal.type = shape;
    // Set the marker action.  Options are ADD, DELETE, and new in ROS Indigo: 3 (DELETEALL)
    goal.action = visualization_msgs::Marker::ADD;
    // Set the pose of the marker.  This is a full 6DOF pose relative to the frame/time specified in the header
    goal.pose.position.x = -6;
    goal.pose.position.y = -7;
    goal.pose.position.z = 0;
    goal.pose.orientation.x = 0.0;
    goal.pose.orientation.y = 0.0;
    goal.pose.orientation.z = 0.0;
    goal.pose.orientation.w = 1.0;

    // Set the scale of the marker -- 1x1x1 here means 1m on a side
    goal.scale.x = 0.8;
    goal.scale.y = 0.8;
    goal.scale.z = 0.1;

    // Set the color -- be sure to set alpha to something non-zero!
    goal.color.r = 0.0f;
    goal.color.g = 1.0f;
    goal.color.b = 0.0f;
    goal.color.a = 0.5;

    goal.lifetime = ros::Duration();
}

void mark_range()
{
    range.header.frame_id = "/odom";
    range.header.stamp = ros::Time::now();

    // Set the namespace and id for this marker.  This serves to create a unique ID
    // Any marker sent with the same namespace and id will overwrite the old one
    range.ns = "basic_shapes";
    range.id = 0;

    // Set the marker type.  Initially this is CUBE, and cycles between that and SPHERE, ARROW, and CYLINDER
    range.type = shape;
    // Set the marker action.  Options are ADD, DELETE, and new in ROS Indigo: 3 (DELETEALL)
    range.action = visualization_msgs::Marker::ADD;
    // Set the pose of the marker.  This is a full 6DOF pose relative to the frame/time specified in the header
    range.pose.position.x = 0;
    range.pose.position.y = 0;
    range.pose.position.z = 0;
    range.pose.orientation.x = 0.0;
    range.pose.orientation.y = 0.0;
    range.pose.orientation.z = 0.0;
    range.pose.orientation.w = 1.0;

    // Set the scale of the marker -- 1x1x1 here means 1m on a side
    range.scale.x = 15;
    range.scale.y = 15;
    range.scale.z = 0.1;

    // Set the color -- be sure to set alpha to something non-zero!
    range.color.r = 0.0f;
    range.color.g = 1.0f;
    range.color.b = 0.0f;
    range.color.a = 0.5;

    range.lifetime = ros::Duration();
}

void callback2(scout::goal_srv::Request &req,
              scout::goal_srv::Response &res)
{
    if(req)
    {
        goal.x = req->x;
        goal.y = req->y;
    }

    marker.header.frame_id = "/odom";
    marker.header.stamp = ros::Time::now();

    // Set the namespace and id for this marker.  This serves to create a unique ID
    // Any marker sent with the same namespace and id will overwrite the old one
    marker.ns = "basic_shapes";
    marker.id = 0;

    // Set the marker type.  Initially this is CUBE, and cycles between that and SPHERE, ARROW, and CYLINDER
    marker.type = shape;
    // Set the marker action.  Options are ADD, DELETE, and new in ROS Indigo: 3 (DELETEALL)
    marker.action = visualization_msgs::Marker::ADD;
    // Set the pose of the marker.  This is a full 6DOF pose relative to the frame/time specified in the header
    marker.pose.position.x = goal.x;
    marker.pose.position.y = goal.y;
    marker.pose.position.z = 0;
    marker.pose.orientation.x = 0.0;
    marker.pose.orientation.y = 0.0;
    marker.pose.orientation.z = 0.0;
    marker.pose.orientation.w = 1.0;

    // Set the scale of the marker -- 1x1x1 here means 1m on a side
    marker.scale.x = 0.8;
    marker.scale.y = 0.8;
    marker.scale.z = 0.1;

    // Set the color -- be sure to set alpha to something non-zero!
    marker.color.r = 0.0f;
    marker.color.g = 1.0f;
    marker.color.b = 0.0f;
    marker.color.a = 0.5;

    marker.lifetime = ros::Duration();

    if(goal)
    {
        res.suc = 1
    }
    else
    {
        res.suc = 0
    }
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "RL_input");
    ros::NodeHandle n;
    ros::Subscriber sub = n.subscribe("odom", 1000, callback);
    ros::Publisher pub = n.advertise<scout::RL_input_msgs>("RLin",1000);

    // ros::ServiceServer service = n.advertiseService("goal_sent", callback2);
    // ros::Publisher pub2 = n.advertise<visualization_msgs::Marker>("goal_marker",1000);

    ros::Publisher pub3 = n.advertise<visualization_msgs::Marker>("goal_marker",1000);
    ros::Publisher pub4 = n.advertise<visualization_msgs::Marker>("goal_marker",1000);
    mark_goal();
    mark_range();

    while(ros::ok())
    {
        ros::AsyncSpinner spinner(2);
        spinner.start();
        pub.publish(pub_msg);
        pub3.publish(goal);
        pub4.publish(range);
        spinner.stop();
    }
    return 0;
}