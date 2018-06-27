#!/bin/bash

# echo "Starting GUI"
# if ! python wolf_UI.py
# then
#     echo "program terminated"
#     exit
# fi

# if ! python networkSetup.py
# then
#     echo "An error occurred"
#     exit
# fi

echo "Ready to start the vehicle"
read -p "Would you like to continue: [y/n] "  response

if [ "$response" = "y" ]
then
    echo "launching ROS files"
    #launch python script here
else
    echo "Shutting down"
    exit
fi

for i in {0..100}
do
    echo -ne "loading --> $i% \r"
    sleep 0.1
done

echo ''

# echo ""
# echo '#####                     (10%)\r\c'
# sleep 1
# echo '#############             (20%)\r\c'
# sleep 1
# echo '#######################   (100%)\r\c'
# echo '\n'


echo "finished"
