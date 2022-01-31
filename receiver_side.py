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

            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

            cv2.imshow('Live Raspberry Pi ', mat=img)

            if cv2.waitKey(1) == ord('q'):
                break
except KeyboardInterrupt:
    pass

cv2.destroyAllWindows()
