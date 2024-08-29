import math
import time
from pymavlink import mavutil

def send_attitude(vehicle, time_boot_ms, roll, pitch, yaw, rollspeed, pitchspeed, yawspeed):
    """
    Send ATTITUDE message to set the attitude and rates of the drone.
    """
    try:
        # Encode the ATTITUDE message
        msg = vehicle.mav.attitude_encode(
            int(time_boot_ms),        # Timestamp in milliseconds
            roll,                     # Roll angle in radians
            pitch,                    # Pitch angle in radians
            yaw,                      # Yaw angle in radians
            rollspeed,                # Roll rate in radians/second
            pitchspeed,               # Pitch rate in radians/second
            yawspeed                  # Yaw rate in radians/second
        )
        vehicle.mav.send(msg)
        print("Attitude message sent successfully.")
    except Exception as e:
        print(f"Error sending attitude message: {e}")

def main():
    # Create a connection to the FCU
    vehicle = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
    vehicle.wait_heartbeat()
    print("Connected to the vehicle")

    while True:
        # Example attitude data
        roll = 0.0  # Roll angle in radians
        pitch = 0.0  # Pitch angle in radians
        yaw = math.radians(90)  # Yaw angle in radians
        rollspeed = 0.0  # Roll rate in radians/second
        pitchspeed = 0.0  # Pitch rate in radians/second
        yawspeed = 0.0  # Yaw rate in radians/second
        time_boot_ms = int(time.time() * 1000)  # Timestamp in milliseconds

        send_attitude(vehicle, time_boot_ms, roll, pitch, yaw, rollspeed, pitchspeed, yawspeed)
        time.sleep(1)  # Send data every second

if __name__ == "__main__":
    main()
