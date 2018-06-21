#!/usr/bin/env python

from Tkinter import *
import Image, ImageTk
import urllib
import cStringIO 

import math

CLICKED_CORNERS = []

#----------------------------------------------------------------------------------------------------
#
#                         GRAPHICAL USER INTERFACE USING TKINTER
#
#
#----------------------------------------------------------------------------------------------------
class Interface():
    def __init__(self):
        self.CLICKING_MAP = False
        self.clicked_corners = []
        self.ZOOM = 15
        self.LAT = 42.0
        self.LON = -87.69
        self.HBAR_POS = 0.0
        self.VBAR_POS = 0.0

        self.CreateMap()
        
        self.root = Tk()
        self.frame = Frame(self.root, bd=2, relief=SUNKEN)
        
        self.canvas_frame=Frame(self.frame,width=640,height=640)
        self.canvas_frame.grid(row=0,column=0)
        self.canvas=Canvas(self.canvas_frame,width=640,height=640,scrollregion=(0,0,1920,1920))
        self.hbar=Scrollbar(self.canvas_frame,orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM,fill=X)
        self.hbar.config(command=self.canvas.xview)
        self.vbar=Scrollbar(self.canvas_frame,orient=VERTICAL)
        self.vbar.pack(side=RIGHT,fill=Y)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=640,height=640)
        self.canvas_frame.place(x=10, y=170)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.pack(fill=BOTH,expand=1)
        self.root.geometry("700x1000")
        
        #image_name = "images/map_" + str(self.ZOOM) + ".jpg"
        image_name = "images/stitched_map.jpg"
        self.img = ImageTk.PhotoImage(Image.open(image_name))
        self.image_on_canvas = self.canvas.create_image(0,0,image=self.img,anchor="nw")
        
        self.canvas.bind("<Button 1>",self.GetCoodsCB)

        
    def SetUpWindow(self):
    
        placePointButton = Button(text="Place Point", command=self.PlacePointCB)
        placePointButton.place(x=10, y=50)
        
        undoButton = Button(text="Undo last command", command=self.UndoCB)
        undoButton.place(x=10, y=80)

        recordButton = Button(text="Take recording at last point", command=self.RecordCB)
        recordButton.place(x=10, y=110)
        
        exitButton = Button(text="Exit", command=self.ExitCB)
        exitButton.place(x=10, y=140)

        zoomInButton = Button(text="zoom in", command=self.ZoomInCB)
        zoomInButton.place(x=10, y=840)
        
        zoomOutButton = Button(text="zoom out", command=self.ZoomOutCB)
        zoomOutButton.place(x=90, y=840)
    
        #self.canvas.create_line(0, 400, 900, 400, fill='blue', width=5.0)  # x-axis

        self.root.mainloop()
        
    def PlacePointCB(self):
        print "point button Pressed!"
        self.CLICKING_MAP = True
        my_lat, my_lon = self.GetLatLon()
        print my_lat
        print my_lon
        
    def UndoCB(self):
        print "undo Pressed!"
    
    def RecordCB(self):
        print "record Pressed!"

    def ZoomInCB(self):
        if self.ZOOM < 17:
            print "zooming in!"
            self.LAT, self.LON = self.GetLatLon()
            self.ZOOM = self.ZOOM + 1

            self.CreateMap()
            image_name = "images/stitched_map" + ".jpg"
            self.img = ImageTk.PhotoImage(Image.open(image_name))
            self.image_on_canvas = self.canvas.create_image(0,0,image=self.img,anchor="nw")
            self.canvas.itemconfig(self.image_on_canvas, image = self.img)
        
    def ZoomOutCB(self):
        if self.ZOOM > 10:
            print "Zooming out!"
            self.LAT, self.LON = self.GetLatLon()
            self.ZOOM = self.ZOOM - 1

            self.CreateMap()
            image_name = "images/stitched_map" + ".jpg"
            self.img = ImageTk.PhotoImage(Image.open(image_name))
            self.image_on_canvas = self.canvas.create_image(0,0,image=self.img,anchor="nw")
            self.canvas.itemconfig(self.image_on_canvas, image = self.img)
        
    def ExitCB(self):
        print "Exiting!"
        exit()
    
    def GetCoodsCB(self, event):
        if (self.CLICKING_MAP == True):
            print (event.x,event.y)
            #clicked_lat, clicked_lon = self.GetLatLon()
            print (clicked_lat, clicked_lon)
            self.CLICKING_MAP = False
    
    def GetLatLon(self):
        self.VBAR_POSE = (self.vbar.get()[0] + self.vbar.get()[1]) / 2.0
        self.HBAR_POSE = (self.hbar.get()[0] + self.hbar.get()[1]) / 2.0

        R = 6371000.0
        dist_to_edge = 71*(2**(19 - self.ZOOM))
        del_x = 3.0*dist_to_edge
        del_lat = -(del_x / R)*180.0/math.pi
        temp_lat = self.LAT + 2.0*(self.VBAR_POSE - 0.5)*(del_lat)

        del_y = 3.0*dist_to_edge
        lat_R = R*math.cos(temp_lat*math.pi/ 180.0)
        del_lon = (del_y / lat_R)*180.0/math.pi
        
        temp_lon = self.LON + 2.0*(self.HBAR_POSE - 0.5)*(del_lon)

        return temp_lat, temp_lon


    def FindTileLatLon(self, lat_index, lon_index):
        R = 6371000.0
        dist_to_edge = 71*(2**(19 - self.ZOOM))
        del_x = 2.0*lat_index*dist_to_edge
        del_lat = (del_x / R)*180.0/math.pi
        map_lat = self.LAT + del_lat
        
        del_y = 2.0*lon_index*dist_to_edge
        lat_R = R*math.cos(map_lat*math.pi/ 180.0)
        del_lon = (del_y / lat_R)*180.0/math.pi
        map_lon = self.LON + del_lon

        return map_lat, map_lon

    def StitchMaps(self):
        result = Image.new("RGB", (1920, 1920))
        for lat_index in range(-1, 2):
            for lon_index in range(-1, 2):
                
                img_name = "images/map_" + str(lat_index) + "_" + str(lon_index) + ".jpg"
                temp_img = Image.open(img_name)
                
                left_ver = 640 + lon_index*640
                right_ver = left_ver + 640
                top_hor = 640 - lat_index*640
                bot_hor = top_hor + 640

                result.paste(temp_img, (left_ver, top_hor, right_ver, bot_hor))
        result.save("./images/stitched_map.jpg")
                
    def CreateMap(self):
        print "Loading Map"
        for lat_index in range(-1, 2):
            for lon_index in range(-1, 2):
                map_lat, map_lon = self.FindTileLatLon(lat_index, lon_index)
                img_name = "images/map_" + str(lat_index) + "_" + str(lon_index)
                map_coods = str(map_lat) + "," + str(map_lon)
                get_static_google_map(img_name, center=map_coods, zoom=self.ZOOM, imgsize=(640,640), imgformat="jpg", maptype="hybrid" )
        self.StitchMaps()
        print "Map created!"


#--------------------------------------------------------------------------------------------------
#
#                         OBTAIN STATIC MAP FROM GOOGLE
#
#
#--------------------------------------------------------------------------------------------------
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



        
if __name__ == "__main__":
    
    #SetUpWindow()
    myGUI = Interface()
    myGUI.SetUpWindow()
