#!/bin/bash

#export the ROS master URI to be in the vehicle
export ROS_MASTER_URI=http://192.168.0.104:11311

#start the GUI
echo "Starting GUI"
if ! python wolfUI.py
then
    echo "program terminated"
    exit
fi

#connect to the vehicle and sftp the path files
if ! python networkSetup.py
then
    echo "An error occurred"
    exit
fi



# echo "Ready to start the vehicle"
# read -p "Would you like to continue: [y/n] "  response

# if [ "$response" = "y" ]
# then
#     echo "launching ROS files"
#     #launch python script here
# else
#     echo "Shutting down"
#     exit
# fi

# for i in {0..100}
# do
#     echo -ne "loading --> $i% \r"
#     sleep 0.1
# done

echo ''
echo "finished"
