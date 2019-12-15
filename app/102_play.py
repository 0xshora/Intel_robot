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
import pandas as pd
import matplotlib.pyplot as plt

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


def detect_ball(length):
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)
    pts = deque(maxlen=args["buffer"])
    camera = cv2.VideoCapture(0)

    Data_Features = ['x', 'y', 'time']
    Data_Points = pd.DataFrame(data = None, columns = Data_Features , dtype = float)
    while True:
        if is_escape_flg(length):
            avoid_function(length)
    	# grab the current frame
    	(grabbed, frame) = camera.read()

    	#Reading The Current Time

    	# if we are viewing a video and we did not grab a frame,
    	# then we have reached the end of the video
    	if args.get("video") and not grabbed:
    		break

    	# resize the frame, blur it, and convert it to the HSV
    	# color space
    	frame = imutils.resize(frame, width=1800)
    	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    	# construct a mask for the color "green", then perform
    	# a series of dilations and erosions to remove any small
    	# blobs left in the mask
    	mask = cv2.inRange(hsv, greenLower, greenUpper)
    	mask = cv2.erode(mask, None, iterations=2)
    	mask = cv2.dilate(mask, None, iterations=2)

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

                if radius >= 100:
                    #the object is close enough
                    text = "s\n"
                    send_msg(text)
                    continue


                if 800 <= center and center <= 1000:
                    text = "p {}\n".format(1000)
                elif center >= 900:
                    #the object is right
                    #ex. 1500
                    text = "r {}\n".format((center-900) * 100)
                else:
                    #the object is left
                    #ex. 100
                    text = "r {}\n".format((center-900) * 100)
                send_msg(text)
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
            text = "r 1000"
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

    	# show the frame to our screen
    	cv2.imshow("Frame", frame)
    	key = cv2.waitKey(1) & 0xFF

    	# if the 'q' key is pressed, stop the loop
    	if key == ord("q"):
                break

def voice(cmd = None):
    if cmd is None:
        return

    if string.find(cmd, "まがれ") != -1:
        text = "r {}\n".format(5000)
        send_msg(text)
    else if string.find(cmd, "まえにすすめ") != -1:
        text = "p {}\n".format(1000)
        send_msg(text)
    else if string.find(cmd, "うしろにすすめ") != -1:
        text = "p {}\n".format(-1000)
        send_msg(text)
    else if string.find(cmd, "とまれ") != -1:
        text = "s\n"
        send_msg(text)

"""
def go_around(length = 1):
    #the distance to the object is 1 m
    # if possible, the voice might be a part of the command
    # turn right
    move_x = 2
    move_y = 4
    text = "r {}\n".format(5000)
    send_msg(text)
    time.sleep(1)
    text = "s\n"
    send_msg(text)

    #move straight
    text = "p {}\n".format(1000)
    send_msg(text)
    time.sleep(move_x)
    text = "s\n"
    send_msg(text)

    #turn left
    text = "r {}\n".format(-5000)
    send_msg(text)
    time.sleep(1)
    text = "s\n"
    send_msg(text)

    #move straight
    text = "p {}\n".format(1000)
    send_msg(text)
    time.sleep(move_y)
    text = "s\n"
    send_msg(text)

    #turn left
    text = "r {}\n".format(-5000)
    send_msg(text)
    time.sleep(1)
    text = "s\n"
    send_msg(text)

    #move straight
    text = "p {}\n".format(1000)
    send_msg(text)
    time.sleep(move_x)
    text = "s\n"
    send_msg(text)

    #turn right
    text = "r {}\n".format(5000)
    send_msg(text)
    time.sleep(1)
    text = "s\n"
    send_msg(text)

    #move_straight
    text = "p {}\n".format(1000)
    send_msg(text)
    time.sleep(move_y)
    text = "s\n"
    send_msg(text)
"""

