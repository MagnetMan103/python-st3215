import serial
import time

# Configuration
PORT = '/dev/tty.usbmodem5A680132761'
SERVO_ID = 1
BAUD_RATE = 1000000

# Protocol constants
INST_WRITE = 0x03

# Addresses
ADDR_MIN_ANGLE = 0x09  # 2 bytes
ADDR_MAX_ANGLE = 0x0B  # 2 bytes
ADDR_LOCK = 0x37  # 1 byte (SRAM, controls EEPROM write lock)


def checksum(data):
    """Calculate checksum: ~(sum of bytes) & 0xFF"""
    return (~sum(data)) & 0xFF


def build_write_packet(servo_id, address, values):
    """Build a WRITE packet. values is a list of bytes."""
    length = len(values) + 3  # instruction + address + data + checksum
    packet_data = [servo_id, length, INST_WRITE, address] + values
    cs = checksum(packet_data)
    return bytes([0xFF, 0xFF] + packet_data + [cs])


def main():
    print("=== Reset ST3215 Angle Limits to 0-4095 ===\n")

    # Open serial port
    ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
    time.sleep(0.1)
    ser.reset_input_buffer()

    # Step 1: Unlock EEPROM (write 0 to lock register)
    print("1. Unlocking EEPROM...")
    packet = build_write_packet(SERVO_ID, ADDR_LOCK, [0])
    ser.write(packet)
    time.sleep(0.05)

    # Step 2: Set min angle = 0 (2 bytes: low=0, high=0)
    print("2. Setting min angle = 0...")
    packet = build_write_packet(SERVO_ID, ADDR_MIN_ANGLE, [0x00, 0x00])
    ser.write(packet)
    time.sleep(0.05)

    # Step 3: Set max angle = 4095 (2 bytes: low=0xFF, high=0x0F)
    print("3. Setting max angle = 4095...")
    packet = build_write_packet(SERVO_ID, ADDR_MAX_ANGLE, [0xFF, 0x0F])
    ser.write(packet)
    time.sleep(0.05)

    # Step 4: Lock EEPROM (write 1 to lock register)
    print("4. Locking EEPROM...")
    packet = build_write_packet(SERVO_ID, ADDR_LOCK, [1])
    ser.write(packet)
    time.sleep(0.05)

    ser.close()
    print("\n✓ Done! Angle limits reset to 0-4095 (full 360°)")
    print("\nNow test with:")
    print("  servo.MoveTo(1, 0)")
    print("  servo.MoveTo(1, 4095)")


if __name__ == "__main__":
    main()