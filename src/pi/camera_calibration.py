from picamera2 import Picamera2
import cv2
import numpy as np

cam = Picamera2()
cam.start()

lower_green = np.array([35, 80, 50])
upper_green = np.array([85, 255, 255])

KNOWN_DISTANCE = 30.0   # cm
REAL_WIDTH = 5.0        # cm

while True:
    frame = cam.capture_array()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(largest_contour) > 500:
            x, y, w, h = cv2.boundingRect(largest_contour)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            focal_length = (w * KNOWN_DISTANCE) / REAL_WIDTH

            print(f"Pixel Width: {w}")
            print(f"Focal Length: {focal_length:.2f}")

            cv2.putText(
                frame,
                f"Focal Length: {focal_length:.2f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    cv2.imshow("Calibration", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
