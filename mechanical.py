class RobotArm:
    def __init__(self, right_move=False, left_move=False, up_move=False, down_move=False, forward_move=False, backward_move=False):
        self.right_move = right_move
        self.left_move = left_move
        self.up_move = up_move
        self.down_move = down_move
        self.forward_move = forward_move
        self.back_move = backward_move
        self.position = (0, 0, 0)
        self.active = False

    def arm_movement(self):
        if not self.active:
            return

        print("Robot arm is active.")
        x, y, z = self.position

        if self.right_move:
            x += 1
            print("Moving right → x += 1")
        if self.left_move:
            x -= 1
            print("Moving left → x -= 1")
        if self.up_move:
            y += 1
            print("Moving up → y += 1")
        if self.down_move:
            y -= 1
            print("Moving down → y -= 1")
        if self.forward_move:
            z += 1
            print("Moving forward → z += 1")
        if self.back_move:
            z -= 1
            print("Moving backward → z -= 1")

        self.position = (x, y, z)
        print(f"Updated 3D Position: x={x}, y={y}, z={z}")

class ArmRotation:
    def __init__(self, active_arm):
        self.rotation_angle = 0
        self.active = False
        self.active_arm = active_arm

    def rotate(self, delta, right_rotate=False, left_rotate=False, complete_rotate=False):
        if not self.active:
            return

        print("Robot arm rotation is active.")
        if right_rotate:
            self.rotation_angle += delta
        if left_rotate:
            self.rotation_angle -= delta
        if complete_rotate:
            self.rotation_angle = 360
        print(f"Updated rotation angle: {self.rotation_angle}°")

    def reset_rotation(self):
        self.rotation_angle = 0

class ClawControl:
    def __init__(self, open_claw=False, close_claw=False, release_object_from_claw=False, object_held=False, object_mass=0.0, secure_grip=False, safe_pressure=0.0):
        self.open_claw = open_claw
        self.close_claw = close_claw
        self.release_object_from_claw = release_object_from_claw
        self.object_held = object_held
        self.object_mass = object_mass
        self.secure_grip = secure_grip
        self.safe_pressure = safe_pressure

    def claw_movement(self):
        if self.open_claw:
            print("Claw is opening.")
        if self.close_claw:
            print("Claw is closing.")
        if self.release_object_from_claw:
            print("Releasing object from claw.")

    def evaluate_claw_state(self, pressure, mass):
        safe_mass = False
        
        if 15 <= pressure <= 40:
            print("Grip strength is secure.")
            self.secure_grip = True
        elif pressure < 15:
            print("Grip strength is weak.")
            self.secure_grip = False
        elif pressure > 40:
            print("Grip strength is too strong.")
            self.secure_grip = False

        if 0 <= mass <= 10:
            print("Object mass is within the safe range.")
            self.object_mass = mass
            safe_mass = True
        elif mass < 0:
            print("Object mass is negative.")
            safe_mass = False
        elif mass > 10:
            print("Object mass is too heavy.")
            safe_mass = False

        self.object_held = self.secure_grip and safe_mass
        print("Object is being held securely." if self.object_held else "Object is not being held securely.")
        return self.object_held

class WheelServoController:
    def __init__(self):
        self.current_speed = 0
        self.current_direction = "stopped"
        self.encoder_feedback = 0

    def set_speed(self, speed):
        self.current_speed = speed
        print(f"[WHEEL] Speed set to {speed} units")

    def set_direction(self, direction):
        self.current_direction = direction
        print(f"[WHEEL] Direction set to {direction}")

    def stop(self):
        self.current_speed = 0
        self.current_direction = "stopped"
        print("[WHEEL] Wheel stopped")

    def update_encoder_feedback(self, value):
        self.encoder_feedback = value
        print(f"[WHEEL] Encoder feedback: {value}")

class SolarPanel:
    def __init__(self):
        self.is_deployed = False
        self.power_generated = 0.0
        self.generation_log = []

    def deploy(self):
        self.is_deployed = True
        print("[SOLAR] Deployed.")

    def retract(self):
        self.is_deployed = False
        print("[SOLAR] Retracted.")

    def update_power_generated(self, sunlight_intensity):
        if self.is_deployed:
            self.power_generated = sunlight_intensity * 0.8
            self.generation_log.append((time.time(), self.power_generated))
            print(f"[SOLAR] Power generated: {self.power_generated:.2f}W")
        else:
            self.power_generated = 0.0
            print("[SOLAR] Panel retracted. No power generated.") 