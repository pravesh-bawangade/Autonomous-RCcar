from keras.models import load_model
import cv2
import serial


def main(url, input_size, model_path, serial_port):

    ser = serial.Serial(serial_port, 115200, timeout=1)
    cap = cv2.VideoCapture(url)
    while True:
        # Capture frame
        ret, frame = cap.read()
        to_x = cv2.resize(frame, input_size, interpolation=cv2.INTER_CUBIC)
        model = load_model(model_path)
        _, out = model.predict(to_x)
        ser.write(chr(1+out.argmax(-1)).encode())

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    ser.close()


if __name__ == "__main__":

    # @TODO: test this code.

    main("http://192.168.1.103:8080/video", (240,320), "/model.h5", "com9")