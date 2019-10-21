'''
# rule based algorithm
# this program is deprecated...
'''

import numpy as np

SCREEN_CENTER_X = 400

# given parameters
# @LENGTH : distance between the machine and objects
# @BOXES  : boxes which represent detected positions
LENGTH = 100
BOXES = [[365, 75, 453, 453]]

# define parameters for the control
# @THR_FROTN_LEN : a threshold in the point of front length
# @THR_BOXSIZE : a threshold within a bix box or not
THR_FRONT_LEN = 100
THR_SIDE_LEN = 100
THR_BOXSIZE = 20000

# censerが前二つ横二つだと仮定


def decide_action(length, box):
    box_x_0 = box[0]
    box_y_0 = box[1]
    box_x_1 = box[2]
    box_y_1 = box[3]
    width = box_x_1 - box_x_0
    height = box_y_1 - box_y_1
    center_x = box_x_0 + 0.5 * len_x
    center_y = box_y_0 + 0.5 * len_y
    box_size_flg = 0
    if width * height >= THR_BOXSIZE:
        box_size_flg = 1

    front_r_len = length[0]
    front_l_len = length[1]
    side_r_len = length[2]
    side_l_len = length[3]

    # some reaction at front censer
    if front_r_len < THR_FRONT_LEN or front_l_len < THR_FRONT_LEN:
        # near the box
        if box_size_flg:
            # stop(success)
            print('s')
        elif front_r_len < THR_FRONT_LEN and front_l_len < THR_FRONT_LEN:
            # just back
            print('b')
        elif front_r_len < THR_FRONT_LEN:
            if side_l_len > THR_SIDE_LEN:
                # turn left and avoid object
                print('turn left')
            else:
                # just back
                print('back')
        else:
            if side_r_len > THR_SIDE_LEN:
                # turn right and avoid object
                print('turn right')
            else:
                # just back
                print('back')

    # no reaction at front censers
    # but thre are an object at side censers
    # a first priority is avoiding collision
    elif side_r_len < THR_SIDE_LEN or side_l_len < THR_SIDE_LEN:
        if side_r_len < THR_SIDE_LEN and side_l_len < THR_SIDE_LEN:
            # stop
            print('stop')
        if side_r_len < THR_SIDE_LEN:
            print('turn left')
        elif side_l_len < THR_SIDE_LEN:
            print('turn right')

    else:
        if box:
            # follow the box
            if center_x < SCREEN_CENTER_X:
                if side_l_len < THR_SIDE_LEN:
                    print('turn right')
                else:
                    print('follow')
            else:
                if side_r_len < THR_SIDE_LEN:
                    print('turn left')
                else:
                    print('follow')
            # if box does not exist, just go ahead
        else:
            print('search')
            # go straight
