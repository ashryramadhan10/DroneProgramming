# DroneProgramming

## 1. Ardupilot Installation

Follow this instructions: [https://ardupilot.org/dev/docs/building-setup-linux.html](https://ardupilot.org/dev/docs/building-setup-linux.html)

## 2. Simulation Test

* Step-1:

`cd && cd ardupilot/ArduCopter/`

* Step-2:

Start the simulation with wiping the virtual EEPROM option to load correct parameters.

`sim_vehicle.py -w`

* Step-3:

After simulation has started, press Ctrl+C and start the simulation normally.

`sim_vehicle.py --console --map`

## 3. Simulation Environment Creation

* Step-1:

```console
sudo chmod u+x quickstart.sh
./quickstart.sh
```

* Step-2:

Run this inside `~/ardu-sim/` directory
```console
./ardu-sim.sh
screen -r
mavproxy.py --master 127.0.0.1:14550 --console --map
killall screen
```

## 3. Startup Options

1. `--master:X` specifies connection address to your vehicle. It could be one of the followings:
   1. `/dev/ttyUSBX` for Linux and `COMX` for Windows serial connections. To check `tty` use `dmesg | grep tty`
   2. `tcp:IP:PORT` for local TCP connections.
   3. `udp:IP:PORT` or just `IP:PORT` for local UDP connections.
   4. `tcpout:IP:PORT` for remote TCP connections.
   5. `udpout:IP:PORT` for remote UDP connections.
   6. Multiple master connection can be defined to the same vehicle for redundant data links.
2. If master is a serial connection, baud rate can be specified as:
   1. `--baudrate=X` or 
   2. `--master=Y,X` where X is the baud rate.
3. `--console` opens the MAVProxy ground control station Console.
4. `--map` opens the interactive map interface.
5. `--quadcopter` is used for quadcopter controls.
6. `--out` is used to forward the MAVLink packets to a remote device (serial, USB or network address/port). Useful if using multiple ground station computers or relaying the stream through an intermediate node.
   1. `/dev/ttyUSBX` for Linux and `COMX` for Windows serial connections.
   2. `tcp:IP:PORT` for local TCP connections.
   3. `udp:IP:PORT` or just `IP:PORT` for local UDP connections.
   4. `tcpout:IP:PORT` for remote TCP connections.
   5. `udpout:IP:PORT` for remote UDP connections.
   6. Multiple stream outputs can be defined.
7. `--sitl` is used to host and port to send simulated RC input for the Software in the loop (SITL) simulator. 
   1. Usually `--sitl=127.0.0.1:5501`.
8. `--streamrate` is used to configure the stream rate of the connection.
9. `--source-system` defines system ID of this GCS.
10. `--source-component` defines component ID of this GCS.
11. `--target-system` defines target master system ID.
12. `--target-component` defines target master component ID.
13. `--logfile` defines the master logfile name.
14. `--append-log` used to append new logs to the older one.
15. `--nodtr` disables DTR drop on close.
16. `--show-errors` used to show MAVLink error messages.
17. `--speech` enables text to speech.
18. `--aircraft` name of the aircraft being flown. If used, logfiles will be stored in `/Logs/AircraftName/Date/flightNumber/flight.tlog`. 
19. `--cmd` initial commands to run in MAVProxy and delimited by `;`.
20. `--load-module` loads a desired MAVProxy module on startup.
21. `--mavversion` specifies the MAVLink version.
22. `--auto-protocol` used to auto detect MAVLink protocol version.
23. `--continue` continue to the logs.
24. `--nowait` used for not waiting a heartbeat message at startup.
25. `--dialect` used to specify MAVLink dialect. Uses the APM dialect by default.
26. `--rtscts` used for RTS/CTS hardware flow control of master connection.
27. `--mission` used to give the current mission a name. If used, the flight log will be stored as `/Logs/aircraftname/missionname` rather than the default `/Logs/aircraftname/currentdatetime`.
28. `--daemon` used to start MAVProxy in daemon mode (as a background process). No interactive shell will be started.
29. `--state-basedir` defines the base directory that logs will be stored, if it is not the current directory.
30. `--version` show current MAVProxy version.
31. `--moddebug` is debugging messages level. Default is 0 (no debug output). A value of 3 is useful for debugging crashes or errors in MAVProxy and its modules.
32. `--default-modules` is a comma separated list of the modules to load on startup by default.
33. `--non-interactive` is used for not starting interactive shell.
34. `--force-connected` is used for using master even if initial connection fails.

[Source](https://ardupilot.org/mavproxy/docs/getting_started/starting.html)

## 4. MaxProxy Commands

### 4.1. Set Throttle to Neutral

```console
rc 3 1000
```

In MAVProxy, you can send RC (radio control) commands using the `rc` command. This allows you to simulate RC input to your flight controller, which is useful for testing and automation purposes.

The `rc` command in MAVProxy is used to send RC channel values to the flight controller. The format for the `rc` command is:

```sh
rc [channel] [value]
```

- `channel`: The RC channel number (1 to 16).
- `value`: The PWM value for the channel (typically between 1000 and 2000).
---
**Step-by-Step Examples:**

1. **Start MAVProxy:**
   Start MAVProxy and connect to your flight controller. Replace the connection string as necessary.

   ```sh
   mavproxy.py --master=udp:127.0.0.1:14550
   ```

2. **Send RC Commands:**
   Use the `rc` command to send RC inputs to the flight controller.

   - **Set Throttle (Channel 3) to 1500:**

     ```sh
     rc 3 1500
     ```

   - **Set Roll (Channel 1) to 1200:**

     ```sh
     rc 1 1200
     ```

   - **Set Pitch (Channel 2) to 1700:**

     ```sh
     rc 2 1700
     ```

   - **Set Yaw (Channel 4) to 1600:**

     ```sh
     rc 4 1600
     ```

3. **Reset RC Channels:**
   To reset all RC channels to their default values (typically 1500), use the `rc reset` command:

   ```sh
   rc reset
   ```

---

**Combining RC Commands in Scripts:**

You can also combine multiple RC commands into a script file and execute it within MAVProxy. This is useful for automating complex RC input sequences.

1. **Create a Script File (e.g., `rc_commands.txt`):**

   ```plaintext
   rc 3 1500
   rc 1 1200
   rc 2 1700
   rc 4 1600
   ```

2. **Load and Execute the Script in MAVProxy:**

   ```sh
   script rc_commands.txt
   ```

### 4.2. Load Module

```console
module load message
```

`message` module is used to run `MAVLink` `COMMAND_LONG` and `COMMAND_INT`.

e.g:

**MAV_CMD_DO_SET_HOME(179)** to set home
```console
module load message
message COMMAND_LONG 0 0 179 0 0 0 0 0 -35.363 149.165 575
```

### 4.3. Hardware Safety Switch

```console
arm safetyon
arm safetyoff
```

### 4.4. Arming-Disarming

```console
arm throttle
disarm
```

:warning: If you arm the vehicle and do nothing it automatically disarms after `DISARM_DELAY` seconds.

To show disarm delay parameter `param show DISARM_DELAY`.

To set disarm delay parameter to 10 seconds 

```console
param set DISARM_DELAY 10
```

### 4.5. Mode

```console
mode guided
```

## 5. Mission Editor

```console
mavproxy.py --master=127.0.0.1:14550 --console --map
module load misseditor
```

After adding some waypoints, add them by clicking `Write WPs`

Mission editor also has some useful terminal commands:
   1. `wp clear` clear mission items.
   2. `wp ftp` fetches mission item list from vehicle using FTP and saves it to `way.txt`.
   3. `wp ftpload FILE_NAME` sends mission item list to vehicle using FTP.
   4. `wp list` fetches mission item list from vehicle.
   5. `wp load FILE_NAME` sends mission item list to vehicle.
   6. `wp save FILE_NAME` saves mission item list to `FILE_NAME`.
   7. Note: 0-th waypoint is home location.

To start a mission (without radio):

`arm throttle`
`mode auto`
`long MAV_CMD_MISSION_START 0 0 0 0 0 0 0 0`

## 6. GeoFence

Geofences help you to create virtual boundary radius and height of the drone.

1. ArduPilot supports fences to allow your vehicle to only fly at certain areas.
2. Start the MAVProxy using `mavproxy.py --master=127.0.0.1:14550 --console --map`.
3. To enable fences, `param set FENCE_ENABLE 1` or `fence enable`.
4. To disable fences, `param set FENCE_ENABLE 0` or `fence disable`.
5. `FENCE_TYPE` is a bitmask parameter and used to which fence types will be used.
   1. By default, `7`, maximum altitude, circle, and polygon fences are enabled.
   2. To enable minimum altitude, do `param set FENCE_TYPE 15`, and also set minimum altitude
   like `param set FENCE_ALT_MIN 10` but with doing this, vehicle can't take off if 
   `FENCE_ALT_MIN` is greater than zero. So for takeoff, `fence disable` must be done.
6. By default, there is a cylindrical fence centered at home location with minimum and maximum altitudes.
   1. Radius can be set using `param set FENCE_RADIUS 300`. By doing that vehicle can't go further than 300 meters.
   2. Maximum altitude can be set using `param set FENCE_ALT_MAX 50`. By doing that vehicle can't fly higher than 50 meters.
   3. Minimum altitude can also be set using `param set FENCE_ALT_MIN 10` but `param set FENCE_TYPE 15` must be done. By doing that
   vehicle can't go lower than 10 meters.
7. By default, vehicle do RTL when breaches fence but behavior can be set using `FENCE_ACTION`.
8. If you want to disable user input during landing, `param set LAND_REPOSITION 0`

[Source](https://ardupilot.org/copter/docs/parameters.html#fence-parameters)

## 7. Rally Points

Rally point is a safe place for landing in case the HOME is way too far.

1. Start the MAVProxy using `mavproxy.py --master=127.0.0.1:14550 --console --map`.
2. `param set RALLY_LIMIT_KM 0` to use the closest rally point.
3. Rally points have terminal commands:
   1. `rally list` is used to list rally points on flight controller.
   2. `rally load FILE_NAME` loads rally points from a file to flight controller.
   3. `rally save FILE_NAME` saves rally points from flight controller to a file.
   4. `rally clear` deletes all rally points from flight controller.
   5. `rally add` is used to add rally point to the clicked location on map.
   6. `rally remove INDEX` is used to remove a rally points listed at a specific index.
   7. `set rallyalt 50` sets default rally point altitude to 50 meters.

## 8. Command Int

1. Int command enables user to send [MAV_CMD_*](https://mavlink.io/en/messages/common.html#mav_commands) commands to vehicle.
2. It is used to send [COMMAND_INT](https://mavlink.io/en/messages/common.html#COMMAND_INT) messages to the vehicle to
give commands during flight.
3. It uses [command](https://mavlink.io/en/services/command.html) service of the MAVLink.
4. Usage is: `command_int FRAME_TYPE COMMAND_NAME CURRENT AUTOCONTINUE PARAM1 PARAM2 PARAM3 PARAM4 X Y Z`
5. [Frame type](https://mavlink.io/en/messages/common.html#MAV_FRAME) and [command name](https://mavlink.io/en/messages/common.html#mav_commands) 
must be specified.
6. PARAM1-4 and Z are float, X and Y are int32.
7. Lets fly to a location in guided mode using [MAV_CMD_DO_REPOSITION](https://mavlink.io/en/messages/common.html#MAV_CMD_DO_REPOSITION):
   1. `command_int MAV_FRAME_GLOBAL_RELATIVE_ALT_INT MAV_CMD_DO_REPOSITION 0 0 0 0 0 0 -353613322 1491611469 10`
   2. This command needs altitude in meters as its 7th parameter.
   3. 5th, 6th parameters are latitude, longitude and they must be integers (lat\*1e7, lon\*1e7)
8. Not all the commands are supported in `COMMAND_INT` form but will be implemented and supported near future.

[Source](https://mavlink.io/en/messages/common.html#COMMAND_INT)

### 8.1. `current` Parameter

The `current` parameter in the `COMMAND_INT` message specifies whether the command being sent is to be treated as the currently active mission item for immediate execution or simply as part of a mission list to be executed later.

- **`0`: Part of the Mission List**
  - When `current` is set to `0`, the command is added to the list of mission items but is not executed immediately. This is used when you are uploading a series of waypoints or commands to be executed sequentially during the mission.
  
- **`1`: Current Mission Item**
  - When `current` is set to `1`, the command is marked as the active mission item and is executed immediately by the drone. This typically means the drone will start performing the action associated with this command right away.

### 8.2. `autocontinue` Parameter

The `autocontinue` parameter controls whether the drone should automatically move to the next mission item after completing the current one.

- **`0`: Do Not Automatically Continue**
  - The drone will complete the current mission item and then stop, waiting for further instructions.

- **`1`: Automatically Continue**
  - The drone will complete the current mission item and immediately proceed to the next mission item in the list.

### 8.2. Demonstration

```console
> command_int MAV_FRAME_GLOBAL_RELATIVE_ALT_INT MAV_CMD_DO_REPOSITION 1 0 0 0 0 0 -353613322 1491611469 10
```

## 9. System Command

1. Connect to the vehicle using: `mavproxy.py --master=127.0.0.1:14550`
2. `reboot` command is used to soft restart flight controller.
3. `time` is used to show time on flight controller and computer.
4. `script SCRIPT_FILE_NAME.EXTENSION` is used to run a text file contains MAVProxy commands.
5. `shell` is used to run a shell command.
6. `status` command shows the latest packets.
7. `watch MESSAGE_NAME` is used to watch an updating message.
8. `exit` is used to exit from MAVProxy. `set requireexit True` enables this command.

[Source](https://ardupilot.org/mavproxy/docs/uav_configuration/system.html)

## 10. Log Module

1. Connect to the vehicle using: `mavproxy.py --master=127.0.0.1:14550`
2. Load the module using: `module load log`
3. Display help screen: `log help`
4. List on-board data flash logs: `log list`
5. Download logs: `log download X Y` where `X` is the log index and `Y` is the filename to be saved as *.bin.
6. Erase on-board logs: `log erase`
7. Resume log downloading: `log resume`
8. Show log download status: `log status`
9. Abort downloading logs: `log cancel`

[Source](https://ardupilot.org/mavproxy/docs/modules/log.html)

## 11. Graph Module

1. Graph module plots live data from vehicle for monitoring vehicle state.
2. Connect to the vehicle using `mavproxy.py --master=127.0.0.1:14550`.
3. After starting MAVProxy `module load graph`.
4. `graph MESSAGE_NAME.FIELD_NAME` is used to graph specific data field.
5. Multiple data can be plotted to the same graph as:
   1. `graph MESSAGE_NAME1.FIELD_NAME1 MESSAGE_NAME2.FIELD_NAME2 MESSAGE_NAME3.FIELD_NAME3`.
6. `graph legend MESSAGE_NAME1.FIELD_NAME1 LEGEND_NAME` is used to add legend to graph.
7. Use `graph timespan X` to change the time space to X seconds on axis-x.
8. Use `graph tickresolution X` to change the tick resolution to X seconds on axis-x.
9. Mathematical operations are allowed in data.
10. Multiple graphs are allowed.
11. Let's plot altitude using [VFR_HUD](https://mavlink.io/en/messages/common.html):
    1. `graph legend (VFR_HUD.alt-584) "Relative Altitude"`
    2. `graph (VFR_HUD.alt-584)`
12. Let's plot relative altitude using [GLOBAL_POSITION_INT](https://mavlink.io/en/messages/common.html#GLOBAL_POSITION_INT)
    1. `graph legend (GLOBAL_POSITION_INT.relative_alt/1000.0) "Relative Altitude"`
    2. `graph (GLOBAL_POSITION_INT.relative_alt/1000.0)`
13. Let's plot [VIBRATION](https://mavlink.io/en/messages/common.html#VIBRATION) on all axes:
    1. `graph legend VIBRATION.vibration_x "Vibration on X axis"`
    2. `graph legend VIBRATION.vibration_y "Vibration on Y axis"`
    3. `graph legend VIBRATION.vibration_z "Vibration on Z axis"`
    4. `graph VIBRATION.vibration_x VIBRATION.vibration_y VIBRATION.vibration_z`
14. Homework:
    1. Takeoff to 10 meters.
    2. Fly to a location in GUIDED mode on 10 meters and observe the graphs.
    3. On different graphs plot:
       1. Desired roll vs. roll
       2. Desired pitch vs. pitch
       3. Desired yaw vs. yaw
    4. Each plots must be in float degrees.
    5. Add legend to all the graphs before plotting (like specified in 3rd step).
    6. Set time span to 10 seconds before plotting.
    7. Set tick resolution to 0.1 seconds before plotting.
    8. Hint: [NAV_CONTROLLER_OUTPUT](https://mavlink.io/en/messages/common.html#NAV_CONTROLLER_OUTPUT), 
[ATTITUDE](https://mavlink.io/en/messages/common.html#ATTITUDE)

---

1. **AHRS (Attitude and Heading Reference System)**:
   - AHRS provides data related to the orientation of the drone, including:
     - `AHRS.Roll`
     - `AHRS.Pitch`
     - `AHRS.Yaw`
   
   Example command to graph AHRS data:
   ```
   graph AHRS.Roll AHRS.Pitch AHRS.Yaw
   ```

2. **VFR_HUD (Vertical Flight Reference - Head-Up Display)**:
   - VFR_HUD provides essential flight parameters:
     - `VFR_HUD.Alt` (Altitude)
     - `VFR_HUD.Airspeed` (Airspeed)
     - `VFR_HUD.Heading` (Heading)
     - `VFR_HUD.Throttle` (Throttle percentage)
   
   Example command to graph VFR_HUD data:
   ```
   graph VFR_HUD.Alt VFR_HUD.Airspeed VFR_HUD.Heading VFR_HUD.Throttle
   ```

3. **GPS (Global Positioning System)**:
   - GPS data provides geographical position information:
     - `GPS.Lat` (Latitude)
     - `GPS.Lng` (Longitude)
     - `GPS.Alt` (Altitude above sea level)
   
   Example command to graph GPS data:
   ```
   graph GPS.Lat GPS.Lng GPS.Alt
   ```

4. **RCOU (RC Output)**:
   - RCOU provides information about RC channel outputs, including throttle and other control outputs:
     - `RCOU.Chan1` (Channel 1 output)
     - `RCOU.Chan2` (Channel 2 output)
     - ...

   Example command to graph RCOU data:
   ```
   graph RCOU.Chan1 RCOU.Chan2 ...
   ```

5. **BAT (Battery Status)**:
   - BAT provides information about the battery status:
     - `BAT.Volt` (Battery voltage)
     - `BAT.Curr` (Battery current)
     - `BAT.Remaining` (Remaining battery percentage)

   Example command to graph BAT data:
   ```
   graph BAT.Volt BAT.Curr BAT.Remaining
   ```

6. **SYS_STATUS (System Status)**:
   - SYS_STATUS provides overall system status information:
     - `SYS_STATUS.Load` (System load)
     - `SYS_STATUS.Voltage` (Main voltage)
     - `SYS_STATUS.Current` (Main current)
     - `SYS_STATUS.CPU` (CPU usage)

   Example command to graph SYS_STATUS data:
   ```
   graph SYS_STATUS.Load SYS_STATUS.Voltage SYS_STATUS.Current SYS_STATUS.CPU
   ```

These are just examples of common fields you might want to graph using MAVProxy's graph module. Replace the specific field names (`AHRS.Roll`, `VFR_HUD.Alt`, etc.) with the exact field names as provided by your drone's telemetry system. This will allow you to visualize and monitor these parameters in real-time during your drone operations. Adjust the graphing commands based on your specific needs and the telemetry data available from your drone system.

[Source](https://ardupilot.org/mavproxy/docs/modules/graph.html)

## 12. Horizon Module

1. Connect to the vehicle using `mavproxy.py --master=127.0.0.1:14550 --load-module="horizon,map,console"`.
2. Or after starting MAVProxy, `module load MODULE_NAME`, ex: `module load horizon`.
3. Let's take off the vehicle to the 50 meters:
   1. `mode GUIDED`
   2. `arm throttle`
   3. `takeoff 50`
4. Let's get back our vehicle to the ground using `mode LAND`.
5. Let's fly to a location in GUIDED mode using `guided -35.36217477 149.16507393 50`.
6. Let's change the mode to LOITER using `mode LOITER`.
7. By using `rc X Y`, MAVProxy periodically send RC Override to channel X with Y PWM value.
   1. `rc 1 X` overrides roll PWM with X value. 
      1. `X>1500` means roll right.
      2. `X<1500` means roll left.
      3. `X=1500` means no roll but still send RC Roll Override message.
   2. `rc 2 X` overrides pitch PWM with X value.
      1. `X>1500` means pitch backward.
      2. `X<1500` means pitch forward.
      3. `X=1500` means no pitch but still send RC Pitch Override message.
   3. `rc 3 X` overrides throttle PWM with X value.
      1. `X>1500` means gain altitude in LOITER mode.
      2. `X<1500` means lower altitude in LOITER mode.
      3. `X=1500` means maintain altitude in LOITER mode.
   4. `rc 4 X` overrides yaw PWM with X value.
      1. `X>1500` means yaw clockwise.
      2. `X<1500` means yaw counter-clockwise.
      3. `X=1500` means no yaw but still send RC Yaw Override message.
8. In GUIDED mode, copter can process RC Yaw Override message.

## 13. Link Management

1. Start using: `mavproxy.py`
2. Show link statistics: `link`
3. Display link help screen: `link help`
4. List existing links: `link list`
5. Add a link to autopilot: `link add X:Y` where `X` is connection string and `Y` is an optional label.
   1. `X` is the connection string and covered before in [here](mavproxy-quickstart.md).
   2. `Y` is the label to make the link memorable, example label: `{"label":"your_link_name"}`
   3. Before adding a serial link run the command `set baudrate X` where `X` in the baud rate value.
6. Remove a link using: `link remove X` where `X` can be the link index or label.
7. Start high latency mode: `link hl on`
8. Stop high latency mode: `link hl off`
9. Reset statistics: `link resetstats`
10. Show output count: `output`
11. Display output help screen: `output help`
12. Add an output to an endpoint: `output add X` where `X` is connection string.
    1. Connection strings are covered before in [here](mavproxy-quickstart.md).
13. List existing outputs: `output list`
14. Remove an output using: `output remove X` where `X` is the output index.

[Source](https://ardupilot.org/mavproxy/docs/modules/link.html)

## 14. Long Command

1. Long command enables user to send [MAV_CMD_*](https://mavlink.io/en/messages/common.html#mav_commands) commands to vehicle.
2. It is used to send [COMMAND_LONG](https://mavlink.io/en/messages/common.html#COMMAND_LONG) messages to the vehicle to
give commands during flight.
3. All the parameters are in float.
4. It uses [command](https://mavlink.io/en/services/command.html) service of the MAVLink.
5. Usage is: `long COMMAND_NAME PARAM1 PARAM2 PARAM3 PARAM4 PARAM5 PARAM6 PARAM7`
6. Lets takeoff in guided mode using [MAV_CMD_NAV_TAKEOFF](https://mavlink.io/en/messages/common.html#MAV_CMD_NAV_TAKEOFF):
   1. `long MAV_CMD_NAV_TAKEOFF 0 0 0 0 0 0 10`
   2. This command needs takeoff altitude in meters as its 7th parameter.
7. Not all the commands are supported in `COMMAND_LONG` form but will be implemented and supported near future.

[Source](https://mavlink.io/en/messages/common.html#COMMAND_LONG)

## 15. Map Module

Connect to the vehicle using one of the following:
1. `mavproxy.py --master=127.0.0.1:14550 --map`.
2. `mavproxy.py --master=127.0.0.1:14550 --load-module="map"`
3. `mavproxy.py --master=127.0.0.1:14550` and then `module load map`

## 16. Position Command

1. Start the MAVProxy using `mavproxy.py --master=127.0.0.1:14550 --console --map`.
2. Position command in MAVProxy is used to move the vehicle relative to current location and heading.
3. Usage: `position x y z`
   1. Positive `x` means move `x` meters forward.
   2. Negative `x` means move `x` meters backward.
   3. Positive `y` means move `y` meters right.
   4. Negative `y` means move `y` meters left.
   5. Positive `z` means lose `z` meters altitude.
   6. Negative `z` means gain `z` meters altitude.

## 17. Polygon Fence

1. ArduPilot supports fences to allow your vehicle to only fly at certain areas.
2. Start the MAVProxy using `mavproxy.py --master=127.0.0.1:14550 --console --map`.
3. To enable fences, `param set FENCE_ENABLE 1` or `fence enable`.
4. To disable fences, `param set FENCE_ENABLE 0` or `fence disable`.
5. `FENCE_TYPE` is a bitmask parameter and used to which fence types will be used.
   1. By default, `7`, maximum altitude, circle, and polygon fences are enabled.
   2. To enable minimum altitude, do `param set FENCE_TYPE 15`, and also set minimum altitude
   like `param set FENCE_ALT_MIN 10` but with doing this, vehicle can't take off if 
   `FENCE_ALT_MIN` is greater than zero. So for takeoff, `fence disable` must be done.
6. By default, there is a cylindrical fence centered at home location with minimum and maximum altitudes.
   1. Radius can be set using `param set FENCE_RADIUS 300`. By doing that vehicle can't go further than 300 meters.
   2. Maximum altitude can be set using `param set FENCE_ALT_MAX 50`. By doing that vehicle can't fly higher than 50 meters.
   3. Minimum altitude can also be set using `param set FENCE_ALT_MIN 10` but `param set FENCE_TYPE 15` must be done. By doing that
   vehicle can't go lower than 10 meters.
7. By default, vehicle do RTL when breaches fence but behavior can be set using FENCE_ACTION.
8. If you want to disable user input during landing, `param set LAND_REPOSITION 0`

Just right click then choose `fence` -> `draw`. After the boundary created, the drone will not going to outside of the boundary, and it will try to move it's position according to the defined polygon shape.

[Source](https://ardupilot.org/copter/docs/parameters.html#fence-parameters)

## 19. Param Editor

```console
module load paramedit
```

## 20. Time Synchronization

1. Connect to the vehicle using: `mavproxy.py --master=127.0.0.1:14550`
2. Load the module `module load system_time`
3. Set the parameter `param set BRD_RTC_TYPES=1` (1st bit is enough).
4. After loading the module MAVProxy automatically sends `SYSTEM_TIME` messages to autopilot.
5. By default, MAVProxy sends messages every 10s and can be changed using:
   1. `system_time set interval_timesync X` where `X` is interval in seconds to send `TIMESYNC` message.
   2. `system_time set interval X` where `X` is interval in seconds to send `SYSTEM_TIME` message.
6. `system_time set verbose true` to show messages on air.
7. `system_time set verbose false` to hide messages on air.

[Source](https://ardupilot.org/mavproxy/docs/modules/systemtime.html)

## 21. Terrain Module

1. Terrain module in MAVProxy provides terrain data by downloading them from internet and cache inside SD card of 
flight controller to use in terrain data related flight modes (any commands framed as 
[MAV_FRAME_GLOBAL_TERRAIN_ALT](https://mavlink.io/en/messages/common.html#MAV_FRAME_GLOBAL_TERRAIN_ALT) 
or [MAV_FRAME_GLOBAL_TERRAIN_ALT_INT](https://mavlink.io/en/messages/common.html#MAV_FRAME_GLOBAL_TERRAIN_ALT_INT)).
1. Connect to the vehicle using `mavproxy.py --master=127.0.0.1:14550 --load-module="map"`.
2. After starting MAVProxy `module load terrain`.
3. `terrain status` is used to show requested or supplied terrain data.
4. `terrain check` is used to query flight stack to show terrain related information of the position clicked on map.
5. `terrain check LATITUDE LONGITUDE` is used to query flight stack to show terrain related information of the position.

[Source](https://ardupilot.org/mavproxy/docs/modules/terrain.html)







