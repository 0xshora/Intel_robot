import numpy as np
import cv2

def main(mirror=True, size=None):
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret, frame = cap.read()

        if mirror is True:
            frame = frame[:, ::-1]

        if size is not None and len(size) == 2:
            frame = cv2.resize(frame, size)

        cv2.imshow('tmp', frame)

        k = cv2.waitKey(50)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
