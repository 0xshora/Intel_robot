# coding: utf-8
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(
        '../data/haarcascades/haarcascade_lowerbody.xml')

def draw_detections(img, rects, thickness=1):
    img = np.array(img)
    for x, y, w, h in rects:
        pad_w, pad_h = int(0.15 * w), int(0.05 * h)
        cv2.rectangle(img, (x + pad_w, y + pad_h),
                      (x + w - pad_w, y + h - pad_h), (0, 255, 0), thickness)


def cascade(img):
    global face_cascade
    # img = cv2.resize(img, (680, 480)) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # カスケードファイルの読み込み
    # face_cascade = cv2.CascadeClassifier(
    # '../data/haarcascades/haarcascade_frontalface_default.xml')
    # face_cascade = cv2.CascadeClassifier('../data/haarcascades/haarcascade_upperbody.xml')
    # face_cascade = cv2.CascadeClassifier(
    #     '../data/haarcascades/haarcascade_lowerbody.xml')

    # delete minNeighbors=3
   
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minSize=(30, 20))
    print(faces)
    # draw_detections(img, faces)
    cv2.imshow('img', img)


def detect_boxes(mirror=True, size=None):
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret, frame = cap.read()

        if mirror is True:
            frame = frame[:, ::-1]

        if size is not None and len(size) == 2:
            frame = cv2.resize(frame, size)

        cascade(frame)

        k = cv2.waitKey(50)
        if k == 27:  # ESCキーで終了
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    detect_boxes()
