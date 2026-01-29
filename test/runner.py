import serial
import time

PORT = '/dev/tty.usbmodem5A680132761'
SERVO_ID = 1
BAUD_RATE = 1000000

INST_WRITE = 0x03
ADDR_POSITION_CORRECTION = 0x1F  # 2 bytes
ADDR_LOCK = 0x37

def checksum(data):
    return (~sum(data)) & 0xFF

def build_write_packet(servo_id, address, values):
    length = len(values) + 3
    packet_data = [servo_id, length, INST_WRITE, address] + values
    cs = checksum(packet_data)
    return bytes([0xFF, 0xFF] + packet_data + [cs])

print("=== Reset Position Correction ===\n")

ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
time.sleep(0.1)
ser.reset_input_buffer()

# Unlock EEPROM
print("1. Unlocking EEPROM...")
ser.write(build_write_packet(SERVO_ID, ADDR_LOCK, [0]))
time.sleep(0.05)

# Reset position correction to 0 (2 bytes: 0x00, 0x00)
print("2. Resetting position correction to 0...")
ser.write(build_write_packet(SERVO_ID, ADDR_POSITION_CORRECTION, [0x00, 0x00]))
time.sleep(0.05)

# Lock EEPROM
print("3. Locking EEPROM...")
ser.write(build_write_packet(SERVO_ID, ADDR_LOCK, [1]))
time.sleep(0.05)

ser.close()
print("\n✓ Done! Position correction reset.")
print("\nPower cycle the servo (unplug/replug power), then test again.")