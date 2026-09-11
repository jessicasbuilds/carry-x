from picamera2 import Picamera2
import cv2
import numpy as np
import serial
import time
import RPi.GPIO as GPIO

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

TRIG = 23
ECHO = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, GPIO.LOW)
time.sleep(0.5)

cam = Picamera2()
cam.start()

lower_green = np.array([35, 80, 50])
upper_green = np.array([85, 255, 255])
REAL_WIDTH = 5.0
FOCAL_LENGTH = 840.0
TARGET_DISTANCE = 50
DISTANCE_TOLERANCE = 10
OBSTACLE_STOP_DISTANCE = 20
CENTER_TOLERANCE = 40
last_command = ""

def get_ultrasonic_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    pulse_start = time.time()
    pulse_end = time.time()
    timeout = time.time() + 0.03
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if time.time() > timeout:
            return -1
    timeout = time.time() + 0.03
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if time.time() > timeout:
            return -1
    pulse_duration = pulse_end - pulse_start
    return round(pulse_duration * 17150, 2)

try:
    while True:
        frame = cam.capture_array()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape
        frame_center = width // 2
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cam_distance = -1
        ultrasonic_distance = get_ultrasonic_distance()
        command = "STOP"
        target_found = False

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 500:
                target_found = True
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cx = x + w // 2
                cy = y + h // 2
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.line(frame, (frame_center, 0), (frame_center, height), (255, 0, 0), 2)
                cam_distance = round((REAL_WIDTH * FOCAL_LENGTH) / w, 2)
                error = cx - frame_center

                if ultrasonic_distance > 0 and ultrasonic_distance < OBSTACLE_STOP_DISTANCE:
                    command = "STOP"
                elif error < -CENTER_TOLERANCE:
                    command = "LEFT"
                elif error > CENTER_TOLERANCE:
                    command = "RIGHT"
                else:
                    if cam_distance > TARGET_DISTANCE + DISTANCE_TOLERANCE:
                        command = "FORWARD"
                    elif cam_distance < TARGET_DISTANCE - DISTANCE_TOLERANCE:
                        command = "BACKWARD"
                    else:
                        command = "STOP"

                cv2.putText(frame, f"Cam Dist: {cam_distance:.2f} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f"Error: {error}", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        else:
            command = "STOP"

        if command != last_command:
            ser.write((command + "\n").encode())
            print("Sent command:", command)
            last_command = command

        cv2.putText(frame, f"Ultrasonic: {ultrasonic_distance} cm", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Command: {command}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        if not target_found:
            cv2.putText(frame, "Target not found", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Green Band Detection", frame)
        cv2.imshow("Mask", mask)
        if cv2.waitKey(1) == ord('q'):
            break
        time.sleep(0.05)
except KeyboardInterrupt:
    print("Program stopped.")
finally:
    ser.close()
    GPIO.cleanup()
    cv2.destroyAllWindows()
