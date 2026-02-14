from dronekit import connect, VehicleMode
import time

# Connect
vehicle = connect('/dev/serial0', baud=57600, wait_ready=True)

# 1. Write Params (Disable RC and GPS checks)
print("Writing Parameters...")
vehicle.parameters['ARMING_CHECK'] = 0
time.sleep(1) # Give the Pixhawk a second to process

# 2. Change to GUIDED mode
print("Switching to STABILIZE mode...")
vehicle.mode = VehicleMode("STABILIZE")

# 3. Arm Motors
print("Arming...")
vehicle.armed = True

# 4. Monitor
timeout = 0
while not vehicle.armed and timeout < 10:
    print(" Waiting for arming...")
    time.sleep(1)
    timeout += 1

if vehicle.armed:
    print("MOTORS ARMED! (Spinning at idle)")
    time.sleep(5)
    print("Disarming...")
    vehicle.channels.overrides['3'] = None
    time.sleep(15)
    vehicle.armed = False
else:
    print("Arming failed. Check your Pixhawk's light (Yellow = Error).")

vehicle.close()
