import numpy as np
import cv2

# camera center
SCREEN_CENTER_X = 400

# given parameters
# @LENGTH : distance between the machine and objects
# @BOXES  : boxes which represent detected positions
LENGTH = [100, 600, 3000, 200]
BOXES = [[365, 75, 453, 453]]

# define parameters for the control
# @THR_FROTN_LEN : a threshold in the point of front length
# @THR_BOXSIZE : a threshold within a bix box or not
THR_FRONT_LEN = 100
THR_SIDE_LEN = 100
THR_BOXSIZE = 20000

# length[0] : front rigth
# length[1] : front left
# length[2] : side right
# length[3] : side left


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


def is_escape_flg(length):
    flg = 0
    if length[0] < THR_FRONT_LEN or length[1] < THR_FRONT_LEN:
        flg = 1
    elif length[2] < THR_SIDE_LEN or length[3] < THR_FRONT_LEN:
        flg = 1
    return flg


def chase_function(d, theta, A=10, B=10, max_rolling=200, max_sp=100):
    if theta > 5 or theta < -5:
        # rolling
        roll_sp = A * theta
        # send(r, min(roll_sp, max_rolling))
    else:
        # move forward
        if d < 20 and d > -20:
            # stop
            print("stop!")
        else:
            move_sp = B * d
            # send(p, min(move_sp, max_sp))


def avoid_function(d, length, roll_sp=100):
    # send(r, roll_sp)
    print("just rolling")


def search_function():
    cnt = 0
    if cnt % 100 < 60:
        print("move forward")
    else:
        # send(p, default_sp)
        print("just rolling")


def main(length, mirror=True, size=None):
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret, frame = cap.read()

        if mirror is True:
            frame = frame[:, ::-1]

        if size is not None and len(size) == 2:
            frame = cv2.resize(frame, size)

        boxes = cascade(frame)

        flg = is_escape_flg(length)
        box = boxes[0]
        if flg:
            avoid_function(length)
            # print('just rolling')
        elif box:
            search_function(length)
            # print('speed')
            # print('roll')
        else:
            chase_function(length)
            # print('speed')

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
