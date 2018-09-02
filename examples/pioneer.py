#!/usr/bin/env python3
import time
import sys

sys.path.append("..")
from pyrep.api import VRepApi

class PioneerP3DX:

    def __init__(self, api: VRepApi):
        self._api = api
        self._ground_truth = api.sensor.ground_truth("Pioneer_p3dx")
        self._left_motor = api.joint.with_velocity_control("Pioneer_p3dx_leftMotor")
        self._right_motor = api.joint.with_velocity_control("Pioneer_p3dx_rightMotor")
        self._sonar_sensors = []
        for i in range(1, 17):
            self._sonar_sensors.append(api.sensor.proximity("Pioneer_p3dx_ultrasonicSensor" + str(i)))

    def rotate_right(self, speed=2.0):
        self._move(speed, -speed)

    def rotate_left(self, speed=2.0):
        self._move(-speed, speed)

    def move_forward(self, speed=2.0):
        self._move(speed, speed)

    def move_backward(self, speed=2.0):
        self._move(-speed, -speed)

    def _move(self, left: float, right: float):
        self._left_motor.set_target_velocity(left)
        self._right_motor.set_target_velocity(right)

    def sensor_distance(self, sensor_number: int):
        state, coordinate = self._sonar_sensors[sensor_number].read()
        if state == 0:
            return -1
        return coordinate.get_z()

    def get_position(self):
        return self._ground_truth.get_position()


# Example usage
if __name__ == "__main__":
    with VRepApi.connect("127.0.0.1", 19997) as api:
        pioneer = PioneerP3DX(api)
        while True:
            rl = pioneer.sensor_distance(6)
            ll = pioneer.sensor_distance(3)

            if 0.01 < rl < 1:
                pioneer.rotate_left()
            elif 0.01 < ll < 1:
                pioneer.rotate_right()
            else:
                pioneer.move_forward()
            time.sleep(0.1)
