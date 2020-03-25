
#include <processCloud.h>


using namespace std;

//constructor
template <typename PointT>
ProcessPointClouds<PointT>::ProcessPointClouds(){}
//deconstructor
template <typename PointT>
ProcessPointClouds<PointT>::~ProcessPointClouds(){}

template <typename PointT>
typename pcl::PointCloud<PointT>::Ptr
ProcessPointClouds<PointT>:: FilterCloud_D(typename pcl::PointCloud<PointT>::Ptr cloud,float filter_leafSize,int neibor_Num,Eigen::Vector4f minPoint,Eigen::Vector4f maxPoint){

    typename pcl::PointCloud<PointT>::Ptr cloudFiltered(new pcl::PointCloud<PointT>());
    typename pcl::PointCloud<PointT>::Ptr cloudRegion(new pcl::PointCloud<PointT>());
    typename pcl::PointCloud<PointT>::Ptr cloud_filtered(new pcl::PointCloud<PointT>());
    typename pcl::PointCloud<PointT>::Ptr cloud_remo(new pcl::PointCloud<PointT>());
    auto startTime = std::chrono::steady_clock::now();

    // TODO:: Fill in the function to do voxel grid point reduction and region based filtering
    //creat the filtering object:downsample the dataset using a leaf size of filter_leafSize
    typename pcl::VoxelGrid<PointT>sor;
    sor.setInputCloud(cloud);
    sor.setLeafSize(filter_leafSize,filter_leafSize,filter_leafSize);
    sor.filter(*cloudFiltered);

    typename pcl::StatisticalOutlierRemoval<PointT> st;
    st.setInputCloud (cloudFiltered);
    st.setMeanK(neibor_Num);
    st.setStddevMulThresh(1.0);
    st.filter (*cloud_remo);

    typename pcl::CropBox<PointT> Car_roof;
    Car_roof.setInputCloud(cloud_remo);
    //filter surround point of the car
    Car_roof.setMin(Eigen::Vector4f(-0.5,-0.5,-1,1));
    Car_roof.setMax((Eigen::Vector4f(0.2,0.3,0.2,1)));
    Car_roof.setNegative(true);
    Car_roof.filter(*cloudRegion);
    //region we deal!
    typename pcl::CropBox<PointT> region;
    region.setInputCloud(cloudRegion);
    region.setMin(minPoint);
    region.setMax(maxPoint);
    region.setNegative(false);
    region.filter(*cloud_filtered);
    return cloud_filtered;

}

