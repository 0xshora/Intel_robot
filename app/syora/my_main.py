import cv2
import requests
import subprocess
import os

def main():
    avg = None
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if avg is None:
            avg = gray.copy().astype("float")
            continue
        cv2.accumulateWeighted(gray, avg, 0.5)
        mdframe = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

        # cv2.imshow('MotionDetected Frame', mdframe)

        thresh = cv2.threshold(mdframe, 3, 255, cv2.THRESH_BINARY)[1]

        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        target = contours[0]
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if max_area < area and area < 10000 and area > 1000:
                max_area = area
                target = cnt

        if max_area >= 8000:
            cv2.imwrite('tmp.jpg', frame)
            files = {"imageFile": open("tmp.jpg", "rb")}
            send_line(file_name='tmp.jpg')
            cap.release()
            # start following
            print("execute : python2 ../201_main.py")
            os.chdir('../')
            subprocess.call(["python2", "201_main.py"])
            break

        key = cv2.waitKey(30)
        if key == 27:
            break
    cap.release()
    # cap.destroyAllWindows()

def send_line(file_name=None):
    if not file_name:
        files = {"imageFile": open(file_name, "rb")}

    if not file_name:
        requests.post("https://notify-api.line.me/api/notify", headers={"Authorization": "Bearer $LINE_AUTH$"}, params={"message": "start following!"}, files=files)

    else:
        requests.post("https://notify-api.line.me/api/notify", headers={"Authorization": "Bearer $LINE_AUTH$"}, params={"message": "start following!"})

if __name__ == '__main__':
    main()
