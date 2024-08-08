from pymavlink import mavutil
import time

class GPSState:
    def __init__(self):
        self.time_week = 0
        self.time_week_ms = 0
        self.status = 0
        self.location = {'lat': 0, 'lng': 0, 'alt': 0}
        self.hdop = 0
        self.vdop = 0
        self.velocity = {'vn': 0, 've': 0, 'vd': 0}
        self.ground_speed = 0
        self.ground_course = 0
        self.num_sats = 0
        self.have_vertical_velocity = False
        self.have_speed_accuracy = False
        self.have_horizontal_accuracy = False
        self.have_vertical_accuracy = False
        self.gps_yaw = 0
        self.have_gps_yaw = False
        self.gps_yaw_configured = False

def handle_gps_input(msg, state):
    packet = msg.get_payload()
    gps_id = packet.gps_id
    ignore_flags = packet.ignore_flags

    # Check if this message corresponds to the correct GPS instance
    if gps_id != 0:  # Example instance ID, replace with your condition
        return

    state.time_week = packet.time_week
    state.time_week_ms = packet.time_week_ms
    state.status = packet.fix_type

    state.location = {
        'lat': packet.lat,
        'lng': packet.lon,
        'alt': packet.alt * 0.01  # Convert to meters
    }

    if not (ignore_flags & 1):  # Check if altitude is not ignored
        state.hdop = packet.hdop * 0.01  # Convert to meters

    if not (ignore_flags & 2):  # Check if vertical dilution is not ignored
        state.vdop = packet.vdop * 0.01  # Convert to meters

    if not (ignore_flags & 4):  # Check if horizontal velocity is not ignored
        state.velocity['vn'] = packet.vn * 0.01
        state.velocity['ve'] = packet.ve * 0.01

    if not (ignore_flags & 8):  # Check if vertical velocity is not ignored
        state.velocity['vd'] = packet.vd * 0.01
        state.have_vertical_velocity = True

    state.ground_speed = packet.vel * 0.01
    state.ground_course = packet.cog * 0.01

    if packet.fix_type >= 3 and packet.time_week > 0:
        now_ms = int(time.time() * 1000)
        state.num_sats = packet.satellites_visible

    if packet.yaw != 0:
        state.gps_yaw = packet.yaw * 0.01
        state.have_gps_yaw = True
        state.gps_yaw_configured = True

def handle_hil_gps(msg, state):
    packet = msg.get_payload()

    state.time_week = 0
    state.time_week_ms = packet.time_usec / 1000
    state.status = packet.fix_type

    state.location = {
        'lat': packet.lat,
        'lng': packet.lon,
        'alt': packet.alt * 0.1  # Convert to meters
    }

    state.hdop = min(packet.eph * 0.01, 9999)
    state.vdop = min(packet.epv * 0.01, 9999)

    state.ground_speed = packet.vel * 0.01

    state.velocity = {
        'vn': packet.vn * 0.01,
        've': packet.ve * 0.01,
        'vd': packet.vd * 0.01
    }

    state.num_sats = packet.satellites_visible

    now_ms = int(time.time() * 1000)
    state.last_gps_time_ms = now_ms

def main():
    # Connect to MAVLink system (replace with your connection string)
    mav = mavutil.mavlink_connection(device="/dev/ttyACM0,115200")

    state = GPSState()

    while True:
        msg = mav.recv_match()
        if msg is None:
            continue

        if msg.get_type() == 'GPS_INPUT':
            handle_gps_input(msg, state)
        elif msg.get_type() == 'HIL_GPS':
            handle_hil_gps(msg, state)

        print(f"GPS State: {state.__dict__}")

if __name__ == "__main__":
    main()
