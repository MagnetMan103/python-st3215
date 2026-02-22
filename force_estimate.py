#!/usr/bin/env python3
import os
import time
from st3215 import ST3215

# -----------------------------
# Configuration
# -----------------------------
servo_id = 1
Kt = 0.5                  # Torque constant (Nm/A) from datasheet
arm_length = 0.254         # meters
force_limit =   0.7         # N — stop if exceeded
dev = "/dev/tty.usbmodem5A680132761"

# -----------------------------
# Connect to servo bus
# -----------------------------
servo_bus = ST3215(dev)
print(f"Connected to servo bus at {dev}, monitoring servo {1}")

# -----------------------------
# Start servo movement
# -----------------------------
servo_bus.StartServo(1)
servo_bus.SetAcceleration(1, 20)
servo_bus.SetSpeed(1, 50)
servo_bus.MoveTo(1, 2048)   # target position
print("Servo moving...")

# -----------------------------
# Main loop: monitor force and stop on collision
# -----------------------------
try:
    while True:
        current_mA = servo_bus.ReadCurrent(1)
        if current_mA is not None:
            current_A = current_mA / 1000.0       # convert mA -> A
            torque = Kt * current_A
            force = torque / arm_length

            print(f"Current: {current_A:.2f} A | Torque: {torque:.2f} Nm | Force: {force:.2f} N")

            # Collision detection
            if force >= force_limit:
                print(f"⚠️ Force limit exceeded! Stopping servo {1}")
                servo_bus.StopServo(1)
                break  # exit loop immediately
        else:
            print("⚠️ Current reading failed")

        time.sleep(0.05)  # 20 Hz update

except KeyboardInterrupt:
    servo_bus.StopServo(1)
    print("\nForce logging stopped by user")