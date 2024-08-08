import time
import math
from pymavlink import mavutil

# Establish MAVLink connection
master = mavutil.mavlink_connection('/dev/ttyACM0', baud=115200)

# Define the GPS and attitude data
latitude = 47.397742
longitude = 8.545594
altitude = 488.0
fix_type = 3  # 3D Fix
satellites_visible = 5
hdop = 0.8  # Horizontal Dilution of Precision
vdop = 0.8  # Vertical Dilution of Precision

def calculate_yaw_from_degrees(yaw_deg):
    """Convert yaw from degrees to radians."""
    return math.radians(yaw_deg)

while True:
    # Example GPS data (replace with actual data from your GPS)
    vn = 10  # Velocity in North direction (cm/s)
    ve = 20  # Velocity in East direction (cm/s)

    # Calculate yaw from GPS data if needed, or set it directly
    desired_yaw_deg = 300  # Desired yaw in degrees
    yaw_rad = calculate_yaw_from_degrees(desired_yaw_deg)
    
    # Convert yaw to centidegrees for debugging (if needed)
    yaw_cdeg = int(75 * 100)
    
    # Correct the time_boot_ms to fit within uint32_t range
    time_boot_ms = int(time.time() * 1000) % 4294967296
    
    # Send HIL_GPS message
    master.mav.hil_gps_send(
        time_usec=int(time.time() * 1e6),
        fix_type=fix_type,
        lat=int(latitude * 1e7),
        lon=int(longitude * 1e7),
        alt=int(altitude * 1e3),  # Convert to mm
        eph=int(hdop * 100),  # Convert HDOP to integer
        epv=int(vdop * 100),  # Convert VDOP to integer
        vel=0,  # GPS speed in cm/s (0 if unknown)
        vn=vn,  # GPS velocity in north direction in cm/s
        ve=ve,  # GPS velocity in east direction in cm/s
        vd=0,  # GPS velocity in down direction in cm/s (0 if unknown)
        cog=yaw_cdeg,  # Course over ground in centidegrees
        satellites_visible=satellites_visible
    )
    
    # Debug: print values to ensure they are within expected ranges
    print(f"time_boot_ms: {time_boot_ms}")
    print(f"roll: {0.0}, pitch: {0.0}, yaw: {yaw_rad}")
    print(f"rollspeed: {0.0}, pitchspeed: {0.0}, yawspeed: {0.0}")
    
    # Send ATTITUDE message
    master.mav.attitude_send(
        time_boot_ms=time_boot_ms,  # Corrected Time in milliseconds
        roll=0.0,  # Roll in radians
        pitch=0.0,  # Pitch in radians
        yaw=yaw_rad,  # Yaw in radians
        rollspeed=0.0,  # Roll rate in radians/second
        pitchspeed=0.0,  # Pitch rate in radians/second
        yawspeed=0.0  # Yaw rate in radians/second
    )
    
    # Send data at a regular interval
    time.sleep(0.1)
