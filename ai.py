import time
import random
import math

class AIModule:
    def __init__(self):
        self.anomaly_log = []

    def detect_environment_pattern(self, env_readings):
        if env_readings["temperature"] > 70 and env_readings["humidity"] < 20:
            print("[AI] Possible fire conditions detected.")
            return "fire_risk"
        if env_readings["sound_level"] > 90:
            print("[AI] Possible wildlife or machinery detected.")
            return "anomaly_noise"
        return "normal"

    def detect_sensor_anomaly(self, history):
        if len(history) < 2:
            return None
        prev = history[-2][1]
        latest = history[-1][1]
        anomalies = []
        for key in latest:
            if abs(latest[key] - prev.get(key, latest[key])) > 30:
                anomalies.append(key)
        if anomalies:
            msg = f"[AI] Sudden change in: {', '.join(anomalies)}"
            print(msg)
            self.anomaly_log.append((time.time(), msg))
            return msg
        return None

    def predict_action(self, battery_level, light_level):
        if battery_level < 25 and light_level < 100:
            print("[AI] Predicting: Enter low power mode.")
            return "pause_mission"
        return "continue"

class VisionAIModule:
    def __init__(self):
        self.detected_shapes = ["cube", "rectangular_prism", "sphere", "cylinder", "cone"]

    def detect_shape(self):
        return random.choice(self.detected_shapes)

class ShapeVolumeDetection:
    def __init__(self, claw_volume_min_kg=0.0, claw_volume_max_kg=10.0):
        self.claw_volume_min_kg = claw_volume_min_kg
        self.claw_volume_max_kg = claw_volume_max_kg

    def evaluate_claw_grip(self, volume):
        if volume < self.claw_volume_min_kg:
            print("The object is too light to be picked up by the claw.")
        elif volume > self.claw_volume_max_kg:
            print("The object is too heavy to be picked up by the claw.")
        else:
            print("The object can be picked up by the claw.")

    def cube_volume(self):
        edge_length = 10.0
        volume = pow(edge_length, 3)
        self.evaluate_claw_grip(volume)
        return volume

    def rectangular_prism_volume(self):
        length = 10.0
        width = 8.0
        height = 6.0
        volume = length * width * height
        self.evaluate_claw_grip(volume)
        return volume

    def sphere_volume(self):
        radius = 5.0
        volume = (4 / 3) * math.pi * pow(radius, 3)
        self.evaluate_claw_grip(volume)
        return volume

    def cylinder_volume(self):
        radius = 5.0
        height = 20.0
        volume = math.pi * pow(radius, 2) * height
        self.evaluate_claw_grip(volume)
        return volume

    def cone_volume(self):
        radius = 5.0
        height = 20.0
        volume = (1 / 3) * math.pi * pow(radius, 2) * height
        self.evaluate_claw_grip(volume)
        return volume 