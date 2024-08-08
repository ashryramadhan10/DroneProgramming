import time
from pymavlink import mavutil

# Create the connection (udpout for sending, `udpin` for receiving), MavLink v2 by default
master = mavutil.mavlink_connection(device="/dev/ttyACM0,115200")

# wait for a heartbeat
master.wait_heartbeat(timeout=5)

# debugging messages
print("Connected to the master")
print("Target system:", master.target_system, "Target component:", master.target_component)

# We dont wait for 'hearbeat' from Ground Control Station (GCS) here

# NOTE: 'MAV_MODE_MANUAL_ARMED' and 'MAV_STATE_ACTIVE' 
# important here, otherwise QGroundControl will not show 'Connected' 
# state, but still receive data (spotted in 'MAVLink Inspector' tab).
def send_heartbeat():
    master.mav.heartbeat_send(
        mavutil.mavlink.MAV_TYPE_QUADROTOR,    # Type of the MAV
        mavutil.mavlink.MAV_AUTOPILOT_GENERIC, # Autopilot type
        mavutil.mavlink.MAV_MODE_MANUAL_ARMED, # Base mode (manual and armed)
        0,                                     # Custom mode
        mavutil.mavlink.MAV_STATE_ACTIVE       # System status (active)
    )

def send_attitude(roll, pitch, yaw, rollspeed, pitchspeed, yawspeed):
    master.mav.attitude_send(
        int(time.time() * 1000) & 0xFFFFFFFF,  # time_boot_ms (convert to ms and wrap around to fit 32-bit)
        roll, pitch, yaw,               # radians
        rollspeed, pitchspeed, yawspeed # radians/s
    )

def send_gps(lat, lon, alt, fix_type=3):
    master.mav.gps_raw_int_send(
        int(time.time() * 1000),  # time_boot_ms
        fix_type,                 # GPS fix type
        lat, lon, alt,            # latitude, longitude, altitude
        0,                    # eph (position uncertainty)
        0,                    # epv (altitude uncertainty)
        0,                    # velocity (cm/s)
        0,                    # course over ground (degrees * 100)
        10,                      # num satellites visible
    )

def send_vfr_hud(airspeed, groundspeed, heading, throttle, alt, climb):
    master.mav.vfr_hud_send(
        airspeed, groundspeed, heading, throttle, alt, climb
    )

def send_sys_status():
    master.mav.sys_status_send(
        0,      # onboard_control_sensors_present
        0,      # onboard_control_sensors_enabled
        0,      # onboard_control_sensors_health
        500,    # load
        12000,  # voltage_battery
        -1,     # current_battery
        -1,     # battery_remaining
        0,      # drop_rate_comm
        0,      # errors_comm
        0,      # errors_count1
        0,      # errors_count2
        0,      # errors_count3
        0,      # errors_count4
    )

while True:
    send_heartbeat()
    send_attitude(0, 0, 90, 0, 0, 0)
    send_gps(473566000, 851234567, 500000)
    send_vfr_hud(0, 0, 0, 50, 50, 0)
    send_sys_status()

    time.sleep(1)
    print("successfully sent hil gps input")