#include <iostream>
#include <ros/ros.h>
#include "serialport/GPS.h"
#include <geometry_msgs/PoseStamped.h>
// #include <nav_msgs/Path.h>
#include "gpstoenu/enu.h"
#include "geodetic_conv.hpp"

using namespace std;

gpstoenu::enu data;
// geometry_msgs::PoseStamped myloc;
// nav_msgs::Path path_track;
double x, y, z;

// 坐标转换参考点初始化
double lat_ref = 40.15596159682;
double lon_ref = 116.26572619231;
double hgt_ref = 48.196;

void callback(const serialport::GPS::ConstPtr &msg)
{
    double lat = msg->lat;
    double lon = msg->lon;
    double hgt = msg->hgt;
    geodetic_converter::GeodeticConverter Conv;
    
    Conv.initialiseReference(lat_ref, lon_ref, hgt_ref);
    
    double init_lat, init_lon, init_alt;
    Conv.getReference(&init_lat, &init_lon, &init_alt);

    if (!Conv.isInitialised())
    {
        ROS_INFO("Warning: No GPS Reference Points Are Set! \n");
    }

    Conv.geodetic2Enu(lat,lon,hgt, &x, &y, &z);

    data.x = y;
    data.y = -x;

    // myloc.pose.position.x = x;
    // myloc.pose.position.y = y;
    // myloc.pose.position.z = 0;
    
    cout << "X轴距离: " << data.x<< "; " << "Y轴距离: " << data.y << endl;
    cout << "" << endl;
}

int main(int argc, char ** argv)
{
    ros::init(argc, argv, "gpstoenu");
    ros::NodeHandle n;
    
    ros::Subscriber sub = n.subscribe("GPS", 1000, callback);
    ros::Publisher pub = n.advertise<gpstoenu::enu>("enu", 1000);

    // ros::Publisher pub2 = n.advertise<gpstoenu::enu>("enu", 1000);

    // myloc.header.frame_id="lidar";

    while (ros::ok())
    {
        ros::AsyncSpinner spinner(2);
        spinner.start();

        pub.publish(data);

        // path_track.poses.push_back(myloc);
        // pub2.publish(path_track);

        spinner.stop();
    }
    return 0;
}
