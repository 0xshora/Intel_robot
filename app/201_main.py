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
#used in send_msg
stopflg = 0

face_cascade = cv2.CascadeClassifier('../data/haarcascades/haarcascade_frontalface_default.xml')

def cascade(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    global face_cascade

    boxes = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minSize=(30, 30))
    return boxes

def cal_center_size(rect):
    if len(rect) == 0:
        return 0, 0
    center = (rect[3] - rect[1]) / 2 + rect[1]
    size = (rect[3] - rect[1]) * (rect[4] - rect[2])
    return center, size

def detect_face():
    stopflg = 0
    greenLower = (30, 120, 6)
    greenUpper = (80, 210, 250)
#    greenLower = (50, 120, 50)
#    greenUpper = (80, 210, 90)
    #pts = deque(maxlen=args["buffer"])
    camera = cv2.VideoCapture(1)

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

        mywidth = 100
    	frame = imutils.resize(frame, width = mywidth)


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
    	# cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    	# 	cv2.CHAIN_APPROX_SIMPLE)[-2]
    	center = None
        box = cascade(frame)
        if len(box) != 0:
            center, size = cal_center_size(box)
    	# only proceed if at least one contour was found
    	if center != None:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                # c = max(cnts, key=cv2.contourArea)
                # ((x, y), radius) = cv2.minEnclosingCircle(c)
                # M = cv2.moments(c)
                # center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                print("center:" + center)
                print("size:" + str(size))

                if size >= 1000:
                    #the object is close enough
                    text = "s\n"
                    mysend_msg(text)

                    print("close. stop")
                    continue


                if mywidth/2-mywidth/4 <= center and center <= mywidth/2+mywidth/4:
                    text = "p {}\n".format(5000)
                    mysend_msg(text)
                    print("forward")
                    continue

                elif center >= mywidth/2+mywidth/4:
                    #the object is right
                    #ex. 1500
                    text = "r {}\n".format(5000)

                    mysend_msg(text)
                    print("right")
                    continue

                else:
                    #the object is left
                    #ex. 100
                    text = "r {}\n".format(-5000)

                    mysend_msg(text)
                    print("left")
                    continue 

        else:
            #not found

            print("not found")
            text = "s"

            center = None
            mysend_msg(text)
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
                detect_face(length = distance)
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

msgcnt = [0, 0, 0]
boundary = [2, 1, 50]
previous = 0

def mysend_msg(msg):
    global previous
    global msgcnt
    global boundary
    c = msg[0]
    if c == "p":
        msgcnt[0] += 1
    elif c == "r":
        msgcnt[1] += 1
    elif c == "s":
        msgcnt[2] += 1

    for i in range(3):
        if msgcnt[i] > boundary[i]:
            if c == "s" and previous != 2:
                msgcnt[i] =  0
                previous = 2
                break
            if c == "s" and previous == 2:
                send_msg(msg)
                previous = -1
                break
            if c == "s" and previous == -1:
                break
            send_msg(msg)
            print("********************", msg)
            msgcnt = [0, 0, 0]
            previous = i

from mutagen.mp3 import MP3 as mp3
import pygame
import time
def sound(msg):
    c = msg[0]
    filename = ""
    if c == "p":
        filename = '/home/ri/Intel_robot/data/wav_file/Proceed.mp3'
    if c == "r" and msg[2] != "-":
        filename = '/home/ri/Intel_robot/data/wav_file/Left.mp3'
    if c == "r" and msg[2] == "-":
        filename = '/home/ri/Intel_robot/data/wav_file/Right.mp3'
    if c == "s":
        filename = '/home/ri/Intel_robot/data/wav_file/Stop.mp3'

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    mp3_length = mp3(filename).info.length
    pygame.mixer.music.play(1)
    time.sleep(mp3_length + 0.25)
    pygame.mixer.music.stop()

def show(msg):
    if msg[0] == "s":
        cv2.destroyAllWindows()
        img = cv2.imread("/home/ri/sent/tantei.png")
        cv2.imshow("color",img)
    if msg[0] == "p" or msg[0] == "r":
        img = cv2.imread("/home/ri/sent/smile.png")
        cv2.imshow("color",img)


def send_msg(msg):
    global stopflg
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 50001
    s.connect((host, port))
    # s.sendall(msg.encode(encoding='ascii'))
    if msg[0] == "s":
        if stopflg == 0:
            s.send(msg)
            sound(msg)
            stopflg = 1
    else:
        s.send(msg)
        sound(msg)
        stopflg = 0
    show(msg)


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
    detect_face()
