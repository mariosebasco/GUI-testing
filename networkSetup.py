#!/usr/bin/env python

import os
import sys
import pysftp as sftp
from pexpect import pxssh
import subprocess

HOST = '192.168.0.104'
USERNAME = 'robot'
PASSWORD = 'Abcd1234'

EVENT_FILE = '/home/robot/Desktop/MLAGui/event_file.txt'
GPS_FILE = '/home/robot/Desktop/MLAGui/gps_raw.txt'

EVENT_DESTINATION = '/home/robot/catkin_ws/src/testing/gps_files/event_file.txt'
GPS_DESTINATION = '/home/robot/catkin_ws/src/testing/gps_files/gps_raw.kml'

def ConnectNetwork():
    #if already connected you don't have to do anything
    cmd = "nmcli -t -f active,ssid dev wifi | egrep '^yes'"
    result = subprocess.check_output(cmd, shell=True)
    if(result[4:-1] == "dd-wrt"):
        print "Already connected to router"
        return True
    
    response = os.system("nmcli c up dd-wrt")
    if response == 0:
        print "Connected to router"
        return True
    else:
        print "Connection failed"
        return False

def CheckConnection():
    response = os.system("ping -c 1 " + HOST)

    #and then check the response...
    if response == 0:
        print HOST, 'Vehicle found!'
        return True
    else:
        print HOST, 'Vehicle not found!'
        return False

def Ssh():
    s = pxssh.pxssh()
    if (s.login(HOST, USERNAME, PASSWORD)):
        print "ssh login successful"

        s.sendline('roslaunch testing test1_path_tracker.launch')
        s.prompt()
        print(s.before)

        s.sendline('rosrun testing state_controller')
        s.prompt()
        print(s.before)
        
        s.logout()

        return True
    return False

def Sftp():
    try:
        s = sftp.Connection(host= HOST, username = USERNAME, password = PASSWORD)

        s.put(EVENT_FILE, EVENT_DESTINATION)
        s.put(GPS_FILE, GPS_DESTINATION)
        s.close()

        print "File transfer complete"
        return True
    
    except Exception, e:
        print e
        return False
        

    
if __name__ == "__main__":
    if ConnectNetwork():
        if CheckConnection():
            Sftp()
            sys.exit(0)
    sys.exit(1)
            
