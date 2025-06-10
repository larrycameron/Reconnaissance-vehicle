# API Documentation

## Core Components

### RobotArm
The main robot arm control class that handles all mechanical movements.

#### Methods
- `move_forward()`: Move the arm forward
- `move_backward()`: Move the arm backward
- `move_up()`: Move the arm upward
- `move_down()`: Move the arm downward
- `move_left()`: Move the arm left
- `move_right()`: Move the arm right

### ArmRotation
Controls the rotation of the robot arm.

#### Methods
- `rotate(degrees)`: Rotate the arm by specified degrees
- `get_current_angle()`: Get current rotation angle
- `reset_rotation()`: Reset to default position

### RobotController
Main controller class that coordinates all robot components.

#### Methods
- `power_button(power_on)`: Turn the system on/off
- `directional_movement_robotarm(**kwargs)`: Control arm movement
- `rotate_arm(degrees)`: Rotate the arm
- `open_claw()`: Open the claw
- `close_claw()`: Close the claw
- `emergency_stop()`: Emergency stop procedure

### VisionAIModule
Handles computer vision and AI processing.

#### Methods
- `detect_objects()`: Detect objects in camera view
- `analyze_shape()`: Analyze detected shapes
- `calculate_volume()`: Calculate object volume

### EnvironmentalSensors
Manages all environmental sensors.

#### Methods
- `get_distance()`: Get distance to nearest object
- `detect_collision()`: Check for potential collisions
- `get_temperature()`: Get ambient temperature
- `get_humidity()`: Get ambient humidity

### ClawControl
Controls the robot's claw mechanism.

#### Methods
- `open()`: Open the claw
- `close()`: Close the claw
- `get_pressure()`: Get current pressure
- `get_mass()`: Get mass of held object

### PowerMonitor
Monitors and manages power systems.

#### Methods
- `get_battery_level()`: Get current battery level
- `get_solar_power()`: Get solar power generation
- `get_power_consumption()`: Get current power consumption

### SafetySystem
Manages safety protocols and emergency procedures.

#### Methods
- `check_safety()`: Perform safety checks
- `emergency_stop()`: Execute emergency stop
- `get_safety_status()`: Get current safety status

## Web Dashboard API

### Endpoints

#### GET /
- Description: Main dashboard interface
- Response: HTML dashboard page

#### GET /status
- Description: Get current system status
- Response: JSON with system status

#### GET /logs
- Description: Get system logs
- Response: JSON array of log entries

#### POST /control/start
- Description: Start the system
- Response: JSON with start status

#### POST /control/stop
- Description: Stop the system
- Response: JSON with stop status

#### POST /control/manual
- Description: Send manual control commands
- Body: JSON with control parameters
- Response: JSON with command status

#### GET /camera/snapshot
- Description: Get latest camera image
- Response: Image file

## Error Handling

All API endpoints return appropriate HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

Error responses include a JSON object with:
- `error`: Error message
- `code`: Error code
- `details`: Additional error details (if available) 