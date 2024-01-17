#determing the X,Y,Z, coordinates from a monocular webcam to unity using TCP sockets
#testing program. Some things may not work

import cv2
import cvzone
import socket

from cvzone.FaceMeshModule import FaceMeshDetector

host, port = "127.0.0.1", 25001 # server address
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cap = cv2.VideoCapture(1)
detector = FaceMeshDetector(maxFaces=1)


initial = True

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
        #d = 60.96
        #f = (w*d)/W  #493
        #print(f)

        

        #FOV is roughly 65 degrees

        #distance
        f = 493
        d = (W*f)/w #distance
        #print(d)
        

        #near =  px distance between eyes * dist to cam / IPD
        #near = (w*d)/6.5
        #print(near)

        if initial:
            origin_X = (pointLeft[0] + pointRight[0])/2
            origin_Y = (pointLeft[1] + pointRight[1])/2    
            O = origin_X, origin_Y
            initial = False
        #print("X =", origin_X, "Y =", origin_Y)
        
        X_pixel_displacement = (pointLeft[0] + pointRight[0])/2 - origin_X
        Y_pixel_displacement = (pointLeft[1] + pointRight[1])/2 - origin_Y
        #print(X, Y)

        X_displacement = X_pixel_displacement * d / f
        Y_displacement = Y_pixel_displacement * d / f

    data = X_displacement, Y_displacement, d    
    #print(X_displacement, Y_displacement, d)
    try:
        #connect
        sock.connect((host, port))
        sock.sendall(data.encode("utf-8"))
        response = sock.recv(1024).decode("utf-8")
    finally:
        sock.close()


    cv2.imshow("Image", img)
    cv2.waitKey(1)
