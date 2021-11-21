# import all libraries here
import cv2
import numpy as np
import serial
# using web cams and video
#url = "http://192.168.1.25:8080/video"
video = "media/4.mp4"
port = "COM2"
baud_rate = 9600
#video = "media/1.MTS"
#cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(url)
# declare variable for data structure
s = serial.Serial(port,baud_rate)
cap = cv2.VideoCapture(video)

line_1_pos = 550
line_2_pos = 300
off_set = 6
min_width_rec = 80 #minimum width of rectangel
min_height_rec = 80 #minimum width of rectangel


#making function
def Circle_in_rec(x,y,w,h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx1 = x+x1
    cy1 = y+y1
    return cx1,cy1

detect = []
counter = 0
# NOW ALGO USE HERE
background_subtract_algo = cv2.bgsegm.createBackgroundSubtractorMOG()






#carPath = "C:\\Users\\DKIN\\Desktop\\chinky\\car_detect\\Cat-Detection-Opencv-master\\cat.xml"
#carPath = "C:\\Users\\DKIN\\recog\\freeky\\Lib\\site-packages\\cv2\\data\\cars.xml"
#trained = cv2.CascadeClassifier(carPath)
while True:
    ret,frame = cap.read()
    grey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(5,5),5)
    #apply  algo
    
    img_sub =  background_subtract_algo.apply(blur)
    dilate = cv2.dilate(img_sub,np.ones((5,5)))
    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatedata = cv2.morphologyEx(dilate,cv2.MORPH_CLOSE,kernal)
    dilatedata = cv2.morphologyEx(dilatedata,cv2.MORPH_CLOSE,kernal)
    contours , h = cv2.findContours(dilatedata,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #draw line here
    line_1 = cv2.line(frame,(0,line_1_pos),(1350,line_1_pos),(127,125,255),3)
    #line_2 = cv2.line(frame,(0,line_2_pos),(1350,line_2_pos),(100,200,0),3)
    
    #cars = trained.detectMultiScale(grey,1.3,3)
    
    #for(x,y,w,h) in cars:
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        #cv2.rectangle(frame,(x,y-40),(x+w,y),(255,0,0),-1)
        #cv2.putText(frame,"car",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255))
    #if frame is not None:
    for (i,c) in enumerate(contours):
        (x,y,w,h) = cv2.boundingRect(c)
        val_counter = (w>= min_width_rec) and (h>= min_height_rec)
        if not val_counter:
            continue
        
        
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),3)
        cv2.rectangle(frame,(x,y-40),(x+w,y),(255,0,0),3)
        cv2.putText(frame,"Vehical detect",(x,y-10),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.8,(125,255,255))
        circle_detect = Circle_in_rec(x,y,w,h)
        detect.append(circle_detect)
        cv2.circle(frame,circle_detect,4,(255,0,0),-1)
        for (x,y) in detect:
            if y<(line_1_pos+off_set) and y>(line_1_pos-off_set):
                counter+=1
                
            cv2.line(frame,(0,line_1_pos),(1350,line_1_pos),(0,125,255),3)
            detect.remove((x,y))
           
        
      
        cv2.putText(frame,"Vehical counts: "+str(counter),(450,70),cv2.FONT_HERSHEY_SIMPLEX,1,(100,100,255))
        
        if counter<20:
            print("Trafic control system activate.......\n Low traffic detect")
            s.write(b"0")
        elif counter>=20 and counter<=50:
            print("Moderate traffic")
            s.write(b"1")
        elif counter>50:
            print("heavy traffic")
            s.write(b"2")
        else:
            print("Not detect something")
    
    
    
    
    
    
    cv2.imshow("frame",frame)
        
    q=cv2.waitKey(1)
    if q==ord("q"):
        break
        
cv2.destroyAllWindows()
