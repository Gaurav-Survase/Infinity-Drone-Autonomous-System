from dronekit import connect, VehicleMode
from pymavlink import mavutil
import time

# Connection with a longer timeout to avoid that error you saw
vehicle = connect('/dev/serial0', baud=57600, wait_ready=True, timeout=60)

def send_body_velocity(velocity_x, velocity_y, velocity_z, duration):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_BODY_NED,
        0b0000111111000111,
        0, 0, 0,
        velocity_x, velocity_y, velocity_z,
        0, 0, 0, 0, 0)
    for x in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

def indoor_test():
    try:
        vehicle.parameters['ARMING_CHECK'] = 0

        # Test if board allows GUIDED without GPS
        print("Switching to GUIDED...")
        vehicle.mode = VehicleMode("GUIDED")

        print("Arming...")
        vehicle.armed = True
        while not vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        # Step 1: Small Hop
        print("Taking off (Throttle Override)...")
        vehicle.channels.overrides['3'] = 1800
        time.sleep(10)

        # Step 2: Hover
        vehicle.channels.overrides['3'] = 2000
        print("Hovering...")
        time.sleep(10)

        # Step 3: Short Forward Move
        print("Moving Forward (2 seconds)...")
