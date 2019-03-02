# Sample Code for Competition @2050
This repository provides sample code for the 2050 competition. It guides you how to use the CityFlow[1]
to simulate the traffic signal control from different perspectives. 

For more description on CityFlow, see [this codebase](https://github.com/zxsRambo/competition).


## Dependencies
This sample code requires the following:
- python 3.*
- more requirements in CityFlow (link needed)

## Installation
In this competition, docker is used by default to set up the environment. A basic dockerFile is provided
in /Docker and you may have to add your specific demand based on it. 

Build docker image using the basic dockerFile
> download [anaconda setup file](https://repo.continuum.io/archive/Anaconda3-5.2.0-Linux-x86_64.sh) and put it into /Docker

> docker built -t docker_image_name .

Please note, the /Docker/sources.list is specifically provided for competitors from China to speed up the installation, and it is not necessary for competitors from other countries. 
More information about docker can be found in [here](https://docs.docker.com/get-started/)

## Data
Some sample data is provided for you to run this code, which is placed in [Dropbox](https://www.dropbox.com/sh/faqz5aslun1ht9d/AAC5f0B7KuGtuejon8Y8Dgrpa?dl=0)

## Usage
### How to run by reading the traffic scenario or the traffic signal plan from the file
To begin with, you can try on running the simplest code by using a default signal plan in the roadnet.
> python run_by_default.py

Then, you can further use a pre-defined signal plan to control the traffic signal.
> python run_by_signal_plan.py

### How to implement a control algorithm
Finally, a more complex control algorithm (SOTL[2]: Self-Organizing Trafc Light Control)is provided for your reference.

> python run_by_control.py

[1] [TheWebConf 2019] CityFlow: A Multi-Agent Reinforcement Learning Environment for Large Scale City Traffic Scenario

[2] Seung-Bae Cools, Carlos Gershenson, and Bart D’Hooghe. 2013. Self-organizing traffic lights: A realistic simulation. In Advances in applied self-organizing systems. Springer, 45–55