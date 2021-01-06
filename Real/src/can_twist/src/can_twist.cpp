#include "ros/ros.h"  //ros需要的头文件
#include <geometry_msgs/Twist.h>
#include "can_listener/vel_can.h"
#include <string>        
#include <iostream>

#include "controlcan.h"//LinuxCAN卡头文件，注意拷贝文件***********************
#include<stdio.h>//不确定是否还需要
#include<stdlib.h>//不确定是否还需要

using namespace std;
typedef unsigned char uint8;//CAN卡通信用数据格式
typedef unsigned short int uint16;//CAN卡通信用数据格式

float linear_temp=0,angular_temp=0;//暂存的线速度和角速度
can_listener::vel_can vel_can_data;

int nDeviceType=4;	//CAN卡类型号，参考头文件，#define VCI_USBCAN2		4，usbminican-II按照USBCAN2设置
int nDeviceInd=0;	//设备索引号，只有1个
int nReserved=0;	//保留
int nCanInd=0;		//CAN接口号，0为工控机右侧接口*****************************


static uint8 Checksum(uint16 id, uint8 *data, uint8 len)//发送帧校验位计算函数
{
	int checksum=0x00;
	checksum=(uint8) (id & 0x00ff) + (uint8) (id>>8) + len;
	for(uint8 i=0; i<len-1; i++)
	{
		checksum +=data[i];
	}
	return checksum;
}


void callback(const geometry_msgs::Twist & cmd_input)//订阅/cmd_vel主题回调函数
{

// ---------------------将接收的速度进行数据处理写入数据到串口----------------------------

    angular_temp = cmd_input.angular.z ;//获取/cmd_vel的角速度,rad/s
    linear_temp = cmd_input.linear.x ;//获取/cmd_vel的线速度.m/s
	
	VCI_CAN_OBJ move[1];//发送帧数据结构体
	move[0].ID=0x130;//控制指令ID=0x00000130
	move[0].SendType=0;//类型0正常发送
	move[0].RemoteFlag=0;//数据帧
	move[0].ExternFlag=0;//标准帧
	move[0].DataLen=0x08;//数据长度，底盘接收8位
	move[0].Data[0]= 0x01;//指令模式，0x00遥控，0x01指令
	move[0].Data[1]= 0x00;//故障清除指令
	move[0].Data[2]= 0x00;//线速度，1.5m/s，百分比
	move[0].Data[3]= 0x00;//角速度，0.7853rad/s，百分比
	move[0].Data[4]= 0x00;//保留
	move[0].Data[5]= 0x00;//保留
	move[0].Data[6]= 0x00;//计数校验，暂时不管
	move[0].Data[7]= 0x00;//校验位
 
	// 底盘线速度转换
	int speed_adv=linear_temp/1.5*100;
	if (speed_adv>100)
	{
		speed_adv=100;
	}
	//SCOUT底盘角速度转换
	int speed_spin=angular_temp/0.7853*100;
	// int speed_spin=angular_temp/0.75*100;//*************************HUNTER底盘角速度
	if (speed_spin>100)
	{
		speed_spin=100;
	}	
	move[0].Data[2]= (unsigned char) speed_adv;
	move[0].Data[3]= (unsigned char) speed_spin;
	
	//计算校验位用数组
	uint8 dataout[8];
	for(int i=0; i<8;i++)
	{
		dataout[i]=move[0].Data[i];
	}

	move[0].Data[7]= Checksum((unsigned short int) move[0].ID, dataout, 0x08);
	VCI_Transmit(nDeviceType, nDeviceInd, nCanInd, move, 1);//帧数据发送
}

int main(int argc, char **argv)
{

	system("echo '   ' | sudo -S chmod -R 777 /dev/bus/usb/");
//---------------------------------can初始化、启动、测试------------------------------
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
	
// -----------------------------CAN的ROS节点定义及数据发送-----------------------
    ros::init(argc, argv, "can_twist");
    ros::NodeHandle n;

    ros::Subscriber sub = n.subscribe("cmd_vel",1000,&callback);
	ros::Publisher vel_can_pub = n.advertise<can_listener::vel_can>("vel_can",1000);

	//获取CAN卡缓存区帧数量
	int num=VCI_GetReceiveNum(nDeviceType, nDeviceInd, nCanInd);
		if (num>100)
		{
			num=100;
		}
		VCI_CAN_OBJ vco[100];

	int num_rec=0;
	short int vel_v=0;//接收线速度m/s*1000
	float fwd=0;//换算线速度m/s
	short int vel_w=0;//接收转角rad*1000
	float ang=0;//换算转角 度

	while(ros::ok())
	{
	// --------------------------接收底盘上传帧数据---------------------------------------------
		cout << 1 << endl;
		//获取CAN卡缓存区帧数据，最大100条，如果无数据等待400ms无响应后退出
		num_rec=VCI_Receive(nDeviceType, nDeviceInd, nCanInd, vco, 100, 400);
		cout << num_rec << endl;
		//接收运动回馈0x131
		for(int i=0; i<num_rec; i++)
		{
			cout << 3 << endl;
			if(vco[i].ID==0x00000131)
			{
				cout << 2 << endl;
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

				vel_can_data.v=fwd;//m/s
				vel_can_data.w=ang;//degree
			}
		}
		vel_can_pub.publish(vel_can_data);

    	ros::spinOnce();
	}

// ------------------------------CAN卡关闭---------------------------------------
	if (VCI_CloseDevice(nDeviceType, nDeviceInd)==1)
	{
		cout << "VCI_CloseDevice succeeded" << endl;
	}
	else
	{
		cout<<"VCI_CloseDevice failed"<<endl;
	}
	return 0;
}
