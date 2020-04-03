#include <ros/ros.h>
//#include <serial_port.h>
#include <processCloud.h>
#include <ctime>
#include <serial_port.h>
#include <Marker.h>
#include "processCloud.cpp"
#include <pcl/PCLPointCloud2.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <visualization_msgs/Marker.h>
#include "vlp_fir/send_msgs.h"
#include "vlp_fir/obs_info.h"
using namespace std;
//SerialPort *My_Serial;
ProcessPointClouds<pcl::PointXYZ>* PointProcessorI = new ProcessPointClouds<pcl::PointXYZ>();

class object3dDetector{

        /*************Publish And  Subcriber*************/
private:
    ros::NodeHandle n;
    ros::Subscriber point_date_sub;
    ros::Publisher  maker_cube_pub;
    ros::Subscriber Livox_date_sub; 
    ros::Publisher point_pub;
    ros::Publisher send_ros;
    vlp_fir::send_msgs obj;
    vlp_fir::obs_info obs_info;
    sensor_msgs::PointCloud2 pc2;

    visualization_msgs::Marker marker;
    std::vector<pcl::PointXYZ> save_MaxPoint;
    std::vector<pcl::PointXYZ> save_MinPoint;

public:
 object3dDetector()
 {
//     ----------------------sub and scrb defination----------------------
     //point_date_sub = n.subscribe("/velodyne_points",10,&object3dDetector::callback,this);
     point_pub = n.advertise<sensor_msgs::PointCloud2>("/processPoint",10);
     Livox_date_sub = n.subscribe("/livox/lidar",10,&object3dDetector::callback,this) ;
     maker_cube_pub = n.advertise<visualization_msgs::Marker>("/box",10);
    //  send_ros = n.advertise<vlp_fir::send_msgs>("obj_",10);
     send_ros = n.advertise<vlp_fir::obs_info>("obj_",10);
 }

 void callback(const sensor_msgs::PointCloud2::ConstPtr& msg)
 {
     std::vector<int>indices_leave;
     pcl::PointCloud<pcl::PointXYZ>::Ptr temp_cloud(new pcl::PointCloud<pcl::PointXYZ>);
     pcl::fromROSMsg(*msg, *temp_cloud);
     pcl::PointCloud<pcl::PointXYZ>::Ptr filterCloud = PointProcessorI->FilterCloud_D(temp_cloud,0.2,50,Eigen::Vector4f(-1,-5,-2,1),Eigen::Vector4f(50,5,1,1));
//     remove the NaN invalid points
     pcl::removeNaNFromPointCloud(*filterCloud,*filterCloud, indices_leave);

//     --------------------------------Do EUCLEANCluster and segementate plane------------------------------

     #if 0
     pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_grid = PointProcessorI->Filter_Grid(filterCloud,10,-10,80,40,0.5);
     std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> cloudClusters = PointProcessorI->EuclideanCluster(cloud_grid,3,20000);
     int clusterID = 0;
     std::cout<<"There has["<<cloudClusters.size()<<"] obj!"<<endl;
     for(int i =0;i<cloudClusters.size();i++) {
         PointProcessorI->Boxing(cloudClusters[i], save_MaxPoint, save_MinPoint);
         std::cout<<"-"<<cloudClusters[i]->points.size()<<"-";
     } std::cout<<endl;
     for(int i = 0;i < save_MaxPoint.size();i++ ) {
        obj =  marker_(save_MaxPoint, save_MinPoint, marker, clusterID, i);
         send_ros.publish(obj);
         maker_cube_pub.publish(marker);
         clusterID++;
     }
     pcl::toROSMsg(*cloud_grid,pc2);
    #else
//get segment plane and without
     std::pair<pcl::PointCloud<pcl::PointXYZ>::Ptr,pcl::PointCloud<pcl::PointXYZ>::Ptr> segmentCloud = PointProcessorI->segmentPlane_RANSAC(filterCloud,1000,0.15);
     std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> cloudClusters = PointProcessorI->EuclideanCluster(segmentCloud.first, 10, 20000);
     int clusterID = 0;
     std::cout<<"There has["<<cloudClusters.size()<<"] obj!"<<endl;
     for(int i =0;i<cloudClusters.size();i++) {
         PointProcessorI->Boxing(cloudClusters[i], save_MaxPoint, save_MinPoint);
         std::cout<<"-"<<cloudClusters[i]->points.size()<<"-";
     } std::cout<<endl;
     for(int i = 0;i < save_MaxPoint.size();i++ ) {
         obj =  marker_(save_MaxPoint, save_MinPoint, marker, clusterID, i);

        // modify
         obs_info.x[i] = obj.x;
         obs_info.y[i] = obj.y;
         obs_info.len[i] = obj.len;
         obs_info.width[i] = obj.width;
         send_ros.publish(obs_info);

        //  send_ros.publish(obj);
         maker_cube_pub.publish(marker);
         clusterID++;
     }
   // PointProcessorI->renderPointCloud(segmentCloud.first,0,255,0);
    pcl::toROSMsg(*segmentCloud.second,pc2);
    #endif
  //   PointProcessorI->send_msg(save_MinPoint,save_MaxPoint,save_MaxPoint.size());
     save_MaxPoint.clear();
     save_MinPoint.clear();
     point_pub.publish(pc2);
 }

  };

 int  main(int argc,char **argv)
 {
//     My_Serial = new SerialPort("/dev/ttyUSB0",115200,8,1,"N");
     cout<<"------------------DO it!-----------------------"<<endl;
     ros::init(argc,argv,"object3d_detector");
     object3dDetector A;
     ros::spin();
//     while(ros::ok())
//     {
//         ros::Rate loop_rate(10);//2 HZ
//         ros::spinOnce();
//         loop_rate.sleep();
//     }
//     return 0;
//
//     ros::MultiThreadedSpinner s(2);
//     ros::spin(s);
 }