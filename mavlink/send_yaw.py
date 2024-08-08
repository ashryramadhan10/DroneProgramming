import time
import math
from pymavlink import mavutil

# Connect to the FCU
def connect_fcu(connection_string):
    return mavutil.mavlink_connection(connection_string)

# Send attitude data (roll, pitch, yaw) to the FCU
def send_attitude(master, roll, pitch, yaw):
    # Get current time in milliseconds and ensure it fits within the valid range
    timestamp = int(time.time() * 1000) % 4294967296
    
    master.mav.attitude_send(
        timestamp,  # Timestamp in milliseconds
        roll,       # Roll in radians
        pitch,      # Pitch in radians
        yaw,        # Yaw in radians
        0,          # Roll rate in radians/second
        0,          # Pitch rate in radians/second
        0           # Yaw rate in radians/second
    )
    print(f"Sent attitude: roll={roll}, pitch={pitch}, yaw={yaw}")

# Send GPS raw data
def send_gps_raw(master, lat, lon, alt):
    msg = master.mav.gps_input_encode(
        0,  # Timestamp (micros since boot or Unix epoch)
        0,  # ID of the GPS for multiple GPS inputs
        (mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_VEL_HORIZ |
         mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_VEL_VERT |
         mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_SPEED_ACCURACY |
         mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_HORIZONTAL_ACCURACY |
         mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_VERTICAL_ACCURACY),
        0,  # GPS time (milliseconds from start of GPS week)
        0,  # GPS week number
        3,  # Fix type: 0-1: no fix, 2: 2D fix, 3: 3D fix, 4: 3D with DGPS, 5: 3D with RTK
        int(lat * 1e7),  # Latitude (WGS84), in degrees * 1E7
        int(lon * 1e7),  # Longitude (WGS84), in degrees * 1E7
        alt,  # Altitude (AMSL, not WGS84), in meters (positive for up)
        0.4,  # GPS HDOP (horizontal dilution of position) in meters
        1.4,  # GPS VDOP (vertical dilution of position) in meters
        0,    # GPS velocity in m/s (North direction)
        0,    # GPS velocity in m/s (East direction)
        0,    # GPS velocity in m/s (Down direction)
        0,    # GPS speed accuracy in m/s
        0,    # GPS horizontal accuracy in meters
        0,    # GPS vertical accuracy in meters
        24    # Number of satellites visible
    )
    master.mav.send(msg)

# Main function to send attitude and GPS data
def main():
    # Adjust the connection string as needed
    connection_string = '/dev/ttyACM0,115200'  # For serial port connection
    # For UDP connection, use:
    # connection_string = 'udp:127.0.0.1:14550'
    
    # Connect to the FCU
    master = connect_fcu(connection_string)
    
    # Set baudrate if needed (e.g., 115200 for serial)
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        0  # Set mode to GUIDED for example
    )
    
    roll = 0.0  # Roll in radians
    pitch = 0.0  # Pitch in radians
    yaw = 0.0  # Initial yaw in radians

    while True:
        # Increment yaw
        yaw += 0.01  # Change this value to adjust the rate of yaw change
        if yaw > 2 * math.pi:  # Wrap yaw within 0 to 2*pi
            yaw -= 2 * math.pi
        
        # Send updated attitude
        send_attitude(master, roll, pitch, yaw)
        
        # Send GPS data
        send_gps_raw(master, 35.084385, -106.650422, 585)
        
        # Sleep for a short interval before sending the next update
        time.sleep(0.1)  # Adjust the interval as needed

if __name__ == "__main__":
    main()
