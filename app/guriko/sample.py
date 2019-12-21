#-*- coding: utf-8 -*-
import cv2
import numpy as np
from scipy import stats

version = cv2.__version__.split(".")
CVversion = int(version[0])

capture = cv2.VideoCapture(0)

#手の認識パラメータ
hmin = 0
hmax = 20
smin = 50

gu_file_count = 0
choki_file_count = 0
pa_file_count = 0

def save_hand(mode,img):
    global gu_file_count
    global choki_file_count
    global pa_file_count

    if mode == 'g':
        filename = 'img_gu{0:03d}.png'.format(gu_file_count)
        print('saving {0}'.format(filename))
        cv2.imwrite(filename,img)
        gu_file_count += 1
    elif mode == 'c':
        filename = 'img_choki{0:03d}.png'.format(choki_file_count)
        print('saving {0}'.format(filename))
        cv2.imwrite(filename,img)
        choki_file_count += 1
    elif mode == 'p':
        filename = 'img_pa{0:03d}.png'.format(pa_file_count)
        print('saving {0}'.format(filename))
        cv2.imwrite(filename,img)
        pa_file_count += 1

#video_input.set(cv2.CAP_PROP_FPS,15)
#video_input.set(cv2.CAP_PROP_FRAME_WIDTH,320)
#video_input.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

while(True):
    #capture = cv2.VideoCapture(0)
    ret,frame = capture.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hsv_channels = cv2.split(hsv)
    h_channel = hsv_channels[0]
    s_channel = hsv_channels[1]

    h_binary = cv2.GaussianBlur(h_channel,(5,5),0)
    ret,h_binary = cv2.threshold(h_binary,hmax,255,cv2.THRESH_TOZERO_INV)
    ret,h_binary = cv2.threshold(h_binary,hmin,255,cv2.THRESH_BINARY)

    ret,s_binary = cv2.threshold(s_channel,smin,255,cv2.THRESH_BINARY)
    hs_and = h_binary & s_binary

    if CVversion == 2:
        img_dist, img_label = cv2.distanceTransformWithLabels(255-hs_and, cv2.cv.CV_DIST_L2, 5)
    else:
        img_dist, img_label = cv2.distanceTransformWithLabels(255-hs_and, cv2.DIST_L2, 5)
        img_label = np.uint8(img_label) & hs_and

        img_label_not_zero = img_label[img_label != 0]

        if len(img_label_not_zero) != 0:
            m = stats.mode(img_label_not_zero)[0]
        else:
            m = 0
        hand = np.uint8(img_label == m)*255

        hs = np.concatenate((h_channel, h_binary), axis=0)
        hs_bin = np.concatenate((s_channel, s_binary), axis=0)
        hs_final = np.concatenate((hs_and, hand), axis=0)
        hs_all = np.concatenate((hs, hs_bin, hs_final), axis=1)
        

        cv2.imshow('hand',hand)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('g'):
            save_hand('g',hand)
        elif key & 0xFF == ord('c'):
            save_hand('c',hand)
        elif key & 0xFF == ord('p'):
            save_hand('p',hand)

capture.release()
cv2.destroyAllWindows()
