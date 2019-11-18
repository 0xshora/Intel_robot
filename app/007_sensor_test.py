import numpy as np
import cv2
import socket
import math

# camera center
SCREEN_CENTER_X = 400
SCREEN_WIDE_X = 800
MAX_W = SCREEN_WIDE_X - SCREEN_CENTER_X
MAX_ANGLE = 60
MAX_ANGLE_RAD = 60. * math.pi / 180.
CAMERA_DIS = 20

THR_FRONT_LEN = 20
THR_SIDE_LEN = 20
THR_BOXSIZE = 20000


def send_msg(msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = '127.0.0.1'
        port = 50001
        s.connect((host, port))
        s.sendall(msg.encode(encoding='ascii'))


def is_escape_flg(length):
    flg = 0
    if length[0] < THR_FRONT_LEN or length[1] < THR_FRONT_LEN:
        flg = 1
    elif length[2] < THR_SIDE_LEN or length[3] < THR_FRONT_LEN:
        flg = 1
    return flg


def avoid_function(roll_sp=1000):
    text = "r {}\n".format(roll_sp)
    send_msg(text)
    # print("just rolling")


def search_function(default_roll=1000, default_sp=2000):
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
    while(1):
        escape_flg = is_escape_flg(length)
        if escape_flg:
            # avoid_function(length)
            avoid_function()
        else:
            search_function()


if __name__ == '__main__':
    main(length)
