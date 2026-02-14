from dronekit import connect, VehicleMode
from pymavlink import mavutil
import time
# Connect to the vehicle
vehicle = connect('/dev/serial0', baud=57600, wait_ready=True, timeout = 60)

def indoor_stabilize_hop():
    vehicle.parameters['ARMING_CHECK'] = 0

    # Test if board allows GUIDED without GPS
    print("Switching to STABILIZE")
    vehicle.mode = VehicleMode("GUIDED")

    print("Arming...")
    vehicle.armed = True
    while not vehicle.armed:
         print(" Waiting for arming...")
         time.sleep(1)

    # Step 1: Small Hop
    print("Taking off (Throttle Override)...")
    vehicle.channels.overrides['3'] = 1700
    time.sleep(3)

    # Step 2: Hover
    vehicle.channels.overrides['3'] = 1600
    print("Hovering...")
    time.sleep(5)

    vehical.channel.override['3'] = ("GUIDED")
    # --- THE LANDING ---
    print("Lowering throttle to land...")
    vehicle.channels.overrides['3'] = 1200
    time.sleep(2)


    vehicle.mode = VehicleMode("LAND")
    # --- SHUTDOWN ---
    print("Disarming...")
    vehicle.channels.overrides['3'] = None # Clear overrides!
    vehicle.armed = False
    print("Test Complete.")
