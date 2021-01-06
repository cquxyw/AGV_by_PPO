#include "ros/ros.h"
#include "std_msgs/String.h"
#include "can_listener/vel_can.h"
#include <iomanip>

using namespace std;

void chatterCallback(const can_listener::vel_canConstPtr& msg)
{
    cout << "线速度=" << msg-> v<< "m/s"<< endl;
    cout << "转角=" << msg-> w<< "rad/s"<< endl;
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "can_listener_listener");
    ros::NodeHandle n;
    ros::Subscriber sub = n.subscribe("vel_can", 1000, chatterCallback);
    ros::spin();
    return 0;
}
