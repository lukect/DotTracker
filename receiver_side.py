import pickle
import socket
import struct

import cv2


def vector_position_from_centre(img_size, circle):
    centre = img_size[1] / 2, img_size[0] / 2  # y-x Array (OpenCV/NumPy)
    x_from_centre, y_from_centre = (circle[0] - centre[0], centre[1] - circle[1])
    return x_from_centre / centre[0], y_from_centre / centre[1]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
    socket.settimeout(2)
    socket.connect(("192.168.12.201", 8382))

    buffer = b''
    payload_size = struct.calcsize("L")

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

        hsv_conv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Lower boundary RED colour range values: Hue (0 - 10)
        red_range_low_hue = [(0, 100, 20), (10, 255, 255)]

        # Upper boundary RED colour range values: Hue (160 - 180)
        red_range_high_hue = [(160, 100, 20), (179, 255, 255)]

        lower_mask = cv2.inRange(hsv_conv, red_range_low_hue[0], red_range_low_hue[1])
        upper_mask = cv2.inRange(hsv_conv, red_range_high_hue[0], red_range_high_hue[1])
        full_mask = lower_mask + upper_mask

        red_filter = cv2.bitwise_and(img, img, mask=full_mask)
        grayscale_red_filter = cv2.cvtColor(red_filter, cv2.COLOR_BGR2GRAY)
        grayscale_red_filter = cv2.medianBlur(grayscale_red_filter, 5)  # Blurring makes circle detection easier.

        circles = cv2.HoughCircles(grayscale_red_filter, cv2.HOUGH_GRADIENT, 1, minDist=100, param1=20, param2=30,
                                   minRadius=30,
                                   maxRadius=0)

        if circles is not None:
            circle_x, circle_y, circle_radius = circles[0][0]  # Only track the most prominent circle/dot
            x, y = vector_position_from_centre(img.shape, (circle_x, circle_y))
            img = cv2.circle(img, (int(circle_x), int(circle_y)), int(circle_radius + 10), (0, 255, 255), 3)
            cv2.putText(img, "radius = " + str(round(circle_radius, 1)), (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 255), 2)
            cv2.putText(img, "x = " + str(round(x, 3)), (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            cv2.putText(img, "y = " + str(round(y, 3)), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        cv2.imshow('Live Raspberry Pi', mat=img)
        cv2.imshow('Live Raspberry Pi: Red-only view', mat=red_filter)

        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()
