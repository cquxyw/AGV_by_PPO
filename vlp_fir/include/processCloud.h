//
// Created by Allen.X on 2019/10/29.
//

#ifndef VLP_FIR_PROCESSCLOUD_H
#define VLP_FIR_PROCESSCLOUD_H

#include <ctime>
#include <vector>
#include <string>
#include <chrono>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <iostream>
#include <pcl/point_types.h>
#include <pcl/kdtree/kdtree.h>
#include <pcl/filters/crop_box.h>
#include <pcl/ModelCoefficients.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/segmentation/extract_clusters.h>
#include <pcl/sample_consensus/method_types.h>//随机参数估计方法头文件
#include <pcl/sample_consensus/model_types.h> //模型定义头文件
#include <pcl/segmentation/sac_segmentation.h>//基于采样一致性分割的类的头文件
#include <pcl/features/moment_of_inertia_estimation.h>
#include <pcl/filters/statistical_outlier_removal.h>
#include "serial_port.h"

template <typename  PointT>
class ProcessPointClouds {
public:
    std::vector<pcl::PointXYZ> save_MaxPoint;
    std::vector<pcl::PointXYZ> save_MinPoint;
    //SerialPort *My_Serial = new SerialPort("/dev/ttyUSB0",115200,8,1,"N");
    ProcessPointClouds();
    ~ProcessPointClouds();
    typename pcl::PointCloud<PointT>::Ptr Filter_Grid (typename pcl::PointCloud<PointT>::Ptr cloud,int left,int right,int row,int column,double grid_size);
    typename pcl::PointCloud<PointT>::Ptr FilterCloud_D (typename pcl::PointCloud<PointT>::Ptr cloud,float filter_leafSize,int neibor_Num,Eigen::Vector4f minPoint,Eigen::Vector4f maxPoint);
    std::pair<typename pcl::PointCloud<PointT>::Ptr,typename pcl::PointCloud<PointT>::Ptr> segmentPlane_RANSAC(typename pcl::PointCloud<PointT>::Ptr cloud, int maxIterations, float distanceThreshold);
    std::vector<typename pcl::PointCloud<PointT>::Ptr> EuclideanCluster(typename pcl::PointCloud<PointT>::Ptr cloud,int minSize,int maxSize);
    void Boxing(typename pcl::PointCloud<PointT>::Ptr cloud,std::vector<PointT> &a,std::vector<PointT> &b);
    void renderPointCloud(const typename pcl::PointCloud<PointT>::Ptr cloud,int color_r,int color_g,int color_b);
    void send_msg(typename std::vector<PointT> &,std::vector<PointT> &,int size);

};









#endif //VLP_FIR_PROCESSCLOUD_H

