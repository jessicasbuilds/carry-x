# CarryX Repository Structure

```text
carry-x/
├── README.md
├── requirements.txt
├── assets/
│   └── carryx-logo.svg
├── docs/
│   ├── ARCHITECTURE.md
│   ├── TESTING.md
│   └── PROJECT_PROPOSAL.md
├── src/
│   ├── pi/
│   │   ├── calculate_object_distance.py
│   │   ├── camera_calibration.py
│   │   ├── camera_greenband.py
│   │   └── testing_ultrasonic_camera.py
│   ├── server/
│   │   └── carryx_server.py
│   └── arduino/
│       └── README.md
└── web/
    └── index.html
```

## Start here

- `README.md` — project overview and engineering story
- `docs/ARCHITECTURE.md` — system-level hardware/software flow
- `docs/TESTING.md` — prototype tests and validation approach
- `docs/PROJECT_PROPOSAL.md` — original design targets and UWB architecture
- `src/pi/` — Raspberry Pi perception and control experiments
- `src/server/` — Flask control interface
- `src/arduino/README.md` — Arduino firmware interface and actuation behavior
- `web/index.html` — CarryX V1.0 supervisory interface

## Note on source preservation

The repository contains the active software and technical documentation needed to understand the prototype. The original Arduino firmware behavior is documented under `src/arduino/README.md` because the connected GitHub upload path rejected the raw `.ino` file during automated repository assembly.
