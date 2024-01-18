#still testing socket features

import cv2
import cvzone
import socket

from cvzone.FaceMeshModule import FaceMeshDetector

host, port = "127.0.0.1", 25001
data = "0,0,0"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cap = cv2.VideoCapture(1)
detector = FaceMeshDetector(maxFaces=1)
initial = True

# Connect to the server and send the data
sock.connect((host, port))

while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=True)
    if faces:
        face = faces[0]
        pointLeft = face[145] #145 is point location for the left eye (shows x and y coordinates)
        pointRight = face[374] #374 for right eye
        cv2.line(img, pointLeft, pointRight, (0,200,0), 3)
        cv2.circle(img, pointLeft, 2, (255,0,255), cv2.FILLED)
        cv2.circle(img, pointRight, 2, (255,0,255), cv2.FILLED)
        w,_ = detector.findDistance(pointLeft, pointRight) #distance (px) between two eye points 
        W = 6.5 #eye distance in cm (near)

        #for focal length
        #known_distance = 60.96
        #f = (w*known_distance)/W  #493
        #print(f)

        #distance
        f = 493     #focal length
        d = (W*f)/w #distance

        #When the camera turns on, the first pos of the face will be set as the initial value
        if initial:
            origin_X = (pointLeft[0] + pointRight[0])/2
            origin_Y = (pointLeft[1] + pointRight[1])/2    
            O = origin_X, origin_Y
            initial = False
        
        X_pixel_displacement = (pointLeft[0] + pointRight[0])/2 - origin_X
        Y_pixel_displacement = (pointLeft[1] + pointRight[1])/2 - origin_Y

        X_displacement = X_pixel_displacement * d / f
        Y_displacement = Y_pixel_displacement * d / f

        #X and Y values converted to string to send over TCP to unity
        data = str(X_displacement) +","+ str(Y_displacement) + "," + str(d)
    
    #sock.sendall(data.encode("utf-8")) #uncomment to send over to unity project. Otherwise, the values are printed
    print(data)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
