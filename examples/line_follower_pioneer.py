#!/usr/bin/env python3
import sys
import time
sys.path.append("..")
from pyrep.api import VRepApi
from pyrep.sensors import VisionSensor

class PioneerP3DX:

    def __init__(self, api: VRepApi):
        self._api = api
        self._left_motor = api.joint.with_velocity_control("Pioneer_p3dx_leftMotor")
        self._right_motor = api.joint.with_velocity_control("Pioneer_p3dx_rightMotor")
        self._left_sensor = api.sensor.vision("LeftRGBSensor")  # type: VisionSensor
        self._right_sensor = api.sensor.vision("RightRGBSensor")  # type: VisionSensor

    def set_two_motor(self, left: float, right: float):
        self._left_motor.set_target_velocity(left)
        self._right_motor.set_target_velocity(right)

    def rotate_right(self, speed=2.0):
        self.set_two_motor(speed, -speed)

    def rotate_left(self, speed=2.0):
        self.set_two_motor(-speed, speed)

    def move_forward(self, speed=2.0):
        self.set_two_motor(speed, speed)

    def move_backward(self, speed=2.0):
        self.set_two_motor(-speed, -speed)

    def right_color(self) -> int:
        image = None
        while image is None:
            image = self._right_sensor.raw_image(is_grey_scale=True)  # type: List[int]
            time.sleep(0.1)
        average = image.sum() / image.size
        return average

    def left_color(self) -> int:
        image = None
        while image is None:
            image = self._left_sensor.raw_image(is_grey_scale=True)  # type: List[int]
            time.sleep(0.1)
        average = image.sum() / image.size
        return average


with VRepApi.connect("127.0.0.1", 19997) as api:
    robot = PioneerP3DX(api)
    while True:
        lclr = robot.left_color()
        rclr = robot.right_color()
        if lclr < 100:
            robot.rotate_left(0.3)
        elif rclr < 100:
            robot.rotate_right(0.3)
        else:
            robot.move_forward(0.3)
        time.sleep(0.01)
