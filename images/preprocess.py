#!/usr/bin/env python

import urllib
import cStringIO
import Image
import math

def get_static_google_map(filename_wo_extension, center=None, zoom=None, imgsize="500x500", imgformat="jpeg",
                          maptype="roadmap", markers=None ):  
    
    request =  "http://maps.google.com/maps/api/staticmap?" # base URL, append query params, separated by &
   
    if center != None:
        request += "center=%s&" % center
    if center != None:
        request += "zoom=%i&" % zoom  # zoom 0 (all of the world scale ) to 22 (single buildings scale)


    request += "size=%ix%i&" % (imgsize)  # tuple of ints, up to 640 by 640
    request += "format=%s&" % imgformat
    request += "maptype=%s&" % maptype  # roadmap, satellite, hybrid, terrain


    if markers != None:
        for marker in markers:
                request += "%s&" % marker

    request += "sensor=false&"   # must be given, deals with getting loction from mobile device 
    #print request
    
    urllib.urlretrieve(request, filename_wo_extension+"."+imgformat) # Option 1: save image directly to disk
    
    web_sock = urllib.urlopen(request)
    imgdata = cStringIO.StringIO(web_sock.read()) # constructs a StringIO holding the image
    try:
        PIL_img = Image.open(imgdata)
    
    # if this cannot be read as image that, it's probably an error from the server,
    except IOError:
        print "IOError:", imgdata.read() # print error (or it may return a image showing the error"
     

#conversion list goes from 
conversion_list = [73957193.820000, 36978596.910000, 18489298.450000]

def FindDistanceToEdge(zoom):
    return 71*(2**(19 - zoom))



if __name__ == "__main__":
    
    for i in range(9):
        img_name = "map_" + str(i)
        print img_name
        get_static_google_map(img_name, center="42.0,-87.69", zoom=10, imgsize=(640,640), imgformat="jpg", maptype="hybrid" )

    print "done!"

    # longitude = -87.69
    # lat = 42.0

    # ZOOM = 16
    # R = 6371000.0
    # del_x = FindDistanceToEdge(ZOOM)
    # del_y = FindDistanceToEdge(ZOOM) 
    # print del_x
    # print del_y
    
    # del_lat = (del_x / R)*180.0/math.pi

    # lat_R = R*math.cos(lat*math.pi/ 180.0)
    # del_long = (del_y / lat_R)*180.0/math.pi
    
    # #print del_long
    # #print del_lat

    # new_long = longitude + del_long
    # new_lat = lat + del_lat
    
    # string1 = "markers=mid:tiny|label:B|color:0xFFFF00|" + str(new_lat) + "," + str(longitude) + "|"
    # string2 = "markers=mid:tiny|label:B|color:0xFFFF00|" + str(lat) + "," + str(new_long) + "|"
    # string3 = "markers=mid:tiny|label:B|color:0xFFFF00|" + str(lat) + "," + str(longitude) + "|"
    
    # print string1
    # print string2
    
    # marker_list = []
    # marker_list2 = []
    
    # marker_list.append(string1)
    # marker_list.append(string2)
    # marker_list.append(string3)

    # marker_list2.append(string2)
    
    # # marker_list.append("markers=mid:tiny|label:B|color:0xFFFF00|42.0,-87.69|")
    # # marker_list.append("markers=mid:tiny|label:B|color:0xFFFF00|42.01,-87.69|")

    # string_center = str(lat) + " " + str(new_long)
    
    # get_static_google_map("img1", center="42.0,-87.69", zoom=ZOOM, imgsize=(640,640), imgformat="jpg", maptype="hybrid")
    #get_static_google_map("img2", center="42.0,-87.69", zoom=9, imgsize=(640,640), imgformat="jpg", maptype="hybrid", markers=marker_list)

    
    #get_static_google_map("img2", center="42.0,-87.69", zoom=5, imgsize=(640,640), imgformat="jpg", maptype="hybrid" )
    
