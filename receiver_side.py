import pickle
import socket

import cv2

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
        socket.settimeout(2)
        socket.connect(("192.168.12.201", 8382))
        while socket:
            packet_size = int(socket.recv(4))  # int size
            packet = socket.recv(packet_size)  # 1GB max
            data = pickle.loads(packet)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR)
            cv2.imshow('Live Raspberry Pi ', mat=img)
except KeyboardInterrupt:
    pass

cv2.destroyAllWindows()
