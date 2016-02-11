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


def send_msg(msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = '127.0.0.1'
        port = 50001
        s.connect((host, port))
        s.sendall(msg.encode(encoding='ascii'))


def cascade(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # カスケードファイルの読み込み
    face_cascade = cv2.CascadeClassifier(
        '../data/haarcascades/haarcascade_frontalface_default.xml')
    # face_cascade = cv2.CascadeClassifier('../data/haarcascades/haarcascade_upperbody.xml')
    # face_cascade = cv2.CascadeClassifier('../data/haarcascades/haarcascade_lowerbody.xml')

    boxes = face_cascade.detectMultiScale(gray)
    # draw_detections(img, boxes)
    # print(faces)
    # cv2.imshow('img', img)
    return boxes


# MAX_W = SCREEN_WIDE_X - SCREEN_CENTER_X
# MAX_ANGLE = 60
# MAX_ANGLE_RAD = 60. * math.pi / 180.
# CAMERA_DIS = 20

def cal_theta_h(rect_a, rect_b):
    a_center_x = rect_a[3] - rect_a[1]
    b_center_x = rect_b[3] - rect_b[1]

    a = a_center_x - SCREEN_CENTER_X
    b = b_center_x - SCREEN_CENTER_X

    tan_max_angle = math.tan(MAX_ANGLE_RAD)

    h = (MAX_W * CAMERA_DIS) / ((a - b) * tan_max_angle)
    tan_x1 = tan_max_angle * (a / MAX_W)
    tan_x2 = tan_max_angle * (b / MAX_W)

    tan_theta = (tan_x1 + tan_x2) / (1 - tan_x1 * tan_x2)
    theta = math.degrees(math.atan(tan_theta))
    return h, theta


def is_escape_flg(length):
    flg = 0
    if length[0] < THR_FRONT_LEN or length[1] < THR_FRONT_LEN:
        flg = 1
    elif length[2] < THR_SIDE_LEN or length[3] < THR_FRONT_LEN:
        flg = 1
    return flg


def chase_function(d, theta, A=10, B=10, max_rolling=200, max_sp=1000):
    if theta > 5 or theta < -5:
        # rolling
        roll_sp = A * theta
        if theta > 0:
            c = 'l'
        else:
            c = 'r'
        text = "{} {}\n".format(c, min(roll_sp, max_rolling))
        send_msg(text)
    else:
        # move forward
        if d < 20 and d > -20:
            # stop
            send_msg(text)
        else:
            move_sp = B * d
            text = "p {}\n".format(min(move_sp, max_sp))
            send_msg()


def avoid_function(roll_sp=100):
    text = "r {}\n".format(roll_sp)
    send_msg(text)
    # print("just rolling")


def search_function(default_roll=100, default_sp=200):
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
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret, frame = cap.read()

        if mirror is True:
            frame = frame[:, ::-1]

        if size is not None and len(size) == 2:
            frame = cv2.resize(frame, size)

        boxes = cascade(frame)

        escape_flg = is_escape_flg(length)
        box = boxes[0]
        if escape_flg:
            avoid_function(length)
            # print('just rolling')
        elif box:
            h, theta = cal_theta_h(box[0], box[1])
            chase_function(h, theta)
            # print('speed')
        else:
            search_function()
            # print('speed')
            # print('roll')

        k = cv2.waitKey(50)
        if k == 27:  # ESCキーで終了
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(length)


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
