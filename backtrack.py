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

    return [velocity_x, velocity_y, velocity_z, duration]

def back_track(path_stack):

    while (len(last_pos) -1 ) != (-1):
        last_pos = len(path_stack) - 1
        # For Velocity X
        if last_pos[0] < 0:
            last_pos[0] = ~last_pos[0]
        elif last_pos[0] > 0:
            last_pos[0] = ~last_pos[0]
        else:
            pass

        # For Velocity Y
        if last_pos[1] < 0:
            last_pos[1] = ~last_pos[1]
        elif last_pos[0] > 0:
            last_pos[1] = ~last_pos[1]
        else:
            pass

        # For Velocity Z
        if last_pos[2] < 0:
