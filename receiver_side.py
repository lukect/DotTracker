import pickle
import socket

import cv2

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
        socket.settimeout(2)
        socket.connect(("192.168.12.124", 8382))
        while socket:
            packet = socket.recv(1073741824)  # 1GB max
            data = pickle.loads(packet)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR)
            cv2.imshow('Live Raspberry Pi ', mat=img)
except KeyboardInterrupt:
    pass

cv2.destroyAllWindows()
