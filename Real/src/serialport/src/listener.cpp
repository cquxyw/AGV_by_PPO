#include "ros/ros.h"
#include "std_msgs/String.h"
#include "serialport/GPS.h"
#include <iomanip>
void chatterCallback(const serialport::GPSConstPtr& msg)
{
    std::cout << std::setiosflags(std::ios::fixed) << std::setprecision(7) << "纬度：" << msg->lat << " 经度：" << msg->lon <<" 高程：" << msg->hgt<< "\n";
    std::cout << std::setiosflags(std::ios::fixed) << std::setprecision(7) << "北向速度：" << msg->vel_n << " 东向速度：" << msg->vel_e <<" 天向速度：" << msg->vel_s<< "\n";
    std::cout << std::setiosflags(std::ios::fixed) << std::setprecision(7) << "滚转：" << msg->ang_r << " 俯仰：" << msg->ang_p <<" 偏航：" << msg->ang_y<< "\n";
    std::cout << std::setiosflags(std::ios::fixed) << std::setprecision(7) << "时间：" << msg->stamp << "\n";
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "listener");
    ros::NodeHandle n;
    ros::Subscriber sub = n.subscribe("GPS", 1000, chatterCallback);
    ros::spin();
    return 0;
}