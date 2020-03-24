import cv2
import pygame
import serial
import numpy as np
import os
import time


class CollectingData:

    def __init__(self, url, serial_port, input_size):
        self.STREAM = url
        self.ser = serial.Serial(serial_port, 115200, timeout=1)
        pygame.init()
        pygame.display.set_mode((300, 300))
        self.input_size = input_size #240, 320

        self.right = np.array([0,0,1])
        self.left = np.array([1,0,0])
        self.forward = np.array([0,1,0])
        self.stop = np.array([0,0,0])

    def start_collection(self):
        cap = cv2.VideoCapture(self.STREAM)
        total_frame = 0
        saved_frame = 0
        X = np.empty((0, self.input_size[0]*self.input_size[1]))
        y = np.empty((0, 3))
        while True:
            # Capture frame
            ret, frame = cap.read()
            # resize
            to_x = cv2.resize(frame, self.input_size, interpolation=cv2.INTER_CUBIC)
            # Display the resulting frame
            cv2.imshow('frame', frame)
            total_frame += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

                if event.type == pygame.KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    # simple orders
                    if key_input[pygame.K_UP]:
                        print("Forward")
                        saved_frame += 1
                        X = np.vstack((X, to_x))
                        y = np.vstack((y, self.forward))
                        self.ser.write(chr(1).encode())

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        self.ser.write(chr(2).encode())

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        X = np.vstack((X, to_x))
                        y = np.vstack((y, self.right))
                        saved_frame += 1
                        self.ser.write(chr(3).encode())

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        X = np.vstack((X, to_x))
                        y = np.vstack((y, self.left))
                        saved_frame += 1
                        self.ser.write(chr(4).encode())

                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("exit")
                        self.ser.write(chr(0).encode())
                        self.ser.close()
                        break

                elif event.type == pygame.KEYUP:
                    self.ser.write(chr(0).encode())

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        file = str(int(time.time()))+"collected_data"
        path = "training_data"
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            np.savez(path + '/' + file + '.npz', train=X, train_labels=y)
        except IOError as e:
            print(e)

        print("Saved Images: "+str(saved_frame))
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    serial_port = "com9"
    input_size = (240, 320)
    url = "http://192.168.1.103:8080/video"
    cd = CollectingData(url=url, serial_port=serial_port, input_size=input_size)
    cd.start_collection()
