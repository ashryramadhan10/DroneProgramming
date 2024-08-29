from pymavlink import mavutil
import time

def send_hil_gps(vehicle, time_usec, fix_type, lat, lon, alt, eph, epv, vel, vn, ve, vd, cog, satellites_visible, gps_id, yaw):
    """
    Send HIL_GPS message with simulated GPS data.

    Parameters:
    vehicle: MAVLink connection object
    time_usec: Timestamp in microseconds
    fix_type: GPS fix type (0-1: no fix, 2: 2D fix, 3: 3D fix)
    lat: Latitude in degrees * 1e7
    lon: Longitude in degrees * 1e7
    alt: Altitude in millimeters
    eph: GPS HDOP (horizontal dilution of precision) in units of 100
    epv: GPS VDOP (vertical dilution of precision) in units of 100
    vel: Ground speed in cm/s
    vn: Velocity North in cm/s
    ve: Velocity East in cm/s
    vd: Velocity Down in cm/s
    cog: Course over ground in degrees * 100
    satellites_visible: Number of satellites visible
    gps_id: GPS ID (zero indexed)
    yaw: Yaw in degrees * 100
    """
    msg = vehicle.mav.hil_gps_encode(
        time_usec,  # Timestamp in microseconds
        fix_type,  # GPS fix type
        lat,  # Latitude in degrees * 1e7
        lon,  # Longitude in degrees * 1e7
        alt,  # Altitude in millimeters
        eph,  # GPS HDOP in units of 100
        epv,  # GPS VDOP in units of 100
        vel,  # Ground speed in cm/s
        vn,  # Velocity North in cm/s
        ve,  # Velocity East in cm/s
        vd,  # Velocity Down in cm/s
        cog,  # Course over ground in degrees * 100
        satellites_visible,  # Number of satellites visible
        gps_id,  # GPS ID (zero indexed)
        yaw  # Yaw in degrees * 100
    )
    vehicle.mav.send(msg)

def main():
    # Create a connection to the FCU
    vehicle = mavutil.mavlink_connection(device="/dev/ttyACM1,115200")
    vehicle.wait_heartbeat(timeout=5)
    print("Connected to the vehicle")

    while True:
        # Example GPS data
        time_usec = int(time.time() * 1e6)  # Timestamp in microseconds
        fix_type = 3  # GPS fix type (3 = 3D fix)
        lat = int(35.084385 * 1e7)  # Latitude in degrees * 1e7
        lon = int(-106.650422 * 1e7)  # Longitude in degrees * 1e7
        alt = 585 * 1000  # Altitude in millimeters (585 meters)
        eph = 50  # Example HDOP (horizontal dilution of precision) * 100
        epv = 50  # Example VDOP (vertical dilution of precision) * 100
        vel = 1000  # Example ground speed in cm/s (10 m/s)
        vn = 0     # North velocity in cm/s
        ve = 0     # East velocity in cm/s
        vd = 0     # Down velocity in cm/s
        cog = int(90 * 100)  # Example course over ground (90 degrees * 100)
        satellites_visible = 10  # Number of satellites visible
        gps_id = 0  # GPS ID (zero indexed)
        yaw = int(90 * 100)  # Example yaw (90 degrees * 100)

        send_hil_gps(vehicle, time_usec, fix_type, lat, lon, alt, eph, epv, vel, vn, ve, vd, cog, satellites_visible, gps_id, yaw)
        time.sleep(1)  # Send data every second

if __name__ == "__main__":
    main()
