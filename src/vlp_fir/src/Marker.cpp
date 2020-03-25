//
// Created by little-bird on 2019/10/31.
//

#include <Marker.h>

using namespace std;
vlp_fir::send_msgs obj1;
vlp_fir::send_msgs marker_(vector<pcl::PointXYZ> &save_aabb_max,vector<pcl::PointXYZ> &save_aabb_min,visualization_msgs::Marker &marker,int n,int i){
    //marker.header.frame_id = "velodyne";
    marker.header.frame_id = "lidar";
    marker.header.stamp = ros::Time();
    marker.ns = "my_namespace";
    marker.id = n;
    marker.type = visualization_msgs::Marker::CUBE;
    marker.action = visualization_msgs::Marker::ADD;

    marker.pose.position.x = (save_aabb_max[i].x + save_aabb_min[i].x)/2;
    marker.pose.position.y = (save_aabb_max[i].y + save_aabb_min[i].y)/2;
    marker.pose.position.z = (save_aabb_max[i].z + save_aabb_min[i].z)/2;

    cout<<"x "<< marker.pose.position.x<<"  y "<<marker.pose.position.y<<endl;
    marker.pose.orientation.x = 0.0;
    marker.pose.orientation.y = 0.0;
    marker.pose.orientation.z = 0.0;
    marker.pose.orientation.w = 1.0;

    marker.scale.x = save_aabb_max[i].x - save_aabb_min[i].x;
    marker.scale.y = save_aabb_max[i].y - save_aabb_min[i].y;
    marker.scale.z = save_aabb_max[i].z - save_aabb_min[i].z;

    marker.color.a = 1; // Don't forget to set the alpha!
    marker.color.r = 0.0;
    marker.color.g = 1.0;
    marker.color.b = 0.0;
    marker.lifetime = ros::Duration(0.1);
    cout<<"L:"<<marker.scale.x<<"  W:"<<marker.scale.y<<" H:"<<marker.scale.z<<endl;
    if(save_aabb_max.size()>0) {
        obj1.num = save_aabb_max.size();
        obj1.x = marker.pose.position.x;
        obj1.y = marker.pose.position.y;
        obj1.z = marker.pose.position.z;
        obj1.len = marker.scale.x;
        obj1.width = marker.scale.y;
        obj1.height = marker.scale.z;
        obj1.date = 1;

    }
    else {
        obj1.date = 0;
        obj1.num = 0;
    }
    return obj1;

}