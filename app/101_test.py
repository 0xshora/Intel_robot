import numpy as np
import cv2
import socket
import math

# camera center
SCREEN_CENTER_X = 400
SCREEN_WIDE_X = 800
MAX_W = SCREEN_WIDE_X - SCREEN_CENTER_X
MAX_ANGLE = 60
MAX_ANGLE_RAD = 60 * math.pi /180.
CAMERA_DIS = 20

# given parameters
# @LENGTH: distance between the machine and objects
# @BOXES : boxes which represent detected positions
LENGTH = [100, 600, 3000, 200]
BOXES = [[365, 75, 453, 453 ]]

#define paramters for the control
# @THR_FRONT_LEN: a threshold in the point of front length
# @THR_BOXSIZE: a threshold within a bix box or not
THR_FRONT_LEN = 20
THR_SIDE_LEN = 20
THR_BOXSIZE = 20000

# length[0] : front right
# length[1] : front left
# length[2] : side right
# length[3] : side left

def send_msg(msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = '127.0.0.1'
        port = 50001
        s.connect((host, port))
        s.sendall(msg.encode(encoding='ascii'))

def cascade(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cascade file
    face_cascade = cv2.Cascadeclassifier('../data/haarcascades/haarcascade_frontalface_default.xml' )

    boxes = face_cascade.detectMultiScale(gray)

    return boxes

def cal_theta_h(rect_a=None, rect_b):
    if rect_a == None:
        h = 500
        theta = -60
        return h
