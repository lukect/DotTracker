import pickle
import socket

import cv2

cam = cv2.VideoCapture(0)
if cam.isOpened():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((socket.gethostname(), 8382))
            server_socket.listen(1)
            while True:
                with server_socket.accept() as connection:
                    connection.settimeout(2)
                    while connection:  # TODO: WHILE CONNECTED
                        ret_camread, img = cam.read()
                        ret_imcode, jpg = cv2.imencode('.jpg', img)
                        packet = pickle.dumps(jpg)
                        connection.sendall(packet)
    except KeyboardInterrupt:
        pass

cam.release()
