#!/usr/bin/env python

from Tkinter import *
import Image, ImageTk, ImageDraw
import urllib
import cStringIO 

import math

#---------------------------------------------------------------------------------------------------
#
#                         GRAPHICAL USER INTERFACE USING TKINTER
#
#
#---------------------------------------------------------------------------------------------------
class Interface():
    def __init__(self):
        self.CLICKING_MAP = False
        self.clicked_corners = []
        self.ZOOM = 20
        self.LAT = 42.0486127
        self.LON = -87.697733
        self.HBAR_POS = 0.0
        self.VBAR_POS = 0.0
        self.CLICKED_POINTS = []
        self.NUM_POINTS_CLICKED = 0
        self.PATH = []
        self.EVENT_POINT = False
        self.EVENTS = []
        self.NUM_EVENTS = 0
        self.COLOR = (128, 0, 0) #red
        self.FREE_POINT_MODE = False
        self.REDRAWING_MAP = False
        
        self.CreateMap()

        self.root = Tk()
        self.root.title("WOLF UI")
        self.frame = Frame(self.root, bd=2, relief=SUNKEN)

        self.TEXTBOX = Text(self.root, height=5, width=30)
        self.TEXTBOX.place(x=450, y=50)
        self.TEXTBOX.insert(END, "WOLF UI\nBegin making Path\n#\n#\n#\n")
        
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
        self.canvas_frame.place(x=10, y=190)
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

        recordButton = Button(text="Place Event Point", command=self.RecordCB)
        recordButton.place(x=10, y=80)
        
        undoButton = Button(text="Undo", command=self.UndoCB)
        undoButton.place(x=10, y=130)
        
        exitButton = Button(text="Exit", command=self.ExitCB)
        exitButton.place(x=10, y=160)

        zoomInButton = Button(text="zoom in", command=self.ZoomInCB)
        zoomInButton.place(x=10, y=850)
        
        zoomOutButton = Button(text="zoom out", command=self.ZoomOutCB)
        zoomOutButton.place(x=90, y=850)

        finishButton = Button(text="Finish Path", command=self.FinishCB)
        finishButton.place(x=570, y=850)

        executeButton = Button(text="execute trajectory", command=self.ExecuteCB)
        executeButton.place(x=535, y=880)

        freePointButton = Button(text="Free/Fixed Points", command=self.FreePointModeCB)
        freePointButton.place(x=535, y=160)
        
        self.root.mainloop()

    def UpdateCanvasImage(self):
        image_name = "images/stitched_map_paths" + ".jpg"
        self.img = ImageTk.PhotoImage(Image.open(image_name))
        self.image_on_canvas = self.canvas.create_image(0,0,image=self.img,anchor="nw")
        self.canvas.itemconfig(self.image_on_canvas, image = self.img)

    def WriteToWindow(self, inputString):
        self.TEXTBOX.insert(END, inputString)
        self.TEXTBOX.delete('1.0','2.0')
        
        
    def PlacePointCB(self):
        self.WriteToWindow("point button Pressed!\n")
        print "point button Pressed!"
        self.CLICKING_MAP = True
        
    def UndoCB(self):
        if (self.NUM_POINTS_CLICKED > 0):
            self.WriteToWindow("Undo pressed!\n")
            print "undo Pressed!"
            if self.CLICKED_POINTS[self.NUM_POINTS_CLICKED - 1][3]:
                self.EVENTS.pop(self.NUM_EVENTS - 1)
                self.NUM_EVENTS = self.NUM_EVENTS - 1
            self.CLICKED_POINTS.pop(self.NUM_POINTS_CLICKED - 1)
            if(len(self.PATH) > 0):
                self.PATH.pop(len(self.PATH) - 1)
            self.NUM_POINTS_CLICKED = self.NUM_POINTS_CLICKED - 1

            self.DrawPaths()
            self.UpdateCanvasImage()
            
    def RecordCB(self):
        self.WriteToWindow("Press location to record!\n")
        print "Press location to record!"
        self.CLICKING_MAP = True
        self.EVENT_POINT = True

    def ZoomInCB(self):
        if self.ZOOM < 20:
            self.WriteToWindow("Zooming in!\n")
            print "zooming in!"
            self.LAT, self.LON = self.GetLatLon()
            self.ZOOM = self.ZOOM + 1

            self.CreateMap()
            self.UpdateCanvasImage()
            
    def ZoomOutCB(self):
        if self.ZOOM > 10:
            self.WriteToWindow("Zooming out!\n")
            print "Zooming out!"
            self.LAT, self.LON = self.GetLatLon()
            self.ZOOM = self.ZOOM - 1

            self.CreateMap()
            self.UpdateCanvasImage()
            
    def ExitCB(self):
        self.WriteToWindow("Exiting!\n")
        print "Exiting!"
        exit()

    def FinishCB(self):
        if(self.NUM_POINTS_CLICKED > 0):
            self.TEXTBOX.insert(END, "Exporting text files!\n")
            self.TEXTBOX.delete('1.0','2.0')
            print "Exporting text files!"
            event_file = open("event_file.txt", "w")
            path_file = open("gps_raw.txt", "w")

            counter = 1
            for event in self.EVENTS:
                event_file.write("event: " + str(counter) + "\n")
                event_file.write("marker id: " + str(event[2]) + "\n")
                event_file.write("latitude: " + str(event[0]) + "\n")
                event_file.write("longitude: " + str(event[1]) + "\n")
                counter = counter + 1

            for path in self.PATH:
                for point in path:
                    path_file.write(str(point[0]) + "\n")
                    path_file.write(str(point[1]) + "\n")
            path_file.write(str(self.CLICKED_POINTS[self.NUM_POINTS_CLICKED - 1][0]) + "\n")
            path_file.write(str(self.CLICKED_POINTS[self.NUM_POINTS_CLICKED - 1][1]) + "\n")
                
            event_file.close()
            path_file.close()

    def FreePointModeCB(self):
        self.FREE_POINT_MODE = not self.FREE_POINT_MODE
        if self.FREE_POINT_MODE:
            print "Free point mode ON"
            self.WriteToWindow("Free mode ON!\n")
        else:
            print "Free point mode OFF"
            self.WriteToWindow("Free mode OFF!\n")

    def ExecuteCB(self):
        print "executing trajectory"
        self.WriteToWindow("Executing trajectory!\n")
    
    def GetCoodsCB(self, event):
        if (self.CLICKING_MAP == True):
            center_lat, center_lon = self.GetLatLon()
            
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

            self.WriteToWindow("clicked latitude " + str(round(clicked_lat, 4)) + "\n")
            self.WriteToWindow("clicked longitude " + str(round (clicked_lon, 4)) + "\n")

            if(not self.FREE_POINT_MODE):
                #convert to lat and lon on map file
                file = open("map.txt" , "r")
                min_dist = 1000
                for line in file:
                    if 'marker' in line:
                        lat_index = line.find('lat')
                        lon_index = line.find('lon')
                        id_index = line.find('id')
                        end_index = line.find('/>')
                        
                        curr_lat = float(line[(lat_index + 5): (lon_index - 2)])
                        curr_lon = float(line[(lon_index + 5): (id_index - 2)])
                        
                        curr_lat_rad = curr_lat*math.pi/180.0
                        clicked_lat_rad = clicked_lat*math.pi/180.0
                        del_lat = (curr_lat - clicked_lat)*math.pi/180.0
                        del_lon = (curr_lon - clicked_lon)*math.pi/180.0
                        
                        a = (math.sin(del_lat/2.0))**2 + math.cos(curr_lat_rad)*math.cos(clicked_lat_rad)*(math.sin(del_lon/2.0)**2)
                        c = 2.0*math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
                        d = R*c
                        if d < min_dist:
                            min_dist = d
                            actual_lat = curr_lat
                            actual_lon = curr_lon
                            marker_id = int(line[(id_index + 4):(end_index - 1)])
                file.close()
            else:
                actual_lat = clicked_lat
                actual_lon = clicked_lon
                marker_id = self.NUM_POINTS_CLICKED
                                    

            point = (actual_lat, actual_lon, marker_id, self.EVENT_POINT)
            self.AppendPoint(point)
            self.UpdateCanvasImage()

            self.EVENT_POINT = False
            self.CLICKING_MAP = False


    def AppendPoint(self, point):
        self.REDRAWING_MAP = False

        if(point[3]): self.COLOR = (0,128,0)
        else: self.COLOR = (128,0,0)
            
        if(self.NUM_POINTS_CLICKED == 0):
            self.DrawPoint(point)
        else:
            point1 = self.CLICKED_POINTS[self.NUM_POINTS_CLICKED - 1]
            if (not self.DrawLine(point1, point)):
                return
            self.DrawPoint(point)

        self.NUM_POINTS_CLICKED = self.NUM_POINTS_CLICKED + 1
        self.CLICKED_POINTS.append(point)
        if point[3]:
            self.EVENTS.append((point[0], point[1], point[2]))
            self.NUM_EVENTS = self.NUM_EVENTS + 1


    def DrawPaths(self):        
        img = Image.open("./images/stitched_map.jpg")
        result = Image.new("RGB", (1920, 1920))
        result.paste(img, (0, 0, 1920, 1920))
        result.save("./images/stitched_map_paths.jpg")

        self.REDRAWING_MAP = True
        print "redrawing paths"

        if (self.NUM_POINTS_CLICKED != 0):
            for i in range(self.NUM_POINTS_CLICKED):
                
                if self.CLICKED_POINTS[i][3]: self.COLOR = (0,128,0)
                else: self.COLOR = (128,0,0)
                
                if(i == 0):
                    self.DrawPoint(self.CLICKED_POINTS[i])
                else:
                    if(not self.DrawLine(self.CLICKED_POINTS[i - 1], self.CLICKED_POINTS[i])):
                        return
                    self.DrawPoint(self.CLICKED_POINTS[i])

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

        draw.polygon((point1[0], point1[1], point2[0], point2[1], point3[0], point3[1], point4[0], point4[1]), fill=self.COLOR)

        img.save("./images/stitched_map_paths.jpg")

    def DrawLine(self, point1, point2):
        R = 6371000.0
        dist_to_edge = 3.0*71.0*(2.0**(19 - self.ZOOM))

        lat1 = point1[0]
        lon1 = point1[1]
        lat2 = point2[0]
        lon2 = point2[1]
        path = []
        pixels = []

        del_lat1 = lat1 - self.LAT
        del_lon1 = lon1 - self.LON
            
        del_x1 = (del_lat1*math.pi/180.0)*R
        
        lat_R1 = R*math.cos(lat1*math.pi/ 180.0)
        del_y1 = (del_lon1*math.pi/180.0)*lat_R1
            
        init_pix_y = int(960.0 - (del_x1/dist_to_edge)*960.0)
        init_pix_x = int(960.0 + (del_y1/dist_to_edge)*960.0)

        del_lat2 = lat2 - self.LAT
        del_lon2 = lon2 - self.LON
        
        del_x2 = (del_lat2*math.pi/180.0)*R
        
        lat_R2 = R*math.cos(lat2*math.pi/ 180.0)
        del_y2 = (del_lon2*math.pi/180.0)*lat_R2
        
        end_pix_y = int(960.0 - (del_x2/dist_to_edge)*960.0)
        end_pix_x = int(960.0 + (del_y2/dist_to_edge)*960.0)
        
        img = Image.open("./images/stitched_map_paths.jpg")
        draw = ImageDraw.Draw(img)

        if(not self.FREE_POINT_MODE):
            file = open("map.txt", "r")
            line = file.readline()
            found_path = False
        
            while True:
                if '<path' in line:
                    id1_index = line.find('id1')
                    id2_index = line.find('id2')
                    end_index = line.find('>')
                    id1 = int(line[id1_index + 5: id2_index - 2])
                    id2 = int(line[id2_index + 5: end_index - 1])
                    if ((id1==point1[2] and id2==point2[2]) or (id1==point2[2] and id2==point1[2])):
                        found_path = True
                        break
                line = file.readline()
                if not line: break
                
            if (found_path == False):
                print "no path found between these two markers"
                self.TEXTBOX.insert(END, "no path found\n")
                self.TEXTBOX.delete('1.0','2.0')
                
                file.close()
                return False

            line = file.readline()
            
            while('</path>' not in line):
                comma_index = line.find(',')
                if(comma_index == -1):
                    line = file.readline()
                    continue
                lat1 = float(line[2:comma_index])
                lon1 = float(line[comma_index + 1:])

                path.append((lat1, lon1))
                        
                del_lat1 = lat1 - self.LAT
                del_lon1 = lon1 - self.LON
                        
                del_x1 = (del_lat1*math.pi/180.0)*R
                
                lat_R1 = R*math.cos(point1[0]*math.pi/ 180.0)
                del_y1 = (del_lon1*math.pi/180.0)*lat_R1
                
                pixel_y1 = int(960.0 - (del_x1/dist_to_edge)*960.0)
                pixel_x1 = int(960.0 + (del_y1/dist_to_edge)*960.0)
                
                pixels.append((pixel_x1, pixel_y1))

                line = file.readline()

            file.close()

            if (id1 == point2[2]):
                path = list(reversed(path))
                pixels = list(reversed(pixels))
        path.insert(0, (point1[0], point1[1]))
        pixels.insert(0, (init_pix_x, init_pix_y))
        pixels.append((end_pix_x, end_pix_y))

        for i in range(len(pixels) - 1):
            draw.line((pixels[i][0], pixels[i][1], pixels[i+1][0], pixels[i+1][1]), fill=128, width=5)

        if (not self.REDRAWING_MAP): self.PATH.append(path)
        img.save("./images/stitched_map_paths.jpg")
        return True

        
    
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
        #self.WriteToWindow("Loading Map\n")
        
        for lat_index in range(-1, 2):
            for lon_index in range(-1, 2):
                map_lat, map_lon = self.FindTileLatLon(lat_index, lon_index)
                img_name = "images/map_" + str(lat_index) + "_" + str(lon_index)
                map_coods = str(map_lat) + "," + str(map_lon)
                get_static_google_map(img_name, center=map_coods, zoom=self.ZOOM, imgsize=(640,640), imgformat="jpg", maptype="hybrid" )
        self.StitchMaps()
        self.DrawPaths()
        print "Map created!"
        #self.TEXTBOX.insert(END, "Map created!\n")
        #self.TEXTBOX.delete('1.0','2.0')        


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



#--------------------------------------------------------------------------------------------------
#
#                                               MAIN
#
#
#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    
    #SetUpWindow()
    myGUI = Interface()
    myGUI.SetUpWindow()
