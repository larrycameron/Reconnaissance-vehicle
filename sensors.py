import time
import random
import math
import matplotlib.pyplot as plt

class EnvironmentalSensors:
    def __init__(self, collision=False, line_tracking=False, proximity_detection=False, obstacle_avoidance=False):
        self.collision = collision
        self.line_tracking = line_tracking
        self.proximity_detection = proximity_detection
        self.obstacle_avoidance = obstacle_avoidance

    def check_collision(self):
        if self.collision:
            print("Collision detected!")

class EnvironmentalSensor:
    def __init__(self):
        self.readings = {
            "temperature": 25.0,
            "humidity": 40.0,
            "air_quality": 50.0,
            "radiation": 0.01,
            "light_level": 300.0,
            "sound_level": 30.0,
            "pressure": 1013.25
        }
        self.log = []

    def read_all_sensors(self):
        self.log_environment()
        print("[ENVIRONMENT] Sensor values updated.")
        return self.readings

    def evaluate_conditions(self):
        evaluations = []
        if self.readings["temperature"] > 45:
            evaluations.append("High Temperature")
        if self.readings["air_quality"] > 100:
            evaluations.append("Poor Air Quality")
        if self.readings["radiation"] > 0.05:
            evaluations.append("Radiation Risk")
        if self.readings["light_level"] < 50:
            evaluations.append("Low Visibility")
        if self.readings["sound_level"] > 85:
            evaluations.append("High Noise")
        return evaluations

    def log_environment(self):
        self.log.append((time.time(), self.readings.copy()))
        print("[ENVIRONMENT] Readings logged.")

    def trend_summary(self):
        if not self.log:
            return "No data"
        latest = self.log[-1][1]
        trend = {k: "rising" if latest[k] > 50 else "stable" for k in latest}
        print(f"[ENVIRONMENT] Trend summary: {trend}")
        return trend

class LiDARScanner:
    def __init__(self, scan_range=10.0, scan_frequency=1.0, current_location=(0.0, 0.0)):
        self.scan_range = scan_range
        self.scan_frequency = scan_frequency
        self.current_location = current_location
        self.last_scan_data = []
        self.map_log = []
        self.scan_resolution = 1.0

    def pin_on_map(self, location):
        self.current_location = location
        if location not in self.map_log:
            self.map_log.append(location)
        print(f"Location pinned on map: {location}")
    
    def perform_scan(self):
        scan_data = []
        angle = 0.0
        while angle < 360.0:
            distance = round(random.uniform(0.2, self.scan_range), 2)
            scan_data.append((angle, distance))
            angle += self.scan_resolution
        self.last_scan_data = scan_data
        print(f"Performed scan with {len(scan_data)} data points.")
    
    def get_scan_summary(self):
        if not self.last_scan_data:
            return "No scan data available."

        distances = [d for _, d in self.last_scan_data]
        summary = {
            "points": len(distances),
            "min_distance": round(min(distances), 2),
            "max_distance": round(max(distances), 2),
            "average_distance": round(sum(distances) / len(distances), 2)
        }
        return summary

    def plot_scan(self):
        if not self.last_scan_data:
            print("No scan data to plot.")
            return

        angles = [math.radians(angle) for angle, _ in self.last_scan_data]
        distances = [distance for _, distance in self.last_scan_data]

        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)
        ax.plot(angles, distances, marker='.', linestyle='-', linewidth=1)
        ax.set_title("LiDAR Scan Visualization")
        ax.set_rmax(self.scan_range)
        plt.show() 