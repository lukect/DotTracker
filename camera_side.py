import pickle
import socket
import struct

import cv2

cam = cv2.VideoCapture(-1, cv2.CAP_V4L2)

if cam.isOpened():
    print('Camera successfully initialized!')

    try:
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((socket.gethostname(), 8382))
                server_socket.listen(1)
                print('Server Socket successfully initialized!\n'
                      'Listening on port ' + server_socket.getsockname()[1])
                while True:
                    try:
                        connection, address = server_socket.accept()
                        connection.settimeout(2)
                        print(str(address) + ' connected!')
                        while connection:
                            ret_cam, img = cam.read()
                            ret_imcode, jpg = cv2.imencode('.jpg', img)
                            data = pickle.dumps(jpg)
                            connection.sendall(struct.pack('L', len(data)) + data)
                    except (ConnectionError, TimeoutError, socket.timeout) as e:
                        print('Disconnect occurred!')
                        pass
    except KeyboardInterrupt:
        pass
else:
    print('Could not initialize camera!')

server_socket.close()
connection.close()
cam.release()
print('Successfully shutdown camera streaming!')
