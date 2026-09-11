from picamera2 import Picamera2
import cv2
import numpy as np

# -------------------------------
# CAMERA SETUP
# -------------------------------
cam = Picamera2()
cam.start()

# -------------------------------
# GREEN COLOR RANGE IN HSV
# Adjust these if needed
# -------------------------------
lower_green = np.array([35, 80, 50])
upper_green = np.array([85, 255, 255])

# -------------------------------
# DISTANCE CALCULATION CONSTANTS
# REAL_WIDTH = actual width of green band in cm
# FOCAL_LENGTH = value found during calibration
# -------------------------------
REAL_WIDTH = 5.0      # Example: green band is 5 cm wide
FOCAL_LENGTH = 840.0  # Example value, replace with your real calibrated value

while True:
    # Capture a frame from the camera
    frame = cam.capture_array()

    # Convert image from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create mask for green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Remove small noise from the mask
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Only continue if at least one contour is found
    if contours:
        # Find the largest green contour
        largest_contour = max(contours, key=cv2.contourArea)

        # Ignore very small objects
        if cv2.contourArea(largest_contour) > 500:
            # Get bounding box around the green object
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Draw rectangle around detected green band
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Find center of object
            cx = x + w // 2
            cy = y + h // 2

            # Draw center point
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Calculate distance using object width in pixels
            distance = (REAL_WIDTH * FOCAL_LENGTH) / w

            # Print distance in terminal
            print(f"Distance: {distance:.2f} cm")

            # Show distance on screen
            cv2.putText(
                frame,
                f"Distance: {distance:.2f} cm",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            # Show center coordinates on screen
            cv2.putText(
                frame,
                f"Center: ({cx}, {cy})",
                (x, y + h + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

    # Show original frame with detection
    cv2.imshow("Green Band Detection", frame)

    # Show black-and-white mask
    cv2.imshow("Mask", mask)

    # Press q to quit
    if cv2.waitKey(1) == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
