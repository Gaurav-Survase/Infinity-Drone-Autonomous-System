from dronekit import connect, VehicleMode
import time

vehicle = connect('/dev/serial0', baud=57600, wait_ready=True)

def motor_spin_15_seconds():
    print("Pre-test safety setup...")
    vehicle.parameters['ARMING_CHECK'] = 0

    # We use STABILIZE for bench testing
    vehicle.mode = VehicleMode("STABILIZE")

    print("Arming...")
    vehicle.armed = True
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("!!! MOTORS ARMED - STARTING 15 SEC TIMER !!!")

    # Start the timer
    start_time = time.time()

    while time.time() - start_time < 15:
        # Check if it accidentally disarmed and re-arm if needed
        if not vehicle.armed:
            print("Auto-disarm detected! Re-arming...")
            vehicle.armed = True

        # 1150 is high enough to prevent 'ground disarm' but low enough to be safe
        vehicle.channels.overrides['3'] = 1150

        remaining = 15 - (time.time() - start_time)
        print(f" Spinning... {remaining:.1f} seconds left")

        time.sleep(1) # Send the heartbeat every second

    # Clean up
    print("Timer finished. Disarming...")
    vehicle.channels.overrides['3'] = None
    vehicle.armed = False
    print("Test Complete.")
