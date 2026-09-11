# Arduino Motor-Control Layer

CarryX uses an Arduino Nano as the low-level actuation controller between the Raspberry Pi decision layer and the L298N motor driver.

## Serial interface

The Arduino listens at **9600 baud** for newline-terminated movement commands from the Raspberry Pi.

Supported commands:

| Command | Effect |
| --- | --- |
| `START` | Arms the session while keeping the motors stopped |
| `STOP` | Ends the session and halts the motors |
| `FORWARD` | Drives both motors forward |
| `REVERSE` | Drives both motors in reverse |
| `LEFT` | Differential turn with the right wheel faster |
| `RIGHT` | Differential turn with the left wheel faster |
| `HALT` | Stops motion while leaving the session armed |

A session-state guard prevents directional commands from actuating the robot until `START` has been received.

## Motor-driver mapping

The firmware is designed around an L298N dual H-bridge with separate enable/PWM and direction pins for the left and right motors.

The implementation uses three speed levels:

- base forward/reverse speed
- faster turn-side speed
- slower turn-side speed

This produces differential steering without requiring a separate steering actuator.

## Safety behavior

On startup, on `STOP`, on `HALT`, or when an unknown serial command is received, the motor outputs are returned to a halted state.

## Integration

The Raspberry Pi tracking layer computes movement intent from camera position, estimated target distance, and ultrasonic obstacle distance. That movement intent is then serialized to this Arduino control layer for physical actuation.

The original `.ino` firmware is part of the CarryX source set; this document records its interface and behavior for repository navigation.
