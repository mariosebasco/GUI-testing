#!/usr/bin/env python

from Tkinter import *
import Image, ImageTk, ImageDraw
import urllib
import cStringIO 

import math

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
        self.ZOOM = 17
        self.LAT = 42.048501
        self.LON = -87.699061
        self.HBAR_POS = 0.0
        self.VBAR_POS = 0.0
        self.CLICKED_POINTS = []
        self.NUM_POINTS_CLICKED = 0
        
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
        image_name = "images/stitched_map_paths.jpg"
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

    def UpdateCanvasImage(self):
        image_name = "images/stitched_map_paths" + ".jpg"
        self.img = ImageTk.PhotoImage(Image.open(image_name))
        self.image_on_canvas = self.canvas.create_image(0,0,image=self.img,anchor="nw")
        self.canvas.itemconfig(self.image_on_canvas, image = self.img)
        
    def PlacePointCB(self):
        print "point button Pressed!"
        self.CLICKING_MAP = True
        
    def UndoCB(self):
        if (self.NUM_POINTS_CLICKED > 0):
            print "undo Pressed!"
            self.CLICKED_POINTS.pop(self.NUM_POINTS_CLICKED - 1)
            self.NUM_POINTS_CLICKED = self.NUM_POINTS_CLICKED - 1

            self.DrawPaths()
            self.UpdateCanvasImage()
            
    def RecordCB(self):
        print "record Pressed!"

    def ZoomInCB(self):
        if self.ZOOM < 17:
            print "zooming in!"
            self.LAT, self.LON = self.GetLatLon()
            self.ZOOM = self.ZOOM + 1

            self.CreateMap()
            self.UpdateCanvasImage()
            
    def ZoomOutCB(self):
        if self.ZOOM > 10:
            print "Zooming out!"
            self.LAT, self.LON = self.GetLatLon()
            self.ZOOM = self.ZOOM - 1

            self.CreateMap()
            self.UpdateCanvasImage()
            
    def ExitCB(self):
        print "Exiting!"
        exit()
    
    def GetCoodsCB(self, event):
        if (self.CLICKING_MAP == True):
            center_lat, center_lon = self.GetLatLon()
            #print(event.x, event.y)
            
            del_x = (640 / 2) - event.y #in pixels
            del_y = event.x - (640 / 2) #in pixels

            dist_to_edge = 71.0*(2.0**(19 - self.ZOOM))
            del_x = dist_to_edge*del_x/320.0 #in meters
            del_y = dist_to_edge*del_y/320.0 #in meters

            R = 6371000.0
            del_lat = (del_x / R)*180.0/math.pi
            clicked_lat = center_lat + del_lat
            
            lat_R = R*math.cos(clicked_lat*math.pi/ 180.0)
            del_lon = (del_y / lat_R)*180.0/math.pi
            clicked_lon = center_lon + del_lon

            print "clicked latitude: " + str(clicked_lat)
            print "clicked longitude: " + str(clicked_lon)

            self.NUM_POINTS_CLICKED = self.NUM_POINTS_CLICKED + 1
            self.CLICKED_POINTS.append((clicked_lat, clicked_lon))
            
            self.DrawPaths()
            self.UpdateCanvasImage()
            
            self.CLICKING_MAP = False

    def DrawPaths(self):
        img = Image.open("./images/stitched_map.jpg")
        result = Image.new("RGB", (1920, 1920))
        result.paste(img, (0, 0, 1920, 1920))
        result.save("./images/stitched_map_paths.jpg")
        
        print "redrawing paths"
        
        if (self.NUM_POINTS_CLICKED != 0):
            for i in range(self.NUM_POINTS_CLICKED):
                if(i == 0):
                    self.DrawPoint(self.CLICKED_POINTS[i])
                else:
                    self.DrawPoint(self.CLICKED_POINTS[i])
                    self.DrawLine(self.CLICKED_POINTS[i - 1], self.CLICKED_POINTS[i])

    def DrawPoint(self, point):
        img = Image.open("./images/stitched_map_paths.jpg")
        
        R = 6371000.0
        dist_to_edge = 3.0*71.0*(2.0**(19 - self.ZOOM))
        del_lat = point[0] - self.LAT
        del_lon = point[1] - self.LON

        del_x = (del_lat*math.pi/180.0)*R

        lat_R = R*math.cos(point[0]*math.pi/ 180.0)
        del_y = (del_lon*math.pi/180.0)*lat_R

        pixel_y = int(960.0 - (del_x/dist_to_edge)*960.0)
        pixel_x = int(960.0 + (del_y/dist_to_edge)*960.0)

        draw = ImageDraw.Draw(img)
        point1 = (pixel_x+5, pixel_y+5)
        point2 = (pixel_x-5, pixel_y+5)
        point3 = (pixel_x-5, pixel_y-5)
        point4 = (pixel_x+5, pixel_y-5)

        draw.polygon((point1[0], point1[1], point2[0], point2[1], point3[0], point3[1], point4[0], point4[1]), fill=128)

        img.save("./images/stitched_map_paths.jpg")

    def DrawLine(self, point1, point2):
        img = Image.open("./images/stitched_map_paths.jpg")
        draw = ImageDraw.Draw(img)

        R = 6371000.0
        dist_to_edge = 3.0*71.0*(2.0**(19 - self.ZOOM))
        
        del_lat1 = point1[0] - self.LAT
        del_lon1 = point1[1] - self.LON

        del_x1 = (del_lat1*math.pi/180.0)*R

        lat_R1 = R*math.cos(point1[0]*math.pi/ 180.0)
        del_y1 = (del_lon1*math.pi/180.0)*lat_R1

        pixel_y1 = int(960.0 - (del_x1/dist_to_edge)*960.0)
        pixel_x1 = int(960.0 + (del_y1/dist_to_edge)*960.0)

        del_lat2 = point2[0] - self.LAT
        del_lon2 = point2[1] - self.LON

        del_x2 = (del_lat2*math.pi/180.0)*R

        lat_R2 = R*math.cos(point2[0]*math.pi/ 180.0)
        del_y2 = (del_lon2*math.pi/180.0)*lat_R2

        pixel_y2 = int(960.0 - (del_x2/dist_to_edge)*960.0)
        pixel_x2 = int(960.0 + (del_y2/dist_to_edge)*960.0)
        
        draw.line((pixel_x1, pixel_y1, pixel_x2, pixel_y2), fill=128, width=5)
        img.save("./images/stitched_map_paths.jpg")

        
    
    def GetLatLon(self):
        self.VBAR_POSE = (self.vbar.get()[0] + self.vbar.get()[1]) / 2.0
        self.HBAR_POSE = (self.hbar.get()[0] + self.hbar.get()[1]) / 2.0

        R = 6371000.0
        dist_to_edge = 71.0*(2.0**(19 - self.ZOOM))
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
        dist_to_edge = 71.0*(2.0**(19 - self.ZOOM))
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
        self.DrawPaths()
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
