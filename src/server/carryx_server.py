from flask import Flask, jsonify
from flask_cors import CORS
import serial
import serial.tools.list_ports

app = Flask(__name__)
CORS(app)

# ── SERIAL SETUP ──────────────────────────────
def find_arduino():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "ttyUSB" in port.device or "ttyACM" in port.device:
            return port.device
    return None

ARDUINO_PORT = find_arduino() or "/dev/ttyUSB0"
BAUD_RATE    = 9600

try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    print(f"Arduino connected on {ARDUINO_PORT}")
except Exception as e:
    arduino = None
    print(f"Arduino not found: {e} — running in demo mode")

# ── STATE ─────────────────────────────────────
state = {
    "running":     False,
    "lost_events": 0
}

# ── HELPER ────────────────────────────────────
def send(command):
    if arduino:
        arduino.write(f"{command}\n".encode())
        print(f"Sent to Arduino: {command}")

# ── SESSION ROUTES (called by the app) ────────
@app.route("/status")
def status():
    return jsonify(state)

@app.route("/start", methods=["POST"])
def start():
    state["running"] = True
    send("START")
    return jsonify({"ok": True})

@app.route("/stop", methods=["POST"])
def stop():
    state["running"] = False
    send("STOP")
    return jsonify({"ok": True})

# ── MOVEMENT ROUTES (called by Pi camera code) ─
# The camera script imports this or calls these
# routes internally to send direction commands

@app.route("/forward", methods=["POST"])
def forward():
    if state["running"]:
        send("FORWARD")
    return jsonify({"ok": True})

@app.route("/left", methods=["POST"])
def left():
    if state["running"]:
        send("LEFT")
    return jsonify({"ok": True})

@app.route("/right", methods=["POST"])
def right():
    if state["running"]:
        send("RIGHT")
    return jsonify({"ok": True})

@app.route("/reverse", methods=["POST"])
def reverse():
    if state["running"]:
        send("REVERSE")
    return jsonify({"ok": True})

@app.route("/halt", methods=["POST"])
def halt():
    if state["running"]:
        send("HALT")
    return jsonify({"ok": True})

@app.route("/lost", methods=["POST"])
def lost():
    # called by camera code when marker is not visible
    state["lost_events"] += 1
    send("HALT")
    print(f"Tracking lost — total lost events: {state['lost_events']}")
    return jsonify({"ok": True})

# ── RUN ───────────────────────────────────────
if __name__ == "__main__":
    print("CarryX server starting on port 5000...")
    app.run(host="0.0.0.0", port=5000)
