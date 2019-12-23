import numpy as np
import cv2
import socket
import math
import traceback
from time import sleep
import string

from collections import deque
import argparse
import imutils
import time
#import pandas as pd
#import matplotlib.pyplot as plt

# camera center
SCREEN_CENTER_X = 400
SCREEN_WIDE_X = 800
MAX_W = SCREEN_WIDE_X - SCREEN_CENTER_X
MAX_ANGLE = 60
MAX_ANGLE_RAD = 60. * math.pi / 180.
CAMERA_DIS = 20

# given parameters
# @LENGTH : distance between the machine and objects
# @BOXES  : boxes which represent detected positions
LENGTH = [100, 600, 3000, 200]
BOXES = [[365, 75, 453, 453]]

# define parameters for the control
# @THR_FROTN_LEN : a threshold in the point of front length
# @THR_BOXSIZE : a threshold within a bix box or not
THR_FRONT_LEN = 20
THR_SIDE_LEN = 20
THR_BOXSIZE = 20000

# length[0] : front rigth
# length[1] : front left
# length[2] : side right
# length[3] : side left


def detect_ball():
    greenLower = (50, 120, 80)
    greenUpper = (80, 150, 90)
    #pts = deque(maxlen=args["buffer"])
    camera = cv2.VideoCapture(0)

    #Data_Features = ['x', 'y', 'time']
    #Data_Points = pd.DataFrame(data = None, columns = Data_Features , dtype = float)
    while True:
        #if is_escape_flg(length):
        #    avoid_function(length)
    	# grab the current frame
    	(grabbed, frame) = camera.read()

    	#Reading The Current Time

    	# if we are viewing a video and we did not grab a frame,
    	# then we have reached the end of the video
    	#if args.get("video") and not grabbed:
    	#	break

    	# resize the frame, blur it, and convert it to the HSV
    	# color space
    	frame = imutils.resize(frame, width=100)
    	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    	# construct a mask for the color "green", then perform
    	# a series of dilations and erosions to remove any small
    	# blobs left in the mask
    	mask = cv2.inRange(hsv, greenLower, greenUpper)
    	mask = cv2.erode(mask, None, iterations=2)
    	mask = cv2.dilate(mask, None, iterations=2)
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        cv2.imshow("Frame", frame)
    	# show the frame to our screen
  #  	cv2.imshow("Frame", frame)
    	key = cv2.waitKey(1) & 0xFF

    	# if the 'q' key is pressed, stop the loop
    	if key == ord("q"):
                break

    	# find contours in the mask and initialize the current
    	# (x, y) center of the ball
    	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    		cv2.CHAIN_APPROX_SIMPLE)[-2]
    	center = None
    	# only proceed if at least one contour was found
    	if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                print(center)
                print("radius:" + str(radius))

                if radius >= 200:
                    #the object is close enough
                    text = "s\n"
                    send_msg(text)
                    print("close. stop")
                    continue

                if 700 <= center[0] and center[0] <= 1100:
                    text = "p {}\n".format(5000)
                    send_msg(text)
                    print("forward")
                    continue

                elif center[0] >= 900:
                    #the object is right
                    #ex. 1500
                    text = "r {}\n".format((center[0]-900) * 100)
                    send_msg(text)
                    print("right")
                    continue
                else:
                    #the object is left
                    #ex. 100
                    text = "r {}\n".format((center[0]-900) * 100)
                    send_msg(text)
                    print("left")
                    continue 

                # only proceed if the radius meets a minimum size
                if (radius < 300) & (radius > 10 ) :
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                            (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)

                    #Save The Data Points
        else:
            #not found
            print("not found")
            text = "s"
            send_msg(text)
            continue
    	# update the points queue
    	pts.appendleft(center)

    	# loop over the set of tracked points
        
    	for i in range(1, len(pts)):
                # if either of the tracked points are None, ignore
                # them
                if pts[i - 1] is None or pts[i] is None:
                        continue

                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        




def server_and_call_main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 50002
    s.bind((host, port))
    s.listen(1)

    clients = []

    try:
        s.settimeout(10)
        connection, address = s.accept()
        clients.append((connection, address))
        while(true):
            try:
                connection.settimeout(3)
                from_client = connection.recv(4096).decode()
                distance = from_client.split()
                # call main method
                #main(length = distance)
                detect_ball(length = distance)
                # sleep(0.1)
                #print("sinal=>{}".format(from_client))
                # to_client = "signal[{}]".format(from_client)
                # connection.send(to_client.encode("utf-8"))
            except exception as e:
                # print(e)
                traceback.print_exc()
                continue
    except exception as e:
        # print(clients)
        # print(e)
        traceback.print_exc()
        connection.close()
        s.close()

    return from_client


def send_msg(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 50001
    s.connect((host, port))
    # s.sendall(msg.encode(encoding='ascii'))
    s.send(msg)


def is_escape_flg(length):
    flg = 0
    if length[0] < THR_FRONT_LEN or length[1] < THR_FRONT_LEN:
        flg = 1
    elif length[2] < THR_SIDE_LEN or length[3] < THR_FRONT_LEN:
        flg = 1
    return flg

def avoid_function(roll_sp=100):
    text = "r {}\n".format(roll_sp)
    send_msg(text)
    # print("just rolling")


if __name__ == '__main__':
    #server_and_call_main()
    detect_ball()
