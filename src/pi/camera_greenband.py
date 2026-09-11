from picamera2 import Picamera2
import cv2
import numpy as np

cam = Picamera2()
cam.start()

lower_green = np.array([35, 80, 50])
upper_green = np.array([85, 255, 255])

while True:
    frame = cam.capture_array()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create green mask
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Pick the largest green object
        largest_contour = max(contours, key=cv2.contourArea)

        # Ignore tiny objects/noise
        if cv2.contourArea(largest_contour) > 500:
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Draw rectangle around detected green band
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Find center point
            cx = x + w // 2
            cy = y + h // 2

            # Draw center dot
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Print center position
            print("Green object center:", cx, cy)

    cv2.imshow("Original with Detection", frame)
    cv2.imshow("Green Mask", mask)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
