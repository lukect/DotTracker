import pickle
import socket

import cv2

cam = cv2.VideoCapture(-1, cv2.CAP_V4L2)
print('cam')
if cam.isOpened():
    print('open')
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((socket.gethostname(), 8382))
            server_socket.listen(1)
            while True:
                with server_socket.accept() as connection:
                    connection.settimeout(2)
                    while connection:
                        ret_camread, img = cam.read()
                        ret_imcode, jpg = cv2.imencode('.jpg', img)
                        packet = pickle.dumps(jpg)
                        packet_size = len(packet)
                        connection.sendall(packet_size.to_bytes(2, 'little', signed=False))
                        connection.sendall(packet)
    except KeyboardInterrupt:
        pass

cam.release()
