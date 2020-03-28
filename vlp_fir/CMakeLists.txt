cmake_minimum_required(VERSION 2.8.3)
project(vlp_fir)

find_package(catkin REQUIRED COMPONENTS
        roscpp
        std_msgs
        pcl_conversions
        pcl_msgs
        pcl_ros
        sensor_msgs
        geometry_msgs
        message_generation  #需要此功能包生成msg文件需要的代码
        )
add_message_files(
 FILES
 send_msgs.msg
)
generate_messages(
DEPENDENCIES
std_msgs
)
FIND_PACKAGE( PCL REQUIRED COMPONENTS common io visualization )

SET(${vlp_fir_SOURCE_DIR})

catkin_package(
 CATKIN_DEPENDS roscpp  std_msgs)

include_directories(include ${PCL_INCLUDE_DIRS}  ${catkin_INCLUDE_DIRS} ${vlp_fir_SOURCE_DIR}/include .include)
link_directories(${PCL_LIBRARY_DIRS}  ${catkin_LIBRARIES} ${vlp_fir_SOURCE_DIR})# 设置动态库链接目录
add_definitions(${PCL_DEFINITIONS})
add_executable(do_it src/main_deal.cpp src/processCloud.cpp src/Marker.cpp src/serial_port.cpp)

target_link_libraries(do_it ${catkin_LIBRARIES} ${PCL_LIBRARIES} ${PCL_COMMON_LIBRARIES} ${PCL_IO_LIBRARIES})
SET( CMAKE_CXX_FLAGS "-std=c++11 -O3")