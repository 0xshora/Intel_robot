import subprocess
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


def cal_theta_h(rect_a=None, rect_b=None):
    if rect_a == None:
        h = 500
        theta = -60
        return h, theta
    elif rect_b == None:
        h = 500
        theta = 60
        return h, theta
    a_center_x = (rect_a[3] - rect_a[1]) / 2 + rect_a[1]
    b_center_x = (rect_b[3] - rect_b[1]) / 2 + rect_a[1]

    a = a_center_x - SCREEN_CENTER_X
    b = b_center_x - SCREEN_CENTER_X

    tan_max_angle = math.tan(MAX_ANGLE_RAD)

    h = (MAX_W * CAMERA_DIS) / ((a - b) * tan_max_angle)
    tan_x1 = tan_max_angle * (a / MAX_W)
    tan_x2 = tan_max_angle * (b / MAX_W)

    tan_theta = (tan_x1 + tan_x2) / (1 - tan_x1 * tan_x2)
    theta = math.degrees(math.atan(tan_theta))
    return h, theta


def chase_function(d, theta, A=5, B=5, max_rolling=200, max_sp=5000):
    if theta > 10 or theta < -10:
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
            text = "s"
            send_msg(text)
        else:
            move_sp = B * d
            text = "p {}\n".format(min(move_sp, max_sp))
            send_msg(text)
    return text


def stop_function():
    text = "s"
    print(text)
    send_msg(text)


def check_camera(camera_idx=0, mirror=True, size=None):
    cap = cv2.VideoCapture(camera_idx)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if mirror is True:
            frame = frame[:, ::-1]

        if size is not None and len(size) == 2:
            frame = cv2.resize(frame, size)

        cv2.imshow('img', frame)
        k = cv2.waitKey(50)
        if k == 27:  # ESCキーで終了
            break

    cap.release()
    cv2.destroyAllWindows()


def main(mirror=True, size=None):
    cap_0 = cv2.VideoCapture(0)
    cap_1 = cv2.VideoCapture(1)
    while(cap_0.isOpened()):
        ret_0, frame_0 = cap_0.read()
        ret_1, frame_1 = cap_1.read()
        if mirror is True:
            frame_0 = frame_0[:, ::-1]
            frame_1 = frame_1[:, ::-1]

        if size is not None and len(size) == 2:
            frame_0 = cv2.resize(frame_0, size)
            frame_1 = cv2.resize(frame_1, size)

        boxes_0 = cascade(frame_0)
        boxes_1 = cascade(frame_1)

        # escape_flg = is_escape_flg(length)
        box_0 = boxes_0[0]
        box_1 = boxes_1[0]
        if box_0 or box_1:
            h, theta = cal_theta_h(box_0, box_1)
            text = chase_function(h, theta)
            # print('speed')
        else:
            text = "s"
            stop_function()

        print(text)
        k = cv2.waitKey(50)
        if k == 27:  # ESCキーで終了
            break

    cap_0.release()
    cap_1.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # main()
    check_camera(camera_idx=1)