def server_and_call_main():
    s = socket.socket(socket.af_inet, socket.sock_stream)
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
    s = socket.socket(socket.af_inet, socket.sock_stream)
    host = '127.0.0.1'
    port = 50001
    s.connect((host, port))
    # s.sendall(msg.encode(encoding='ascii'))
    s.send(msg)


def cascade(img):
    gray = cv2.cvtcolor(img, cv2.color_bgr2gray)

    # load the cascade file

    face_cascade = cv2.cascadeclassifier(
        '../data/haarcascades/haarcascade_frontalface_default.xml')
    # face_cascade = cv2.cascadeclassifier('../data/haarcascades/haarcascade_upperbody.xml')
    # face_cascade = cv2.cascadeclassifier('../data/haarcascades/haarcascade_lowerbody.xml')

    boxes = face_cascade.detectmultiscale(gray)
    # draw_detections(img, boxes)
    # print(faces)
    # cv2.imshow('img', img)
    return boxes


# max_w = screen_wide_x - screen_center_x
# max_angle = 60
# max_angle_rad = 60. * math.pi / 180.
# camera_dis = 20




def is_escape_flg(length):
    flg = 0
    if length[0] < thr_front_len or length[1] < thr_front_len:
        flg = 1
    elif length[2] < thr_side_len or length[3] < thr_front_len:
        flg = 1
    return flg



def avoid_function(roll_sp=100):
    text = "r {}\n".format(roll_sp)
    send_msg(text)
    # print("just rolling")


def search_function(default_roll=5000, default_sp=1000):
    cnt = 0
    if cnt % 100 > 50:
        text = "p {}\n".format(default_sp)
        send_msg(text)
        # print("move forward")
        cnt += 1
    else:
        text = "r {}\n".format(default_roll)
        send_msg(text)
        # print("just rolling")
        cnt += 1

def main(length, mirror=True, size=None):
    cap_0 = cv2.VideoCapture(0)
    cap_1 = cv2.VideoCapture(1)
    while(cap_0.isOpened()):
        print ("hi")
        ret_0, frame_0 = cap_0.read()
        ret_1, frame_1 = cap_1.read()
        if mirror is True:
            frame_0 = frame_0[:, ::-1]
            frame_1 = frame_1[:, ::-1]

        if size is not None and len(size) == 2:
            frame_0 = cv2.resize(frame_0, size)
            frame_1 = cv2.resize(frame_1, size)

        box_0 = []
        box_1 = []
        boxes_0 = cascade(frame_0)
        boxes_1 = cascade(frame_1)
        print("end cascade")
        escape_flg = is_escape_flg(length)
        print(escape_flg)
        print(boxes_0)
        print(boxes_1)
        if len(boxes_0) != 0:
            box_0 = boxes_0[0]
        if len(boxes_1) != 0:
            box_1 = boxes_1[0]

        if escape_flg:
            avoid_function(length)
            # print('just rolling')
        elif len(box_0) != 0 and len(box_1) != 0:
            h, theta = cal_theta_h(box_0, box_1)
            chase_function(h, theta)
            # print('speed')
        else:
            search_function()
            # print('speed')
            # print('roll')

        k = cv2.waitKey(100)
        if k == ord('s'):
            send_msg("s")
            break
        if k == 27:  # ESC end
            break

    cap_0.release()
    cap_1.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    server_and_call_main()


"""
# using transitions
# from transitions import Machine
class StateMachine(object):
    states = ['search', 'chase', 'escape']

    def __init__(self, name):
        self.name = name
        self.machine = Machine(
            model=self, states=StateMachine.states, initial='search', auto_transitions=False)
        self.machine.add_transition(
            trigger='near',     source='search',    dest='escape')
        self.machine.add_transition(
            trigger='near', source='chase', dest='escape')
        self.machine.add_transition(
            trigger='find', source='search', dest='chase')
        self.machine.add_transition(
            trigger='safe', source='escape', dest='search')


intel_robot = StateMachine('test')
"""
