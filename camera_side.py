import pickle
import socket
import struct

import cv2

cam = cv2.VideoCapture(-1, cv2.CAP_V4L2)
print('cam')
if cam.isOpened():
    print('open')
    try:
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((socket.gethostname(), 8382))
                server_socket.listen(1)
                while True:
                    try:
                        connection, address = server_socket.accept()
                        connection.settimeout(2)
                        while connection:
                            ret_cam, img = cam.read()
                            ret_imcode, jpg = cv2.imencode('.jpg', img)
                            data = pickle.dumps(jpg)
                            connection.sendall(struct.pack("L", len(data)) + data)
                    except (ConnectionError, TimeoutError, socket.timeout) as e:
                        pass
    except KeyboardInterrupt:
        pass

server_socket.close()
connection.close()
cam.release()
