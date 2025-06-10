import os
import json
import time
import math
import random
from datetime import datetime

DATA_DIR = os.path.dirname(__file__)
STATUS_FILE = os.path.join(DATA_DIR, 'vehicle_status.json')
LOG_FILE = os.path.join(DATA_DIR, 'vehicle_logs.txt')
COMMAND_FILE = os.path.join(DATA_DIR, 'vehicle_commands.json')
RECON_FILE = os.path.join(DATA_DIR, 'recon_data.json')
RECON_LOG = os.path.join(DATA_DIR, 'recon_log.txt')

# Default route: list of (lat, lon) tuples
DEFAULT_ROUTE = [
    (37.7749, -122.4194),  # San Francisco
    (37.8044, -122.2711),  # Oakland
    (37.6879, -122.4702),  # Daly City
    (37.4419, -122.1430),  # Palo Alto
]

HAZARD_TYPES = [
    'snow', 'wind', 'hurricane', 'tornado', 'tree', 'car crash', 'flood', 'fire', 'ice', 'fog', 'rockslide'
]

class VehicleSim:
    def __init__(self):
        self.route = DEFAULT_ROUTE.copy()
        self.current_idx = 0
        self.position = self.route[0]
        self.speed = 0.001  # degrees per update (fake speed)
        self.battery = 100.0
        self.status = 'idle'
        self.reroute_reason = None
        self.last_command_id = None
        self.recon_mode = False
        self.hazards = []  # List of detected hazards
        self.recon_data = []  # Recon log for dashboard

    def move_towards_next_waypoint(self):
        if not self.route or self.current_idx >= len(self.route):
            self.status = 'idle'
            return
        target = self.route[self.current_idx]
        lat, lon = self.position
        tlat, tlon = target
        dlat = tlat - lat
        dlon = tlon - lon
        dist = math.hypot(dlat, dlon)
        if dist < self.speed:
            self.position = target
            self.current_idx += 1
            self.log_event(f"Reached waypoint {self.current_idx}: {target}")
            if self.recon_mode:
                self.perform_recon_scan(target)
            if self.current_idx >= len(self.route):
                self.status = 'arrived'
        else:
            self.position = (lat + dlat/dist*self.speed, lon + dlon/dist*self.speed)
            self.status = 'enroute'
            if self.recon_mode and random.random() < 0.1:
                self.perform_recon_scan(self.position)
        self.battery = max(0.0, self.battery - 0.01)

    def handle_commands(self):
        if not os.path.exists(COMMAND_FILE):
            return
        try:
            with open(COMMAND_FILE) as f:
                commands = json.load(f)
        except Exception:
            commands = []
        if not commands:
            return
        for cmd in commands:
            cmd_id = str(cmd)
            if cmd_id == self.last_command_id:
                continue
            action = cmd.get('action')
            if action == 'start':
                self.status = 'enroute'
                self.log_event('Vehicle started')
            elif action == 'stop':
                self.status = 'stopped'
                self.log_event('Vehicle stopped')
            elif action == 'manual':
                self.status = f"manual: {cmd.get('direction')} at {cmd.get('speed')}"
                self.log_event(f"Manual control: {cmd.get('direction')} at {cmd.get('speed')}")
            elif action == 'add_route':
                self.route = cmd.get('route', DEFAULT_ROUTE)
                self.current_idx = 0
                self.position = self.route[0]
                self.status = 'enroute'
                self.log_event(f"Route added: {self.route}")
            elif action == 'delete_route':
                self.route = []
                self.current_idx = 0
                self.status = 'idle'
                self.log_event('Route deleted')
            elif action == 'update_route':
                self.route = cmd.get('route', DEFAULT_ROUTE)
                self.current_idx = 0
                self.position = self.route[0]
                self.status = 'enroute'
                self.log_event(f"Route updated: {self.route}")
            elif action == 'reroute':
                self.route = self.simulate_reroute()
                self.current_idx = 0
                self.position = self.route[0]
                self.status = 'rerouted'
                self.reroute_reason = cmd.get('reason', 'unknown')
                self.log_event(f"Rerouted due to {self.reroute_reason}")
            elif action == 'recon':
                self.recon_mode = True
                self.log_event('Recon mission started')
            elif action == 'stop_recon':
                self.recon_mode = False
                self.log_event('Recon mission stopped')
            self.last_command_id = cmd_id
        with open(COMMAND_FILE, 'w') as f:
            json.dump([], f)

    def perform_recon_scan(self, location):
        # Simulate detection of hazards/objects
        detected = []
        if random.random() < 0.4:  # 40% chance to detect something
            hazard_type = random.choice(HAZARD_TYPES)
            hazard = {
                'type': hazard_type,
                'location': {'lat': location[0], 'lon': location[1]},
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'severity': random.choice(['minor', 'moderate', 'severe'])
            }
            self.hazards.append(hazard)
            detected.append(hazard)
            self.log_event(f"Hazard detected: {hazard_type} at {location}")
            self.log_recon(f"Hazard detected: {hazard_type} at {location}")
            # If severe, pause or reroute
            if hazard['severity'] == 'severe':
                self.status = 'paused (hazard)'
                self.log_event(f"Vehicle paused due to severe hazard: {hazard_type}")
        # Simulate recon image/sensor data
        recon_entry = {
            'location': {'lat': location[0], 'lon': location[1]},
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'detected': detected,
            'image': f"recon_image_{int(time.time())}.jpg",
            'sensors': {
                'temperature': round(random.uniform(-10, 40), 1),
                'wind_speed': round(random.uniform(0, 100), 1),
                'humidity': round(random.uniform(10, 90), 1)
            }
        }
        self.recon_data.append(recon_entry)
        self.log_recon(f"Recon scan at {location}: {recon_entry}")
        # Save recon data to file
        with open(RECON_FILE, 'w') as f:
            json.dump(self.recon_data, f, indent=2)

    def simulate_reroute(self):
        lat, lon = self.position
        new_wp = (lat + random.uniform(0.01, 0.05), lon + random.uniform(0.01, 0.05))
        return [self.position, new_wp, DEFAULT_ROUTE[-1]]

    def write_status(self):
        status = {
            'position': {'lat': self.position[0], 'lon': self.position[1]},
            'battery': self.battery,
            'status': self.status,
            'route': [{'lat': lat, 'lon': lon} for lat, lon in self.route],
            'current_waypoint': self.current_idx,
            'reroute_reason': self.reroute_reason,
            'hazards': self.hazards[-10:],  # last 10 hazards
            'recon_mode': self.recon_mode,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        }
        with open(STATUS_FILE, 'w') as f:
            json.dump(status, f, indent=2)

    def log_event(self, msg):
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{datetime.utcnow().isoformat()}] {msg}\n")

    def log_recon(self, msg):
        with open(RECON_LOG, 'a') as f:
            f.write(f"[{datetime.utcnow().isoformat()}] {msg}\n")

    def run(self):
        while True:
            self.handle_commands()
            if (self.status.startswith('enroute') or self.status == 'rerouted') and not self.status.startswith('paused'):
                self.move_towards_next_waypoint()
            self.write_status()
            time.sleep(2)

if __name__ == '__main__':
    sim = VehicleSim()
    sim.run() 