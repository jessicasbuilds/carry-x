# CarryX — Original Engineering Proposal

## Project objective

CarryX was designed as an autonomous self-following robotic bag capable of detecting and following its owner while maintaining a safe following distance.

The original architecture combined localization, embedded computing, motor control, obstacle sensing, power distribution, and a supervisory user interface into one mobile mechatronic platform.

## Original localization architecture

The first design used Ultra-Wideband (UWB) ranging with a wearable tag and multiple anchors mounted on the robot. A Raspberry Pi handled high-level ranging and directional decisions, while an Arduino handled motor actuation.

```text
UWB Tag
   │ RF ranging
   ▼
UWB Anchors
   │
   ▼
Raspberry Pi
   │ serial commands
   ▼
Arduino Nano
   │ PWM / direction
   ▼
L298N Motor Driver
   ├── Left DC Motor
   └── Right DC Motor
```

The system architecture separated high-level perception/localization from low-level motor control, similar to layered control approaches used in robotics and industrial automation.

## Proposed hardware

- Raspberry Pi
- Arduino Nano
- DWM1000 / DW1000-class UWB modules
- L298N motor driver
- DC gear motors
- caster wheels
- 12 V rechargeable battery
- DC-DC buck conversion for 5 V and 3.3 V rails
- obstacle-detection sensors
- suitcase-style enclosure / robotic base

## Power architecture

The original design used a 12 V battery for the drive system, with regulated rails for the logic and sensing hardware.

Estimated design power was approximately 20 W after adding safety margin to the calculated system load. The design therefore targeted a battery capable of supplying at least 3 A.

## Intended performance targets

| Function | Design target |
| --- | --- |
| Tracking range | up to 10 m |
| Positioning accuracy | approximately 10–30 cm |
| Maximum speed | approximately 0.5 m/s |
| Obstacle reaction | under 0.5 s |
| Control update rate | approximately 10 Hz |
| Following distance | approximately 1–3 m |

These were engineering targets from the proposal, not final validated performance claims.

## Control and interface concept

The system was intended to support:

- start / stop control
- system status monitoring
- distance or signal-strength display
- motor activity / movement-state feedback
- autonomous user-following
- obstacle override behavior

## Engineering questions

The project explored several core robotics problems:

- how to estimate user direction robustly
- how to prevent unstable or oscillatory following behavior
- how to prioritize obstacle avoidance over tracking commands
- how to fuse multiple sensor signals
- how to manage latency between sensing, processing, and actuation
- how to size and distribute power for a mobile platform

## Evolution into the camera + ultrasonic prototype

The final software repository also documents a practical implementation path using a Raspberry Pi camera and ultrasonic sensing. This allowed target-following logic, distance control, obstacle overrides, and Pi-to-Arduino communication to be tested before every part of the original UWB architecture was available.

That iteration is documented in:

- `src/pi/camera_greenband.py`
- `src/pi/camera_calibration.py`
- `src/pi/calculate_object_distance.py`
- `src/pi/testing_ultrasonic_camera.py`
- `src/server/carryx_server.py`
- `web/index.html`

## Jessica Builds

**From a thought to reality through innovation.**
