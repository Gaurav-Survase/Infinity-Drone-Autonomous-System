from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Connect to the vehicle
vehicle = connect('/dev/serial0', baud=57600, wait_ready=True)

def fly_to_altitude(target_altitude):
    print("Switching to mode...")
    vehicle.mode = VehicleMode("STABILIZE")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print(f"Taking off to {target_altitude} meters!")
    # THE COMMAND:
    vehicle.simple_takeoff(target_altitude)

    # Monitor the altitude
    while True:
        current_alt = vehicle.location.global_relative_frame.alt
        print(f" Current Altitude: {current_alt:.1f}m")

        # Break once we are within 5% of the target altitude
        if current_alt >= target_altitude * 0.95:
            print("Reached target altitude!")
            break
        time.sleep(1)

# Execute the command to fly at 3 meters
try:
    fly_to_altitude(2)

    # Stay there for 10 seconds
    print("Maintaining altitude...")
    time.sleep(10)

    print("Landing...")
    vehicle.mode = VehicleMode("LAND")
finally:
    vehicle.close()
