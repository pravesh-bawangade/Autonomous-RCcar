import cv2
import numpy as np


def video_stream():
    # input video from smartphone
    cap = cv2.VideoCapture("http://192.168.1.103:8080/video")

    while True:
        # Capture frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_stream()
