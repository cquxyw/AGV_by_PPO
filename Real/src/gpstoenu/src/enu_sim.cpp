#include <iostream>
#include <ros/ros.h>
#include "gpstoenu/enu.h"

using namespace std;

int main(int argc, char ** argv)
{
    ros::init(argc, argv, "enu_sim");
    ros::NodeHandle n;
    
    ros::Publisher pub = n.advertise<gpstoenu::enu>("enu", 1000);

    gpstoenu::enu data;
    
    while(ros::ok())
    {
        data.x = 1;
        data.y = 1;
        pub.publish(data);
        cout << data.x << data.y << endl;
        // ros::spin();
    }
    return 0;
}
