# Reinforcement Learning-based Navigation for Autonoumous Robot

## Table of Contents  
- [Table of contents](#table-of-contents)  
- [Objectives](#objectives)  
- [Setup](#setup)  
- [Quick Start](#quick-start)  
   - [Simulation environment](#simulation-environment)  
   - [Navigation Training](#navigation-training)  
- [Description](#description)  
   - [Robot model](#robot-model)
   - [Object detection by LIDAR](#object-detection-by-LIDAR)  
- [Training Result](#training-result)

## Objectives  
- Create a simulation environment.
- Detect obstacles by LIDAR and acquire ego location by GPS.
- Train the robot to find destination by itself.

## Setup  

## Quick Start
### Simulation Environment  
- start gazebo
```
roslaunch scout based.launch
```
- we provided three world description in [/scout/gazebo/launch/](/scout/gazebo/launch/)  
### Navigation Training
- start training by running [ppo_train.py](/scout/src/based/ppo_train.py)
```
python ppo_train.py
```
- three training strategies correspond to three environment  
   - [based](/scout/src/based/) - fixed goal.  
   - [random goal](/scout/src/random_goal/) - random goal.  
   - [disturb](/scout/src/disturb/) - simulated low-price GPS by add random noise in odom.  

## Description
### Robot model
The robot's name is scout, which is provided by AgileX Robotics.  
![real model](./img/scout_real.png)  
- joints and links are defined by [urdf](/scout/description/urdf/)
- physical appearance  are defined by [meshes](/scout/description/meshes/)
- sensor plugs definition can be found in urdf files  
![virtual_model](./img/scout_vir.png)  

### Object detection by LIDAR  
- use [pcl](./vlp_fir/) to process LIDAR data and detect objects.  
- use rviz to show detection result, launch files are provided in [/scout/description/launch/](./scout/description/launch/)  
![LIDAR](./img/LIDAR.gif)  
   
## Training Result
- based strategy  
![based_test](./img/based_dem.gif)  
- random goal strategy  
- disturb strategy  
