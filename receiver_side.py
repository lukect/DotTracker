import pickle
import socket
import struct

import cv2

buffer = b''
payload_size = struct.calcsize("L")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
        socket.settimeout(2)
        socket.connect(("192.168.12.201", 8383))
        while socket:
            while len(buffer) < payload_size:
                buffer += socket.recv(4096)
            packed_msg_size = buffer[:payload_size]

            buffer = buffer[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            while len(buffer) < msg_size:
                buffer += socket.recv(4096)
            frame_data = buffer[:msg_size]
            buffer = buffer[msg_size:]

            frame = pickle.loads(frame_data)
            img = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow('Live Raspberry Pi ', mat=img)
except KeyboardInterrupt:
    pass

cv2.destroyAllWindows()
