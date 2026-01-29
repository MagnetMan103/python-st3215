from st3215 import ST3215
import time

servo = ST3215('/dev/tty.usbmodem5A680132761')
print(servo.ReadPosition(1))
print(servo.ReadPosition(2))
print(servo.ReadPosition(4))

# 3781 (id1), 2548 (id2) 1888 (id4)
# say 3200 - 4200, and 1500 - 2500
# id 2 is hip, id1 is first joint, id 4 is second joint away
servo.MoveTo(1, 3200, wait=True)
servo.MoveTo(4, 1500, wait=True)
# servo.MoveTo(2, 2548, wait=True)
# servo.MoveTo(4, 1163, wait=True)
# 0 - 4095
# ids 1, 2, 4
# 3000 - 4095 is a good heurestic for servo 1
# Test full range
# servo.MoveTo(1, 3500, wait=True)
# time.sleep(0.5)
# pos0 = servo.ReadPosition(1)
# print(f"Commanded 0    → Actual: {pos0}")
#
# servo.MoveTo(1, 3900, wait=True)
# time.sleep(0.5)
# pos0 = servo.ReadPosition(1)
# print(f"Commanded 0    → Actual: {pos0}")


# servo.MoveTo(2, 3000, wait=True)
# time.sleep(0.5)
# pos0 = servo.ReadPosition(2)
# print(f"Commanded 0    → Actual: {pos0}")
#
# servo.MoveTo(2, 2048, wait=True)
# time.sleep(0.5)
# pos0 = servo.ReadPosition(2)
# print(f"Commanded 0    → Actual: {pos0}")

# id 4
# servo.MoveTo(4, 1500, wait=True)
# time.sleep(0.5)
# pos0 = servo.ReadPosition(4)
# print(f"Commanded 0    → Actual: {pos0}")

# servo.MoveTo(4, 2048, wait=True)
# time.sleep(0.5)
# pos0 = servo.ReadPosition(4)
# print(f"Commanded 0    → Actual: {pos0}")

