#include "ros/ros.h"

#include "can_listener/vel_can.h"
#include "gpstoenu/enu.h"
#include "vlp_fir/obs_info.h"
#include "PPO/RL_input_msgs.h"

#include <sstream>
#include <iostream>

using namespace std;

PPO::RL_input_msgs pub_msg;

void callback1(const gpstoenu::enu::ConstPtr& msg)
{
    pub_msg.x = msg->x;
    pub_msg.y = msg->y;
}

void callback2(const can_listener::vel_can::ConstPtr& msg)
{    
    pub_msg.v = msg->v;
    pub_msg.w = msg->w;
}

// void callback3(const vlp_fir::obs_info& msg)
// {
    
// }


int main(int argc, char **argv)
{
    ros::init(argc, argv, "RL_input");
    ros::NodeHandle n;
    ros::Subscriber sub1 = n.subscribe("enu", 1000, callback1);
    ros::Subscriber sub2 = n.subscribe("vel_can", 1000, callback2);
    // ros::Subscriber sub3 = n.subscribe("obj_", 1000, callback3);

    ros::Publisher pub = n.advertise<PPO::RL_input_msgs>("RLin",1000);

    while(ros::ok())
    {
        ros::AsyncSpinner spinner(3);
        spinner.start();
        pub.publish(pub_msg);
        cout << "State Publish"<< endl;
        spinner.stop();
    }
    return 0;
}
