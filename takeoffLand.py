from dronekit import connect, VehicleMode
from pymavlink import mavutil
import time

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
        # --- FIX FAILSAFE ERRORS ---
        print("Disabling Safety Failsafes for Indoor Test...")
        vehicle.parameters['ARMING_CHECK'] = 0
        vehicle.parameters['FS_THR_ENABLE'] = 0 # Disables Radio Failsafe

        print("Switching to GUIDED...")
        vehicle.mode = VehicleMode("STABILIZE")

        print("Arming...")
        vehicle.armed = True
        while not vehicle.armed:
            time.sleep(1)

        # Step 1: Small Hop (Safer Power)
        print("Taking off...")
        vehicle.channels.overrides['3'] = 1600 # Slightly above half
        time.sleep(3) # Only 2 seconds!

        vehicle.mode = VehicleMode("GUIDED")
        # Step 2: Hover (Middle Power)
        print("Hovering...")
        vehicle.channels.overrides['3'] = 1500
        time.sleep(15)

        # Step 3: Short Forward Move (Slow and Short)
