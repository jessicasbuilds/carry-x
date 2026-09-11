# CarryX Prototype Testing

The CarryX prototype was developed through incremental subsystem tests before combining perception, ranging, safety logic, serial communication, and movement commands.

## 1. Green-marker detection

The camera pipeline was first tested independently using OpenCV HSV segmentation.

Validation steps included:
- capture frames from the Raspberry Pi camera
- convert BGR frames to HSV
- isolate the green marker with an HSV mask
- find contours and reject small noise regions
- select the largest valid contour
- calculate the target center point

## 2. Camera calibration

A target with a known physical width was placed at a known distance. Its observed pixel width was used to estimate camera focal length.

```text
focal_length = (pixel_width * known_distance) / real_width
```

The resulting focal length was then used for approximate camera-based range estimation.

## 3. Distance estimation

The calibrated camera pipeline estimated target range from the target's apparent width:

```text
distance = (real_width * focal_length) / pixel_width
```

This allowed the following logic to respond to both horizontal target position and approximate distance.

## 4. Ultrasonic sensing

An ultrasonic distance sensor was tested through Raspberry Pi GPIO. Timeout handling was included so failed echo measurements would not indefinitely block the control loop.

## 5. Integrated decision test

The camera and ultrasonic systems were combined into one loop.

Current prototype thresholds:
- target following distance: 50 cm
- distance tolerance: ±10 cm
- obstacle stop distance: 20 cm
- horizontal centering tolerance: 40 pixels

The safety hierarchy gives obstacle detection priority over target-following commands.

## 6. Raspberry Pi to Arduino communication

Movement decisions are sent over serial at 9600 baud. To reduce unnecessary traffic, a new command is transmitted only when the requested movement state changes.

Command states include:
- `FORWARD`
- `BACKWARD`
- `LEFT`
- `RIGHT`
- `STOP`

## 7. Supervisory API testing

The Flask service exposes endpoints for session state, movement, halt behavior, and lost-target events. The service can also stay active in demo mode when no Arduino serial connection is available.

## Engineering observations

The testing process exposed CarryX as a system-integration problem rather than a single sensing problem. Camera calibration, lighting, target visibility, obstacle priority, serial behavior, motor response, and mechanical motion all affect the complete feedback loop.

Future validation should quantify:
- distance-estimation error
- command-to-motion latency
- stopping distance
- turning response
- target-loss recovery time
- tracking performance under changing lighting and occlusion

---

**Jessica Builds — From a thought to reality through innovation.**
