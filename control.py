import time
from .mechanical import RobotArm, ArmRotation, WheelServoController
from .sensors import EnvironmentalSensor, LiDARScanner
from .ai import AIModule, VisionAIModule, ShapeVolumeDetection

class RobotController:
    def __init__(self, robotarm, armrotation, vision_ai_module, shape_volume_detector):
        self.robotarm = robotarm
        self.armrotation = armrotation
        self.vision_ai_module = vision_ai_module
        self.shape_volume_detector = shape_volume_detector

    def power_button(self, power_on=False, power_off=False):
        if power_off:
            print("Power is off.")
            self.robotarm.active = False
            self.armrotation.active = False
            return False
        elif power_on:
            print("Power is on.")
            self.robotarm.active = True
            self.armrotation.active = True
            return True

    def rotational_direction_robotarm(self, delta, right_rotate=False, left_rotate=False, complete_rotate=False):
        if self.armrotation.active:
            print("Robot arm rotation is active.")
            if right_rotate:
                self.armrotation.rotation_angle += delta
            if left_rotate:
                self.armrotation.rotation_angle -= delta
            if complete_rotate:
                self.armrotation.rotation_angle = 360
            print(f"Updated rotation angle: {self.armrotation.rotation_angle}°")

    def activate_arm_movement(self):
        if self.robotarm.active:
            print("Executing arm movement...")
            self.robotarm.arm_movement()

    def directional_movement_robotarm(self, right_move=False, left_move=False, up_move=False, down_move=False, forward_move=False, backward_move=False):
        if self.robotarm.active:
            print("Setting directional movement commands...")
            self.robotarm.right_move = right_move
            self.robotarm.left_move = left_move
            self.robotarm.up_move = up_move
            self.robotarm.down_move = down_move
            self.robotarm.forward_move = forward_move
            self.robotarm.back_move = backward_move
            self.activate_arm_movement()

    def analyze_object_with_ai(self):
        detected_shape = self.vision_ai_module.detect_shape()
        print(f"Detected shape: {detected_shape}")
        
        shape_volume_map = {
            "cube": self.shape_volume_detector.cube_volume,
            "rectangular_prism": self.shape_volume_detector.rectangular_prism_volume,
            "sphere": self.shape_volume_detector.sphere_volume,
            "cylinder": self.shape_volume_detector.cylinder_volume,
            "cone": self.shape_volume_detector.cone_volume
        }
        
        if detected_shape in shape_volume_map:
            shape_volume_map[detected_shape]()
        else:
            print("Shape not Identified.")

class AutonomousDecisionEngine:
    def __init__(self):
        self.mission_objective = None
        self.last_sensor_input = {}
        self.actions_log = []
        self.mission_start_time = time.time()
        self.timeout_limit = 600  # seconds

    def set_mission_objective(self, objective):
        self.mission_objective = objective
        print(f"[DECISION ENGINE] Mission objective set: {objective}")

    def update_sensor_input(self, data):
        self.last_sensor_input = data
        print(f"[DECISION ENGINE] Sensor data updated: {data}")

    def evaluate_mission(self):
        if not self.last_sensor_input:
            print("[DECISION ENGINE] No sensor data to evaluate.")
            return
        elapsed = time.time() - self.mission_start_time
        if elapsed > self.timeout_limit:
            print("[DECISION ENGINE] Mission timeout reached. Triggering retry/abort.")
            return "mission_timeout"

        decision = "continue"
        confidence_score = 0.9
        if self.last_sensor_input.get("obstacle_detected"):
            decision = "avoid_obstacle"
            confidence_score = 0.95
        elif self.last_sensor_input.get("target_reached"):
            decision = "complete_mission"
            confidence_score = 1.0
        self.actions_log.append((time.time(), decision, confidence_score))
        print(f"[DECISION ENGINE] Decision made: {decision} (confidence: {confidence_score})")
        return decision

class SafetySystem:
    def __init__(self):
        self.emergency_override = False
        self.abort_triggered = False
        self.safety_log = []

    def check_conditions(self, sensor_input):
        if sensor_input.get("collision_risk"):
            self.activate_emergency_override()
        if sensor_input.get("system_fault"):
            self.trigger_mission_abort()
        if sensor_input.get("temperature") and sensor_input["temperature"] > 60:
            self.activate_emergency_override()

    def activate_emergency_override(self):
        self.emergency_override = True
        self.safety_log.append((time.time(), "emergency_override"))
        print("[SAFETY] Emergency override activated.")

    def trigger_mission_abort(self):
        self.abort_triggered = True
        self.safety_log.append((time.time(), "mission_abort"))
        print("[SAFETY] Mission aborted due to critical fault.")

    def reset_safety_state(self):
        self.emergency_override = False
        self.abort_triggered = False
        print("[SAFETY] Safety state reset.")

    def is_safe_to_proceed(self):
        return not self.emergency_override and not self.abort_triggered

class PowerMonitor:
    def __init__(self, threshold=20):
        self.battery_level = 100
        self.low_power_threshold = threshold
        self.power_log = []
        self.power_source = "battery"  # or 'solar'

    def update_battery_level(self, level, source="battery"):
        self.battery_level = level
        self.power_source = source
        self.power_log.append((time.time(), level, source))
        print(f"[POWER] Battery level: {level}%, Source: {source}")
        if self.battery_level <= self.low_power_threshold:
            self.trigger_low_power_mode()

    def trigger_low_power_mode(self):
        print("[POWER] LOW POWER MODE TRIGGERED. Conserving resources...")

    def estimate_runtime(self, drain_rate_per_min=1):
        if drain_rate_per_min == 0:
            return float('inf')
        return self.battery_level / drain_rate_per_min

    def is_critical(self):
        return self.battery_level <= self.low_power_threshold 