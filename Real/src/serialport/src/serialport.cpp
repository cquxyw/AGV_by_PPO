#include <ros/ros.h> 
#include <serial/serial.h>  //ROS已经内置了的串口包 
#include <std_msgs/String.h>
#include <std_msgs/Empty.h> 
#include <string>
#include <vector>
#include <sstream>
#include <cmath>
#include <cstdlib>//string转化为double
#include <iomanip>//保留有效小数
#include "serialport/GPS.h"
serial::Serial ser; //声明串口对象

using namespace std;

//解析GPS
void RecePro(ros::Publisher pub, std::string s,long int* count)//, double& lat, double& lon,double& hgt,double& vel_n,double& vel_e,double& vel_s,double& ang_r,double& ang_p,double& ang_y )
{
    //分割有效数据，存入vector中
    double lat, lon, hgt, vel_n, vel_e, vel_s, ang_r, ang_p, ang_y;
    //WGS84坐标系下维度，经度，高程，北向速度，东向速度，天向速度，横滚角，俯仰角，航向角
    serialport::GPS GPS_data;
    std::vector<std::string> v;
    std::string::size_type pos1, pos2;
    pos2 = s.find(",");
    pos1 = 0;
    while ( std::string::npos !=pos2 )
    {
        v.push_back( s.substr( pos1, pos2-pos1 ) );
        pos1 = pos2 + 1;
        pos2 = s.find(",",pos1);
    }
    if ( pos1 != s.length() )
        v.push_back( s.substr( pos1 ));
    //解析出经纬度
    if (v.max_size() >= 12 && v[2].length()<=14 && v[3].length()<=15)
    {  
        if (v[2] != "") lat = std::atof(v[2].c_str()) ;//纬度
        if (v[3] != "") lon = std::atof(v[3].c_str()) ;//经度
        if (v[4] != "") hgt = std::atof(v[4].c_str()) ;
        if (v[6] != "") vel_n = std::atof(v[6].c_str()) ;
        if (v[7] != "") vel_e = std::atof(v[7].c_str()) ;
        if (v[8] != "") vel_s = std::atof(v[8].c_str()) ;
        if (v[9] != "") ang_r = std::atof(v[9].c_str()) ;
        if (v[10] != "") ang_p = std::atof(v[10].c_str()) ;
        if (v[11] != "") ang_y = std::atof(v[11].c_str()) ;
        //std::cout <<*count<< " 纬度：" <<setprecision(14)<< lat << " 经度："<<setprecision(15)<< lon << "\n";
        cout<<*count;                   
           
        //发布消息到话题
        GPS_data.lat = lat;
        GPS_data.lon = lon;
        GPS_data.hgt = hgt;
        GPS_data.vel_n = vel_n;
        GPS_data.vel_e = vel_e;
        GPS_data.vel_s = vel_s;
        GPS_data.ang_r = ang_r;
        GPS_data.ang_p = ang_p;
        GPS_data.ang_y = ang_y;
        GPS_data.stamp = ros::Time::now();
        pub.publish(GPS_data);

        std::cout << " 纬度：" <<setprecision(14)<< lat << " 经度："<<setprecision(15)<< lon << "  高度: "<< hgt << "  航向角: " <<  ang_y << "\n";             
        *count=*count+1;
    }
}


int main(int argc, char** argv)
{
    //初始化节点
    ros::init(argc, argv, "serialport");
    //声明节点句柄
    ros::NodeHandle nh;
    //注册Publisher到话题GPS
    ros::Publisher GPS_pub = nh.advertise<serialport::GPS>("/GPS",1000);
    try
    {
      //串口设置
      ser.setPort("/dev/ttyS0");
      ser.setBaudrate(115200);
      serial::Timeout to = serial::Timeout::simpleTimeout(1000);
      ser.setTimeout(to);
      ser.open();
    }
    catch (serial::IOException& e)
    {
        ROS_ERROR_STREAM("Unable to open Serial Port !");
        return -1;
    }
    if (ser.isOpen())
    {
        ROS_INFO_STREAM("Serial Port initialized");
    }
    else
    {
        return -1;
    }

    ros::Rate loop_rate(20);
    long int k=0;
    std::string strRece;
    while (ros::ok())
    {
        if (ser.available())
        {
            //1.读取串口信息：
            ROS_INFO_STREAM("Reading from serial port\n");
            //通过ROS串口对象读取串口信息
            //std::cout << ser.available();
            //std::cout << ser.read(ser.available());
            strRece += ser.read(ser.available());
            //std::cout << "strRece:" << strRece<< "\n" ;            
            //strRece = "#INSPVAXA,COM3,0,39.5,UNKNOWN,0,80.000,1a448000,471d,14695;WAITING_INITIALPOS,NONE,0.00000000000,0.00000000000,0.0000,0.0000,0.0000,0.0000,0.0000,0.000000000,0.000000000,0.000000000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,01000000,0*2b044605\r\n";
            //2.截取数据、解析数据：
            //GPS起始标志
            //std::string gstart = "$GNGGA";//开头
            std::string gstart = ";";//开头
            //std::string gstart = "$GPRMC";//开头            
            //GPS终止标志
            std::string gend = "\r\n";
            int i = 0, start = -1, end = -1;

            while ( i < strRece.length() )
            {
                //找起始标志
                start = strRece.find(gstart);
                //std::cout<<"start="<<start<<"\n";
                //如果没找到，丢弃这部分数据，但要留下最后2位,避免遗漏掉起始标志
                if ( start == -1)
                {
                    if (strRece.length() > 2)   
                        strRece = strRece.substr(strRece.length()-3);
                        break;
                }
                //如果找到了起始标志，开始找终止标志
                else
                {
                    //找终止标志
                    end = strRece.find(gend,start);//从start往后找，否则last会在start前面
                    //std::cout<<"end="<<end<<"\n";
                    //如果没找到，把起始标志开始的数据留下，前面的数据丢弃，然后跳出循环
                    if (end == -1)
                    {
                        if (end != 0)
                        strRece = strRece.substr(start);
                        break;
                    }
                    //如果找到了终止标志，把这段有效的数据剪切给解析的函数，剩下的继续开始寻找
                    else
                    {
                        i = end;
                        //把有效的数据给解析的函数以获取经纬度
                        //cout<<"test="<<strRece.substr(start,end+2-start)<<endl;
                        RecePro(GPS_pub, strRece.substr(start,end+2-start), &k);//,lat,lon,hgt,vel_n,vel_e,vel_s,ang_r,ang_p,ang_y);
                        //std::cout << std::setiosflags(std::ios::fixed)<<std::setprecision(7)<< "纬度：" << lat << " 经度："<< lon << "\n";
                        //如果剩下的字符大于等于4，则继续循环寻找有效数据,如果所剩字符小于等于3则跳出循环
                        if ( i+5 < strRece.length())
                            strRece = strRece.substr(end+2);
                        else
                        {   strRece = strRece.substr(end+2);
                            break;
                        }
                    }
                }
            }
        }
    ros::spinOnce();
    loop_rate.sleep();
    }

    cout<<"GPS node closed"<<endl;
    return 0;
}
