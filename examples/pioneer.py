#!/usr/bin/env python3
import time
import sys
import numpy as np

sys.path.append("..")
from pyrep.api import VRepApi
from pyrep.common import fix_angle_notation, Coordinates


class RobotPosition:

    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    def __str__(self):
        return "(x={:.3f}, y={:.3f}, theta={:.3f})"\
               .format(round(self.x, 3), round(self.y, 3), round(np.rad2deg(self.theta), 3))


class PioneerP3DX:

    def __init__(self, api: VRepApi):
        self._api = api
        # Constants
        self.num_sonars = 16
        self.wheels_distance = 0.36205
        self.wheel_radius = 0.0975
        self.motor_velocity_max = 8.0
        self.sonar_angles = [90, 50, 30, 10, 350, 330, 310, 270, 270, 230, 210, 190, 170, 150, 130, 90]
        self.sonar_detect_min_dist = 0.2
        self.sonar_detect_max_dist = 0.5
        # Handles
        self._ground_truth = api.sensor.ground_truth("Pioneer_p3dx")
        self._left_motor = api.joint.with_velocity_control("Pioneer_p3dx_leftMotor")
        self._right_motor = api.joint.with_velocity_control("Pioneer_p3dx_rightMotor")
        self._sonars = []
        for i in range(1, 17):
            self._sonars.append(api.sensor.proximity("Pioneer_p3dx_ultrasonicSensor" + str(i)))
        # Sonar values
        # -1 == no detection, or detection z coorditate
        self.sonar_readings = np.full(self.num_sonars, -1.0, dtype=np.float)
        # 0.0 == far, 1.0 == close
        self.sonar_readings_normalized = np.zeros(self.num_sonars, dtype=np.float)
        # Ground truth position
        self.real_position = RobotPosition(0, 0, 0)

    def rotate_right(self, speed=2.0):
        self._move(speed, -speed)

    def rotate_left(self, speed=2.0):
        self._move(-speed, speed)

    def move_forward(self, speed=2.0):
        self._move(speed, speed)

    def move_backward(self, speed=2.0):
        self._move(-speed, -speed)

    def stop_moving(self):
        self._move(0, 0)

    def drive(self, linear_velocity, angular_velocity):
        left_velocity =  (2 * linear_velocity - self.wheels_distance * angular_velocity) / (2 * self.wheel_radius)
        right_velocity = (2 * linear_velocity + self.wheels_distance * angular_velocity) / (2 * self.wheel_radius)
        self._move(right_velocity, left_velocity)

    def _move(self, left: float, right: float):
        self._left_motor.set_target_velocity(left)
        self._right_motor.set_target_velocity(right)

    # Get reading from one sonar
    def _get_sonar_reading(self, sonar_number: int) -> Coordinates():
        if not 0 <= sonar_number < self.num_sonars:
            raise Exception("Sonar number does not exist (zero indexed): " + str(sonar_number))
        state, coordinate = self._sonars[sonar_number].read()
        # if streamming has not begun
        while coordinate is None:
            time.sleep(0.1)
            state, coordinate = self._sonars[sonar_number].read()
        if state == 0:
            return -1.0
        return coordinate.z

    # Update the readings of all sonars
    # And update normalized readings
    def update_sonar_readings(self):
        for i, _ in enumerate(self.sonar_readings):
            reading = self._get_sonar_reading(i)
            # If reading is invalid or farther than maximum distance
            if reading == -1 or reading > self.sonar_detect_max_dist:
                self.sonar_readings[i] = -1
                self.sonar_readings_normalized[i] = 0.0
            else:
                # If reading is closer than minimum distance
                if reading < self.sonar_detect_min_dist:
                    reading = self.sonar_detect_min_dist
                self.sonar_readings[i] = reading
                self.sonar_readings_normalized[i] = 1 - (reading - self.sonar_detect_min_dist) / (self.sonar_detect_max_dist - self.sonar_detect_min_dist)

    # Update robot position and orientation
    def update_real_position(self):
        position = self._ground_truth.get_position()
        orientation = self._ground_truth.get_orientation()
        # if streamming has not begun
        while(self._ground_truth.get_position() is None
              or self._ground_truth.get_orientation() is None):
            time.sleep(0.1)
            position = self._ground_truth.get_position()
            orientation = self._ground_truth.get_orientation()
        self.real_position = RobotPosition(position.x, position.y, fix_angle_notation(orientation.gamma))


# Example usage
if __name__ == "__main__":
    with VRepApi.connect("127.0.0.1", 19997) as api:
        pioneer = PioneerP3DX(api)
        while True:
            pioneer.update_real_position()
            print(pioneer.real_position)

            pioneer.update_sonar_readings()
            rl = pioneer.sonar_readings_normalized[5]
            ll = pioneer.sonar_readings_normalized[2]

            if rl > 0.5:
                pioneer.rotate_left()
            elif ll > 0.5:
                pioneer.rotate_right()
            else:
                pioneer.move_forward()
            time.sleep(0.1)
