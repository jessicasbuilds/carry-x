# CarryX Architecture

CarryX separates perception and high-level decision-making from low-level motor actuation.

## Prototype architecture

```text
Tracking target
     |
Pi Camera -----> OpenCV target detection ----+
                                              |
Ultrasonic ---> obstacle distance ------------+--> Raspberry Pi decision logic
                                                       |
                                                       | serial @ 9600 baud
                                                       v
                                                   Arduino Nano
                                                       |
                                                       v
                                                   L298N driver
                                                   /          \
                                             left motor    right motor
```

## Perception

The Raspberry Pi camera captures frames that are converted to HSV color space. A green tracking marker is segmented with an HSV mask, and the largest valid contour is used to estimate target position.

The implementation extracts the target bounding box and center position and compares the target's horizontal position with the center of the camera frame.

## Range estimation

Camera distance is estimated using a calibrated focal length and the apparent width of a target with known physical width:

```text
distance = (real_width * focal_length) / pixel_width
```

A dedicated calibration script estimates focal length from a known-distance reference measurement.

## Safety sensing

An ultrasonic sensor measures forward obstacle distance. Obstacle detection has higher priority than tracking movement, so a close obstacle forces a stop command.

## Decision hierarchy

```text
1. obstacle too close -> STOP
2. target left       -> LEFT
3. target right      -> RIGHT
4. target too far    -> FORWARD
5. target too close  -> BACKWARD
6. target in range   -> STOP
```

## Embedded control

Movement commands are transmitted from Raspberry Pi to Arduino over serial. The Arduino controls the two-wheel differential drive through an L298N motor driver.

## Supervisory software

A Flask service provides start, stop, movement, halt, status, and lost-target endpoints for the user interface and control layer.

## Architecture evolution

The initial CarryX design investigated Ultra-Wideband localization with a wearable tag and multiple anchors. Prototype development then used camera tracking plus ultrasonic ranging to validate the autonomous-following control loop with available hardware.

This progression reflects the project philosophy: validate the system behavior early, learn from hardware, and iterate the sensing architecture.

---

**Jessica Builds — From a thought to reality through innovation.**
