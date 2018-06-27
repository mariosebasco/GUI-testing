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

bar=""

for i in {0..100..5}
do
    bar="$bar#"
    echo -ne "$i\r\n"
    #echo ''
    echo -ne "$bar\r"
    
    sleep 0.1
    #echo "$i"
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
