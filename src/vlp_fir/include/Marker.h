//
// Created by little-bird on 2019/10/31.
//

#ifndef VLP_FIR_MARKER_H
#define VLP_FIR_MARKER_H


#include <visualization_msgs/Marker.h>
#include <pcl_conversions/pcl_conversions.h>
#include "/home/xyw/BUAA/Graduation/devel/include/vlp_fir/send_msgs.h"
using namespace std;
vlp_fir::send_msgs marker_(vector<pcl::PointXYZ> &save_aabb_max,vector<pcl::PointXYZ> &save_aabb_min,visualization_msgs::Marker &marker,int n,int i);
#endif
