from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
import socket
import exceptions
import math
import argparse


def connectMyCopter():
    parser = argparse.ArgumentParser(description="commands")
    parser.add_argument("--connect")
    args = parser.parse_args()

    connection_string = args.connect
    baud_rate = 57600

    vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)
    return vehicle


def arm():
    while vehicle.is_armble == False:
        print("Waiting For vehicle to connect..")
        time.sleep(1)

    print("Ready to pair!!")
    print()
    vehicle.armed = True
    while vehicle.armed == False:
        print("Waiting to be armed..")
        time.sleep(1)

    print("Ready to Goo!!!")
    return None





print("END")s
