#include "ros/ros.h"  //ros需要的头文件
#include <geometry_msgs/Twist.h>//不确定是否还需要
#include <string>        
#include <iostream>
#include <unistd.h>//sleep头文件
#include "controlcan.h"//LinuxCAN卡头文件，注意拷贝文件***********************
#include<stdio.h>//不确定是否还需要
#include<stdlib.h>//不确定是否还需要
#include "can_listener/vel_can.h"

using namespace std;
typedef unsigned char uint8;//CAN卡通信用数据格式
typedef unsigned short int uint16;//CAN卡通信用数据格式

//float linear_temp=0,angular_temp=0;//暂存的线速度和角速度

int nDeviceType=4;	//CAN卡类型号，参考头文件，#define VCI_USBCAN2		4，usbminican-II按照USBCAN2设置
int nDeviceInd=0;	//设备索引号，只有1个
int nReserved=0;	//保留
int nCanInd=1;		//CAN接口号，0为工控机右侧接口*****************************

int main(int argc, char **argv)
{

	//初始化节点
    ros::init(argc, argv, "can_listener");
    //声明节点句柄
    ros::NodeHandle nh;
    //注册Publisher到话题vel_can
    ros::Publisher vel_can_pub = nh.advertise<can_listener::vel_can>("vel_can",1000);

/******************can初始化、启动、测试****************************/
	if (VCI_OpenDevice(nDeviceType, nDeviceInd, nReserved)==1)//CAN卡设备开启
	{
		cout << "VCI_OpenDevice succeeded" << endl;
	}
	else
	{
		cout<<"VCI_OpenDevice failed"<<endl;
	}

	VCI_INIT_CONFIG vic;//CAN参数配置结构体
	vic.AccCode=0;//验收码
	vic.AccMask=0xFFFFFFFF;//屏蔽码，0xFFFFFFFF全接收
	vic.Filter=1;//1单滤波，0双滤波
	vic.Timing0=0x00;//参照CAN卡说明书查询，此处对应波特率500k**********************
	vic.Timing1=0x1C;//参照CAN卡说明书查询，此处对应波特率500k**********************
	vic.Mode=0;//0正常模式，1只听模式
	if (VCI_InitCAN(nDeviceType, nDeviceInd, nCanInd, &vic)==1)//CAN卡初始化
	{
		cout << "VCI_InitCan succeeded" << endl;
	}
	else
	{
		cout<<"VCI_InitCan failed"<<endl;
	}
	
	if (VCI_StartCAN(nDeviceType, nDeviceInd, nCanInd)==1)//CAN卡开启
	{
		cout << "VCI_StartCan succeeded" << endl;
	}
	else
	{
		cout<<"VCI_StartCan failed"<<endl;
	}	
/*****************can初始化、启动、测试****************************/

/******************************************接收并发布底盘上传帧数据***************************/
	int num=0;//CAN卡缓存区帧数量
	VCI_CAN_OBJ vco[100];//帧数据结构体，一次最多获取100条
	int num_rec=0;//接收帧数量
    short int vel_v=0;//接收线速度m/s*1000
	float fwd=0;//换算线速度m/s
	short int vel_w=0;//接收转角rad*1000
	float ang=0;//换算转角 度
	short int warn=0;//报警消息值


	ros::Rate loop_rate(50);//接收频率50Hz
    while (ros::ok())
    {
		num=0;
		num=VCI_GetReceiveNum(nDeviceType, nDeviceInd, nCanInd);//获取CAN卡缓存区帧数量
		if (num>100)
		{
			num=100;
		}
		num_rec=0;
        num_rec=VCI_Receive(nDeviceType, nDeviceInd, nCanInd, vco, 100, 200);//获取CAN卡缓存区帧数据，最大100条，如果无数据等待200ms无响应后退出
        for(int i=0; i<num_rec; i++)
        {
            //cout<<"receive succeeded"<<endl;
            //cout<<"ID="<<(unsigned int) vco[i].ID<<endl;
            if(0)//输出全部接收帧数据
            {
                cout<<"ID="<<hex<< vco[i].ID<<endl;
                for(int j=0; j<8; j++)
                {
                    cout<<dec<<(unsigned int) vco[i].Data[j]<<"-";
                }
                cout<<endl;
            }

            if(vco[i].ID==0x00000131)//仅接收运动回馈0x131
            {
                cout<<"运动回馈ID="<<hex<< vco[i].ID<<endl;
                //cout<< "v="<< dec <<(unsigned int) vco[i].Data[2]<<"-"<< dec <<(unsigned int) vco[i].Data[3]<<endl;
                vel_v=0;
				fwd=0;
                vel_v =vco[i].Data[0];
                vel_v <<=8;
                vel_v |=vco[i].Data[1];
				fwd=(float)vel_v/1000;
                cout<< "线速度=" << dec << fwd<< "m/s"<<endl;
                vel_w=0;
				ang=0;
                vel_w =vco[i].Data[2];
                vel_w <<=8;
                vel_w |=vco[i].Data[3];
				ang=(float)vel_w/1000;
                cout<< "角速度=" << dec << ang<< "rad/s"<<endl;	

				//发布消息到话题
                can_listener::vel_can vel_can_data;
				vel_can_data.v=fwd;//m/s
				vel_can_data.w=ang;//degree
				vel_can_pub.publish(vel_can_data);
            }
			//if(0)
            if(vco[i].ID==0x00000151)//接收系统状态回馈0x151
            {
                //cout<<"系统状态回馈ID="<<hex<< vco[i].ID<<endl;
                //cout<< "v=" << dec <<(unsigned int) vco[i].Data[2]<<"-"<< dec <<(unsigned int) vco[i].Data[3]<<endl;
                warn=0;
                warn =vco[i].Data[4];
                warn <<=8;
                warn |=vco[i].Data[5];
                //cout<< "warn=" << dec << warn<<endl;
				//cout<<dec<<(unsigned int) vco[i].Data[5]<<endl;
				if(warn==0)
				{
					//cout<< "无故障"<< endl;
				}
				else
				{
					cout<< "出现故障"<< endl;
				}
            }
        }
        //sleep(0.02);//单位秒
		ros::spinOnce();
		loop_rate.sleep();
    }
/******************************************接收并发布底盘上传帧数据***************************/

    ros::spinOnce();    
	if (VCI_CloseDevice(nDeviceType, nDeviceInd)==1)//CAN卡关闭
	{
		cout << "VCI_CloseDevice succeeded" << endl;
	}
	else
	{
		cout<<"VCI_CloseDevice failed"<<endl;
	}

	return 0;
}