template <typename PointT>
std::pair<typename pcl::PointCloud<PointT>::Ptr,typename pcl::PointCloud<PointT>::Ptr>
ProcessPointClouds<PointT>::segmentPlane_RANSAC(typename pcl::PointCloud<PointT>::Ptr cloud, int maxIterations, float distanceThreshold){
    //cloudInliers is plane cloudOutliers is the point which remove the plane
    typename pcl::PointCloud<PointT>::Ptr cloudInliers(new pcl::PointCloud<PointT>());
    typename pcl::PointCloud<PointT>::Ptr cloudOutliers(new pcl::PointCloud<PointT>());
    //Create coefficients obj
    pcl::ModelCoefficients::Ptr coefficients (new pcl::ModelCoefficients);
    //inliers表示误差能容忍的点 记录的是点云的序号
    pcl::PointIndices::Ptr inliers (new pcl::PointIndices);
    // Create the segmentation object
    pcl::SACSegmentation<pcl::PointXYZ> seg;
    // Optional
    seg.setOptimizeCoefficients (true);
    // Mandatory-设置目标几何形状
    seg.setModelType (pcl::SACMODEL_PLANE);
    seg.setMaxIterations(maxIterations);
    //分割方法：随机采样法
    seg.setMethodType (pcl::SAC_RANSAC);
    //设置误差容忍范围
    seg.setDistanceThreshold (distanceThreshold);
    //输入点云
    seg.setInputCloud (cloud);
    //分割点云
    seg.segment (*inliers, *coefficients);
    //indices聚类所包含的点集的所有索引
    if (inliers->indices.size () == 0)
    {
        std::cerr << "Could not estimate a planar model for the given dataset." << std::endl;
    }

    pcl::ExtractIndices<pcl::PointXYZ> extract;
//                extract.setInputCloud (filterZ);
    extract.setInputCloud (cloud);
    extract.setIndices (inliers);
    extract.setNegative(false);
    extract.filter (*cloudInliers);

    extract.setNegative(true);
    extract.filter(*cloudOutliers);

    std::pair<typename pcl::PointCloud<PointT>::Ptr, typename pcl::PointCloud<PointT>::Ptr> segResult(cloudOutliers,cloudInliers);

    return segResult;

}
template <typename PointT>
std::vector<typename pcl::PointCloud<PointT>::Ptr>
ProcessPointClouds<PointT>:: EuclideanCluster(typename pcl::PointCloud<PointT>::Ptr cloud,int minSize,int maxSize){

    std::vector<typename pcl::PointCloud<PointT>::Ptr> clusters;
    typename pcl::search::KdTree< PointT>::Ptr tree (new pcl::search::KdTree<PointT>);
    std::vector<pcl::PointIndices> cluster_indices;
    pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
    tree->setInputCloud (cloud);
    ec.setClusterTolerance (0.5);
    ec.setMinClusterSize (minSize);
    ec.setMaxClusterSize (maxSize); //300
    ec.setSearchMethod (tree);
    ec.setInputCloud (cloud);
    ec.extract (cluster_indices);

    for(std::vector<pcl::PointIndices>::const_iterator it = cluster_indices.begin();it != cluster_indices.end();++it){
        typename pcl::PointCloud<PointT>::Ptr cloudCluster (new pcl::PointCloud<PointT>);
        for(std::vector<int>::const_iterator pd = it->indices.begin();pd != it->indices.end();++pd)
            cloudCluster->points.push_back(cloud->points[*pd]);
            cloudCluster->width = cloudCluster->points.size ();
            cloudCluster->height = 1;
            cloudCluster->is_dense = true;
            clusters.push_back(cloudCluster);
            }
    return clusters;

}
template <typename PointT>
void
ProcessPointClouds<PointT>::Boxing(typename pcl::PointCloud<PointT>::Ptr obj,std::vector<PointT> &a,std::vector<PointT> &b){


    PointT min_point_AABB;
    PointT max_point_AABB;
    PointT min_point_OBB;
    PointT max_point_OBB;
    PointT position_OBB;

    pcl::MomentOfInertiaEstimation <PointT> feature_extractor;
    feature_extractor.setInputCloud (obj);
    feature_extractor.compute ();
//
    std::vector <float> moment_of_inertia;
    std::vector <float> eccentricity;
//
    Eigen::Matrix3f rotational_matrix_OBB;
    float major_value, middle_value, minor_value;
    Eigen::Vector3f major_vector, middle_vector, minor_vector;
    Eigen::Vector3f mass_center;
//
    feature_extractor.getMomentOfInertia (moment_of_inertia);//特征提取获取惯性距
    feature_extractor.getEccentricity (eccentricity);//特征提取获取离心率
    feature_extractor.getAABB (min_point_AABB, max_point_AABB);//特征提取AABB
    feature_extractor.getOBB (min_point_OBB, max_point_OBB, position_OBB, rotational_matrix_OBB);//特征提取OBB，position是OBB中心相对AABB中心移动的位移
    feature_extractor.getEigenValues (major_value, middle_value, minor_value);//获取特征值
    feature_extractor.getEigenVectors (major_vector, middle_vector, minor_vector);//获取特征向量
    feature_extractor.getMassCenter (mass_center);//获取最大质心，即点云中心坐标
    a.push_back(max_point_AABB);
    b.push_back(min_point_AABB);
}
template <typename PointT>
void
ProcessPointClouds<PointT>::renderPointCloud(const typename pcl::PointCloud<PointT>::Ptr cloud,int r,int g,int b)
{
    pcl::visualization::PCLVisualizer::Ptr viewer (new pcl::visualization::PCLVisualizer ("Real Time Viewer"));
    pcl::visualization::PointCloudColorHandlerCustom<PointT> single_color(cloud, r,g,b); // 点云显示为绿色
    int v1(0); // 左上角
    viewer->createViewPort(0.0, 0.5, 0.5, 1.0, v1);
    viewer->setBackgroundColor(0,0,0,v1);
    viewer->addText("plane",0,0.5,"1",v1);
    int v2(0); // 右上角
    viewer->createViewPort(0.5, 0.5, 1.0, 1.0, v2);
    viewer->setBackgroundColor(0.5,0.5,25,v2);
    viewer->addText("out_plane",0,0.5,"2",v2);
    int v3(0); // 左下角
    viewer->createViewPort(0.0, 0.0, 0.5, 0.5, v3);
    viewer->setBackgroundColor(0.8,0.2,1,v3);
    viewer->addText("",0,0.5,"3",v3);
    int v4(0); // 右下角
    viewer->createViewPort(0.5, 0.0, 1.0, 0.5, v4);
    viewer->setBackgroundColor(0.2,0.5,0.8,v4);
    viewer->addText("",0.5, 0.0,"4",v4);

    viewer->addPointCloud(cloud,single_color,"plane",v1);
    viewer->updatePointCloud(cloud,"plane");
    viewer->spinOnce();
    while(!viewer->wasStopped()){
//        viewer->spinOnce();
    }

}
template <typename PointT>
typename pcl::PointCloud<PointT>::Ptr
ProcessPointClouds<PointT>:: Filter_Grid (typename pcl::PointCloud<PointT>::Ptr cloud,int left,int right,int row,int column,double grid_size){
    class Grid
    {
    public:
        typename pcl::PointCloud<PointT>::Ptr grid_cloud {new pcl::PointCloud<PointT>()};
        pcl::PointIndices::Ptr grid_inliers {new pcl::PointIndices};
        bool low_emp=true;
        float min_height;
    };
    vector<int>save_vec;
    Grid grid[row][column];
    for (int count = 0; count < cloud->points.size(); count++) {
//        cout<<"x:"<<cloud->points[count].x<<endl;
//        cout<<"y:"<<cloud->points[count].y<<endl;
//        cout<<count<<endl;
        int x_grid = floor(double(cloud->points[count].x) / grid_size);//格子边上的点算在下限上。
        int y_grid = floor(double(cloud->points[count].y + (column * grid_size)/2) / grid_size);
        if ((x_grid < row && x_grid >= 0) && (y_grid < column && y_grid >= 0)) {
            grid[x_grid][y_grid].grid_inliers->indices.push_back(count);
            grid[x_grid][y_grid].grid_cloud->points.push_back(cloud->points[count]);
            if (grid[x_grid][y_grid].low_emp) {
                grid[x_grid][y_grid].min_height = cloud->points[count].z;
                grid[x_grid][y_grid].low_emp = false;
            } else {
                if (cloud->points[count].z <grid[x_grid][y_grid].min_height)
                { grid[x_grid][y_grid].min_height = cloud->points[count].z; }
            }
        }
    }
    //--------GRID-------//
    for(int i=0;i<row;i++)
    {
        for(int j=0;j<column;j++)
        {
            int grid_num = grid[i][j].grid_cloud->points.size();
            if(grid[i][j].min_height<0)//雷达安装位置以下
            {
                for(int k=0;k<grid_num;k++)
                {
                    if( (grid[i][j].grid_cloud->points[k].z>(grid[i][j].min_height+0.14)) )//过滤地面
                    {      //0.20
                        if(grid[i][j].grid_cloud->points[k].z<(grid[i][j].min_height+1.6))
                        {     //2.2
                            if((right+0.4< grid[i][j].grid_cloud->points[k].y )&&(grid[i][j].grid_cloud->points[k].y<left-0.4)){
                                save_vec.push_back(grid[i][j].grid_inliers->indices[k]);
                            }
                        }
                    }
                }
            }
        }
    }
    typename pcl::PointCloud<PointT>::Ptr all_piece(new pcl::PointCloud<PointT>());
    pcl::copyPointCloud(*cloud, save_vec , *all_piece);

    return all_piece;
}
template <typename PointT>
void
ProcessPointClouds<PointT>::send_msg(std::vector<PointT> &a, std::vector<PointT> &b, int size) {

    char buffhd[80];
    char* Send_msg;
    string buffhd_str;
    for(int i = 0;i<size-1;i++)
    {
        for(int j = 0;j<size-i-1;j++)
        {
            if(a[j].x >a[j+1].x)
            {
                swap(a[j],a[j+1]);
                swap(b[j],b[j+1]);
            }
        }
    }
    switch(size)
    {
        case 0:
        {
            sprintf(buffhd,"$,%01d,!",0);
            buffhd_str = buffhd;
            Send_msg = const_cast<char*>(buffhd_str.c_str());
            break;
        }
        case 1:
        {
                float obj_x_min=a[0].x;//最近点
                float obj_x = (a[0].x+b[0].x)/2;//障碍物中心点x
                float obj_y = (a[0].y+b[0].y)/2;//障碍物中心点y
                float obj_z = (a[0].z+b[0].z)/2;//障碍物中心点z
                float obj_l = a[0].x - b[0].x;
                float obj_w = b[0].y - a[0].y;//wo障碍物宽度
                float obj_h = b[0].z - a[0].z;//障碍物高度
                sprintf(buffhd,"$,%01d,%04.1f,%04.1f,%04.1f%04.1f,%04.1f,%04.1f,%04.1f,!",1,obj_x_min,
                                                                                           obj_x,obj_y,obj_z,
                                                                                           obj_l,obj_w,obj_h);
                break;
        }
        case 2:
        {
            for(int i = 1;i <= 2;i++)
            {
                float obj_x_min=a[i].x;//最近点
                float obj_x = (a[i].x+b[i].x)/2;//障碍物中心点x
                float obj_y = (a[i].y+b[i].y)/2;//障碍物中心点y
                float obj_z = (a[i].z+b[i].z)/2;//障碍物中心点z
                float obj_l = a[i].x - b[i].x;
                float obj_w = b[i].y - a[i].y;//wo障碍物宽度
                float obj_h = b[i].z - a[i].z;//障碍物高度
                sprintf(buffhd,"$,%01d,%04.1f,%04.1f,%04.1f%04.1f,%04.1f,%04.1f,%04.1f,!",1,obj_x_min,
                                                                                            obj_x,obj_y,obj_z,
                                                                                            obj_l,obj_w,obj_h);
            }
        }
        case 3:
        {
            for(int i = 1;i <= 3;i++)
            {
                float obj_x_min=a[i].x;//最近点
                float obj_x = (a[i].x+b[i].x)/2;//障碍物中心点x
                float obj_y = (a[i].y+b[i].y)/2;//障碍物中心点y
                float obj_z = (a[i].z+b[i].z)/2;//障碍物中心点z
                float obj_l = a[i].x - b[i].x;
                float obj_w = b[i].y - a[i].y;//wo障碍物宽度
                float obj_h = b[i].z - a[i].z;//障碍物高度
                sprintf(buffhd,"$,%01d,%04.1f,%04.1f,%04.1f%04.1f,%04.1f,%04.1f,%04.1f,!",1,obj_x_min,
                                                                                            obj_x,obj_y,obj_z,
                                                                                           obj_l,obj_w,obj_h);
                break;
            }
        }
        default:
        {
            for(int i = 1;i <= 4;i++)
            {
                float obj_x_min=a[i].x;//最近点
                float obj_x = (a[i].x+b[i].x)/2;//障碍物中心点x
                float obj_y = (a[i].y+b[i].y)/2;//障碍物中心点y
                float obj_z = (a[i].z+b[i].z)/2;//障碍物中心点z
                float obj_l = a[i].x - b[i].x;
                float obj_w = b[i].y - a[i].y;//wo障碍物宽度
                float obj_h = b[i].z - a[i].z;//障碍物高度
                sprintf(buffhd,"$,%01d,%04.1f,%04.1f,%04.1f%04.1f,%04.1f,%04.1f,%04.1f,!",1,obj_x_min,
                        obj_x,obj_y,obj_z,
                        obj_l,obj_w,obj_h);
            }
            break;
        }
    }

//    My_Serial->Send(Send_msg,buffhd_str.length());

}
