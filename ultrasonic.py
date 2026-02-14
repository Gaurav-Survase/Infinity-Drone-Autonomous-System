from dronekit import connect, VehicleMode
from pymavlink import mavutil
import time
import RPi.GPIO as GPIO

# ---------- CONNECT TO DRONE ----------
print("🔗 Connecting to drone...")
vehicle = connect('127.0.0.1:14550', wait_ready=True)
# real drone: '/dev/ttyAMA0' or telemetry port

# ---------- GPIO SETUP ----------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sensors = [
    {"trig": 23, "echo": 24},  # S1
    {"trig": 17, "echo": 27},  # S2
    {"trig": 5,  "echo": 6},   # S3
    {"trig": 12, "echo": 16},  # S4
    {"trig": 20, "echo": 21}   # S5
]

for s in sensors:
    GPIO.setup(s["trig"], GPIO.OUT)
    GPIO.setup(s["echo"], GPIO.IN)
    GPIO.output(s["trig"], False)

time.sleep(2)
print("✅ Ultrasonic ready")

# ---------- DISTANCE FUNCTION ----------
def get_distance(trig, echo):
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    start = time.time()
    stop = time.time()

    while GPIO.input(echo) == 0:
        start = time.time()

    while GPIO.input(echo) == 1:
        stop = time.time()
