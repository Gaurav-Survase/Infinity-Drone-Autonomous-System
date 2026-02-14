import time
from dronekit import connect, VehicleMode

# --- CONFIGURATION ---
# '/dev/ttyAMA0' is the standard hardware serial port on the Pi
# If this fails, try '/dev/serial0'
connection_string =  '/dev/serial0'
baud_rate = 57600

def test_connection():
    print(f"DEBUG: Attempting to connect on {connection_string}...")

    try:
        # We set a timeout so the script doesn't hang forever
        vehicle = connect(connection_string, wait_ready=True, baud=baud_rate, timeout=60)

        print("\n" + "="*30)
        print(" SUCCESS: PIXHAWK CONNECTED")
        print("="*30)

        # Pull basic data to ensure the MAVLink stream is healthy
        print(f" Firmware    : {vehicle.version}")
        print(f" GPS Status  : {vehicle.gps_0}")
        print(f" Battery     : {vehicle.battery}")
        print(f" Flight Mode : {vehicle.mode.name}")
        print("="*30)

        # Always close the connection
        vehicle.close()
        print("\nConnection closed cleanly.")

    except Exception as e:
        print("\n" + "!"*30)
        print(" CONNECTION FAILED")
        print("!"*30)
        print(f"Error Details: {e}")
        print("\nPossible fixes:")
        print("1. Check RX/TX wiring (Try swapping them).")
        print("2. Ensure Pixhawk is powered on.")
        print("3. Verify serial port is enabled in 'sudo raspi-config'.")

if __name__ == "__main__":
    test_connection()
