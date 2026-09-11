# CarryX

**Autonomous Follow-Me Robotic Bag**  
Robotics · Computer Vision · Embedded Systems · Motor Control · Sensor Fusion · Web Control · Mechanical CAD

> **Jessica Builds — From a thought to reality through innovation.**

CarryX is a mechatronics project exploring autonomous luggage that can detect and follow its owner while maintaining a safe distance and responding to obstacles.

I was involved across the full project, including system architecture, sensing, embedded control, software integration, motor-control logic, prototyping, testing, interface development, hardware selection, mechanical CAD, and iterative engineering decisions.

The project began with a UWB-based localization architecture and evolved through hands-on prototyping into a camera + ultrasonic implementation using a Raspberry Pi, Arduino Nano, OpenCV, serial communication, and differential-drive motor control.

## The engineering problem

A follow-me platform has to solve several problems at the same time:

- locate the user relative to the robot
- determine whether to move forward, reverse, or turn
- maintain a useful following distance
- stop safely when an obstacle is detected
- coordinate sensing, high-level decision logic, and low-level motor actuation
- provide a simple human interface to start, stop, and monitor the system
- package electronics, drive components, and sensors into a mechanically usable platform

The original design targeted indoor autonomous following with a suitcase-style mobile platform and separated high-level processing on a Raspberry Pi from real-time motor control on an Arduino.

## Architecture

```text
             USER / TRACKING TARGET
                      │
        ┌─────────────┴─────────────┐
        │                           │
     Pi Camera                Ultrasonic Sensor
   green-marker CV             obstacle distance
        │                           │
        └─────────────┬─────────────┘
                      │
                Raspberry Pi
        OpenCV + decision logic
                      │
              Serial @ 9600 baud
                      │
                 Arduino Nano
                      │
                  L298N Driver
                 ┌────┴────┐
             Left Motor  Right Motor
```

A lightweight Flask service adds a control/monitoring layer between the user interface and the embedded system.

## Mechanical design / CAD

CarryX also includes mechanical design work in AutoCAD. A base-plate drawing was created to define the physical foundation of the mobile platform and provide a structured mounting surface for the embedded electronics, battery/power hardware, motor-drive components, sensors, and drivetrain.

The base plate is part of the chassis-level design problem: converting the electrical and software architecture into a physical robot with practical component placement, mounting points, cable routing, weight distribution, and space for later enclosure development.

The original AutoCAD DWG is maintained as a project artifact and is intended to live in:

```text
cad/base-plate.dwg
```

Because the connected GitHub upload path does not support raw DWG binary writes, the drawing is documented here until the source file is added manually to that location.

## Prototype control pipeline

### 1. Vision-based target detection

The Raspberry Pi camera captures frames and converts them into HSV color space. A green marker is isolated using an HSV mask, small artifacts are filtered, and the largest valid contour is treated as the tracking target.

The implementation calculates:

- target bounding box
- target center `(cx, cy)`
- horizontal error relative to the camera frame center
- approximate target distance from apparent marker width

### 2. Camera calibration and distance estimation

A separate calibration program estimates focal length from a target of known physical width at a known distance.

The tracking code then applies the pinhole-camera relationship:

```text
distance = (real target width × focal length) / observed pixel width
```

This turns the camera from a simple detector into a rough ranging sensor.

### 3. Obstacle safety override

An ultrasonic sensor is connected directly to Raspberry Pi GPIO and continuously measures forward obstacle distance.

The current test configuration prioritizes obstacle avoidance over tracking commands. If an obstacle is inside the stop threshold, the robot stops even when the target is visible.

### 4. Following decision logic

The prototype combines image position and estimated range:

```text
if obstacle too close:
    STOP
elif target left of center:
    LEFT
elif target right of center:
    RIGHT
elif target too far away:
    FORWARD
elif target too close:
    BACKWARD
else:
    STOP
```

Current test values include a 50 cm target following distance, ±10 cm distance tolerance, 20 cm obstacle stop distance, and a 40-pixel horizontal centering tolerance.

