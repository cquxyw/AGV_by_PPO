# Reinforcement Learning-based Navigation for Autonoumous Robot

## Table of Contents  
- [Table of contents](#table-of-contents)  
- [Objectives](#objectives)  
- [Setup](#setup)  
- [Simulation of world](#simulation-of-world)  
- [Physical model of scout](#physical-model-of-scout)  
- [Object detection by LIDAR](#object-detection-by-LIDAR)  
- [Navigation based on RL(PPO)](#navigation-based-on-RL(PPO))  

## Description  
- Simulated in Gazebo.
- Robot's name is scout.
- Scout is trained to find destination by itself.

## Setup  

## Simulation of world
[Simulation of world](./scout/gazebo/worlds/)  

## Physical model of scout  
[Physical model of scout](./scout/description/)  
![real model](./img/scout_real.png)  
Real model  
![virtual_model](./img/scout_vir.png)  
Virtual model  

## Object detection by LIDAR  
[Object detection by LIDAR](./vlp_fir/)  
![LIDAR](./img/LIDAR.gif)  

## Navigation based on RL(PPO)  
[Navigation based on RL(PPO)](./scout/src)  
![based_test](./img/based_dem.gif)  
The robot is trained to avoid obstacles and reach the goal area (green area).
