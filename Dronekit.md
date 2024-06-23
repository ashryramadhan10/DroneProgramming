# Dronekit

## 1. Observer or Listener

```python
def mode_callback(self, attribute_name, message):
    print(self.mode.name)


def parameter_callback(self, parameter_name, message):
    print(parameter_name, message)


def message_callback(self, message_name, message):
    print("Heartbeat:", self.last_heartbeat)

vehicle.add_attribute_listener("mode", mode_callback)
vehicle.parameters.add_attribute_listener("SYSID_THISMAV", parameter_callback)
vehicle.add_message_listener("HEARTBEAT", message_callback)
```

### Common Attributes in DroneKit

These are some of the frequently used attributes you can access in DroneKit:

- `location.global_frame`: The vehicle's location in global coordinates.
- `location.global_relative_frame`: The vehicle's location relative to the home position.
- `location.local_frame`: The vehicle's location in local NED (North-East-Down) frame.
- `attitude`: The vehicle's attitude (pitch, roll, yaw).
- `velocity`: The vehicle's velocity in the NED frame.
- `gps_0`: GPS information such as fix type and number of satellites.
- `battery`: Battery status including voltage, current, and level.
- `mode`: The current flight mode (e.g., "LOITER", "AUTO").
- `armed`: Boolean indicating if the vehicle is armed.
- `system_status`: The system status (e.g., "STANDBY", "ACTIVE").
- `is_armable`: Boolean indicating if the vehicle is ready to be armed.
- `heading`: The vehicle's heading in degrees.
- `groundspeed`: The vehicle's ground speed in meters per second.
- `airspeed`: The vehicle's airspeed in meters per second.
- `last_heartbeat`: Time since the last heartbeat was received.
- `ekf_ok`: Boolean indicating if the EKF (Extended Kalman Filter) is healthy.

### Common Parameters in ArduPilot

These are some of the frequently used parameters you might adjust or monitor:

- **Roll Rate Controller (ATC_RAT_RLL_*)**:
  - `ATC_RAT_RLL_P`: Roll axis rate controller proportional gain.
  - `ATC_RAT_RLL_I`: Roll axis rate controller integral gain.
  - `ATC_RAT_RLL_D`: Roll axis rate controller derivative gain.

- **Pitch Rate Controller (ATC_RAT_PIT_*)**:
  - `ATC_RAT_PIT_P`: Pitch axis rate controller proportional gain.
  - `ATC_RAT_PIT_I`: Pitch axis rate controller integral gain.
  - `ATC_RAT_PIT_D`: Pitch axis rate controller derivative gain.

- **Yaw Rate Controller (ATC_RAT_YAW_*)**:
  - `ATC_RAT_YAW_P`: Yaw axis rate controller proportional gain.
  - `ATC_RAT_YAW_I`: Yaw axis rate controller integral gain.
  - `ATC_RAT_YAW_D`: Yaw axis rate controller derivative gain.

- **Navigation Tuning (NAV_)**:
  - `NAVL1_PERIOD`: L1 navigation period.
  - `NAVL1_DAMPING`: L1 navigation damping.

- **Altitude Hold (ALT_HOLD_)**:
  - `ALT_HOLD_RTL`: Return-to-Launch altitude.
  - `ALT_HOLD_WP`: Waypoint altitude hold.

- **Arming Checks**:
  - `ARMING_CHECK`: Bitmask of pre-arm checks.

- **Battery Monitoring**:
  - `BATT_MONITOR`: Battery monitoring enable/disable.
  - `BATT_CAPACITY`: Battery capacity in mAh.

### Common MAVLink Messages

Here are some of the common MAVLink messages you might use or listen for:

- **Heartbeat**:
  - `HEARTBEAT`: Sent periodically to indicate the system is alive.

- **Command Long**:
  - `COMMAND_LONG`: Used to send various commands to the vehicle, such as arming/disarming.

- **Attitude**:
  - `ATTITUDE`: Contains the vehicle's attitude (pitch, roll, yaw).

- **Global Position**:
  - `GLOBAL_POSITION_INT`: The vehicle's global position (latitude, longitude, altitude).

- **GPS Raw**:
  - `GPS_RAW_INT`: Raw GPS data including fix type and number of satellites.

- **Battery Status**:
  - `BATTERY_STATUS`: Battery information including voltage, current, and remaining capacity.

- **System Status**:
  - `SYS_STATUS`: Contains system status information such as onboard sensors health and battery status.

- **Mission Item**:
  - `MISSION_ITEM`: Defines a mission item in the mission list.
  - `MISSION_CURRENT`: Indicates the current mission item being executed.

- **Param**:
  - `PARAM_REQUEST_READ`: Request to read a parameter.
  - `PARAM_REQUEST_LIST`: Request a list of all parameters.
  - `PARAM_SET`: Set a parameter value.
  - `PARAM_VALUE`: Contains a parameter's value.

- **Command Acknowledgement**:
  - `COMMAND_ACK`: Acknowledges the receipt of a command.

This list covers some of the most commonly used attributes, parameters, and messages. The actual set of available attributes, parameters, and messages can vary depending on the specific vehicle firmware and version you are working with. You can use tools like MAVLink Inspector (part of Mission Planner) to explore available messages and parameters for your specific setup.