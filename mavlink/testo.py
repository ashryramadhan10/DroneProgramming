from pymavlink import mavutil
import time

loop_period = 0.1  # seconds

# Create a connection to the FCU
# Replace 'udpout:localhost:14550' with the appropriate connection string for your setup
vehicle = mavutil.mavlink_connection(device="/dev/ttyACM0,115200")
# vehicle = mavutil.mavlink_connection(device="127.0.0.1:14551")

# wait for a heartbeat
vehicle.wait_heartbeat(timeout=5)

# debugging messages
print("Connected to the vehicle")
print("Target system:", vehicle.target_system, "Target component:", vehicle.target_component)

def send_gps_raw(lat,lon,alt):
    msg = vehicle.mav.gps_input_encode(
    0, # Timestamp (micros since boot or Unix epoch)
    0, # ID of the GPS for multiple GPS inputs
    # Flags indicating which fields to ignore (see GPS_INPUT_IGNORE_FLAGS enum).
    # All other fields must be provided.
    (mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_VEL_HORIZ |
    mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_VEL_VERT |
    mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_SPEED_ACCURACY) |
    mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_HORIZONTAL_ACCURACY |
    mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_VERTICAL_ACCURACY,
    0, # GPS time (milliseconds from start of GPS week)
    0, # GPS week number
    3, # 0-1: no fix, 2: 2D fix, 3: 3D fix. 4: 3D with DGPS. 5: 3D with RTK
    int(lat * 1e7), # Latitude (WGS84), in degrees * 1E7
    int(lon * 1e7), # Longitude (WGS84), in degrees * 1E7
    alt, # Altitude (AMSL, not WGS84), in m (positive for up)
    0.4, # GPS HDOP horizontal dilution of position in m
    1.4, # GPS VDOP vertical dilution of position in m
    0, # GPS velocity in m/s in NORTH direction in earth-fixed NED frame
    0, # GPS velocity in m/s in EAST direction in earth-fixed NED frame
    0, # GPS velocity in m/s in DOWN direction in earth-fixed NED frame
    0, # GPS speed accuracy in m/s
    0, # GPS horizontal accuracy in m
    0, # GPS vertical accuracy in m
    24 # Number of satellites visible.
    )
    vehicle.mav.send(msg)

while True:
    # Record the start time of the loop iteration
    start_time = time.time()

    # Call your method
    send_gps_raw(35.084385, -106.650422, 585)

    # Calculate the elapsed time since the start of the loop iteration
    elapsed_time = time.time() - start_time

    # Calculate the time to sleep to maintain 10 Hz frequency
    if elapsed_time < loop_period:
        time.sleep(loop_period - elapsed_time)
    else:
        print("Warning: Method execution took longer than loop period")
