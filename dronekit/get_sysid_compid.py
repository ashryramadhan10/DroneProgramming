from dronekit import connect
from pymavlink import mavutil

# Connect to the vehicle
connection_string = '127.0.0.1:14550'
print(f'Connecting to vehicle on: {connection_string}')
vehicle = connect(connection_string, wait_ready=True)

# Wait for the first heartbeat to find out the sysid and compid
def get_sysid_compid(vehicle):
    master = mavutil.mavlink_connection(vehicle._handler.master.address)
    master.wait_heartbeat()
    print(f"SYSID: {master.target_system}, COMPONENTID: {master.target_component}")

# Get and print SYSID and COMPONENTID
get_sysid_compid(vehicle)

# Close vehicle connection
vehicle.close()
print("Completed")