### 5. Arduino motor control

The Raspberry Pi sends movement commands to an Arduino Nano over serial communication.

The Arduino controls two DC motors through an L298N motor driver and supports:

- `START`
- `STOP`
- `FORWARD`
- `REVERSE`
- `LEFT`
- `RIGHT`
- `HALT`

Forward/reverse motion drives both wheels together. Turning uses differential wheel speeds, with one side faster than the other.

A session state prevents movement commands from actuating the motors until the system has been explicitly started.

## Control API

CarryX also includes a Flask control service that automatically searches for the Arduino serial port and exposes endpoints for the interface and tracking layer:

| Route | Purpose |
| --- | --- |
| `GET /status` | Read running state and lost-target count |
| `POST /start` | Arm/start the following session |
| `POST /stop` | Stop the session |
| `POST /forward` | Send forward command |
| `POST /left` | Send left command |
| `POST /right` | Send right command |
| `POST /reverse` | Send reverse command |
| `POST /halt` | Stop motion while retaining session state |
| `POST /lost` | Halt and record a lost-target event |

If no Arduino is available, the server can remain up in demo mode rather than failing completely.

## Web interface

The uploaded CarryX V1.0 web interface connects to the Raspberry Pi service on port 5000. It can start and stop a following session, poll system status, display runtime state, and record tracking-loss events.

This creates a simple supervisory layer over the physical robot rather than requiring the operator to control it directly from a terminal.

## Original UWB architecture

The initial design used Decawave/DWM1000 Ultra-Wideband ranging with a wearable tag and multiple anchors. The architecture separated:

- UWB ranging and high-level localization on Raspberry Pi
- Arduino-based motor control
- differential-drive motion
- obstacle sensing
- a supervisory user interface
- 12 V power distribution with regulated 5 V / 3.3 V rails

The design target was approximately 10–30 cm positioning accuracy, up to 10 m tracking range, ~0.5 m/s maximum speed, sub-0.5-second obstacle reaction, and ~10 Hz control updates.

The camera/ultrasonic prototype represents an important engineering iteration: instead of waiting for every element of the original architecture, the following behavior could be tested using hardware and sensors already available.

## Hardware / software stack

**Mechanical design**
- AutoCAD
- base-plate / chassis design
- component layout and mounting planning

**Compute & embedded**
- Raspberry Pi
- Arduino Nano
- serial communication

**Perception & safety**
- Raspberry Pi Camera
- OpenCV
- NumPy
- HSV color segmentation
- HC-SR04-style ultrasonic ranging
- Raspberry Pi GPIO

**Actuation**
- L298N motor driver
- two DC gear motors
- PWM speed control
- differential steering

**Software**
- Python
- C/C++ / Arduino firmware
- Flask
- Flask-CORS
- HTML/CSS/JavaScript interface

## Design philosophy

CarryX is not just a motorized bag. It is a system-integration problem connecting perception, decision-making, communications, electronics, controls, mechanics, safety, and user interaction.

The most interesting part of the project is the loop:

**sense → estimate → decide → command → move → sense again**

That same loop appears throughout autonomous robots, industrial automation, drones, and aerospace systems.

## Project status

This repository documents the design, implementation, and prototype testing of CarryX. The project includes system architecture, mechanical CAD, camera-based target tracking, ultrasonic obstacle detection, Pi-to-Arduino communication, motor-control firmware, supervisory software, hardware integration, and iterative testing.

It should not be interpreted as a production-ready autonomous luggage product.

## Next engineering iterations

- replace color-marker tracking with more robust person/target tracking
- compare camera ranging against UWB ranging
- fuse multiple sensing modalities instead of relying on one target source
- add encoder feedback for closed-loop wheel-speed control
- implement PID distance/heading control
- formalize lost-target recovery behavior
- add battery telemetry and fault monitoring
- characterize latency, range error, turn response, and stopping distance experimentally
- refine chassis CAD around final component dimensions and enclosure constraints

---

### Jessica Builds
**From a thought to reality through innovation.**
