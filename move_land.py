from dronekit import connect, VehicleMode
from pymavlink import mavutil
import time

# Connect to the vehicle
vehicle = connect('/dev/serial0', baud=57600, wait_ready=True)

def send_body_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    velocity_x > 0: Forward / < 0: Backward
    velocity_y > 0: Right / < 0: Left
    velocity_z > 0: Down / < 0: Up
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_BODY_NED, # Relative to the drone's heading
        0b0000111111000111, # Bitmask to indicate velocity control
        0, 0, 0,
        velocity_x, velocity_y, velocity_z,
        0, 0, 0, 0, 0)

    for x in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

def stop_and_hover():
    """Brings the drone to a stop and holds position"""
    print("Stopping all movement...")
    send_body_velocity(0, 0, 0, 2)

def safe_land():
    """Initiates landing and monitors altitude until disarmed"""
    print("Initiating Safe Landing...")
    vehicle.mode = VehicleMode("LAND")

    while vehicle.armed:
        alt = vehicle.location.global_relative_frame.alt
        print(f" Descending... Current Altitude: {alt:.1f}m")
        if alt < 0.2: # Near the ground
            print("Ground reached. Waiting for disarm...")
        time.sleep(1)

    print("Vehicle Disarmed. Safety achieved.")

# --- THE MISSION ---
