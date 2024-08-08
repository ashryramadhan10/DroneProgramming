from pymavlink import mavutil
import time

# Connect to the drone via serial
master = mavutil.mavlink_connection("127.0.0.1:14551")

master.wait_heartbeat()
print("Heartbeat received from system (system ID %d component ID %d)" % (master.target_system, master.target_component))

while True:
    # Receive the OPTICAL_FLOW message
    msg = master.recv_match(type='OPTICAL_FLOW', blocking=True)

    if msg:
        # Extract and print data from the OPTICAL_FLOW message
        print(f"Time: {msg.time_usec}")
        print(f"Flow X: {msg.flow_x} pixels/s")
        print(f"Flow Y: {msg.flow_y} pixels/s")
        print(f"Flow Rate X: {msg.flow_rate_x} rad/s")
        print(f"Flow Rate Y: {msg.flow_rate_y} rad/s")
        print(f"Quality: {msg.quality}")

    time.sleep(0.1)  # Adjust as necessary

